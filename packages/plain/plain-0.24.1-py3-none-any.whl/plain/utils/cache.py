"""
This module contains helper functions for controlling caching. It does so by
managing the "Vary" header of responses. It includes functions to patch the
header of response objects directly and decorators that change functions to do
that header-patching themselves.

For information on the Vary header, see RFC 9110 Section 12.5.5.

Essentially, the "Vary" HTTP header defines which headers a cache should take
into account when building its cache key. Requests with the same path but
different header content for headers named in "Vary" need to get different
cache keys to prevent delivery of wrong content.

An example: i18n middleware would need to distinguish caches by the
"Accept-language" header.
"""

import time
from collections import defaultdict
from hashlib import md5

from plain.http import Response, ResponseNotModified
from plain.logs import log_response
from plain.runtime import settings
from plain.utils.http import http_date, parse_etags, parse_http_date_safe, quote_etag
from plain.utils.regex_helper import _lazy_re_compile

cc_delim_re = _lazy_re_compile(r"\s*,\s*")


def patch_cache_control(response, **kwargs):
    """
    Patch the Cache-Control header by adding all keyword arguments to it.
    The transformation is as follows:

    * All keyword parameter names are turned to lowercase, and underscores
      are converted to hyphens.
    * If the value of a parameter is True (exactly True, not just a
      true value), only the parameter name is added to the header.
    * All other parameters are added with their value, after applying
      str() to it.
    """

    def dictitem(s):
        t = s.split("=", 1)
        if len(t) > 1:
            return (t[0].lower(), t[1])
        else:
            return (t[0].lower(), True)

    def dictvalue(*t):
        if t[1] is True:
            return t[0]
        else:
            return f"{t[0]}={t[1]}"

    cc = defaultdict(set)
    if response.headers.get("Cache-Control"):
        for field in cc_delim_re.split(response.headers["Cache-Control"]):
            directive, value = dictitem(field)
            if directive == "no-cache":
                # no-cache supports multiple field names.
                cc[directive].add(value)
            else:
                cc[directive] = value

    # If there's already a max-age header but we're being asked to set a new
    # max-age, use the minimum of the two ages. In practice this happens when
    # a decorator and a piece of middleware both operate on a given view.
    if "max-age" in cc and "max_age" in kwargs:
        kwargs["max_age"] = min(int(cc["max-age"]), kwargs["max_age"])

    # Allow overriding private caching and vice versa
    if "private" in cc and "public" in kwargs:
        del cc["private"]
    elif "public" in cc and "private" in kwargs:
        del cc["public"]

    for k, v in kwargs.items():
        directive = k.replace("_", "-")
        if directive == "no-cache":
            # no-cache supports multiple field names.
            cc[directive].add(v)
        else:
            cc[directive] = v

    directives = []
    for directive, values in cc.items():
        if isinstance(values, set):
            if True in values:
                # True takes precedence.
                values = {True}
            directives.extend([dictvalue(directive, value) for value in values])
        else:
            directives.append(dictvalue(directive, values))
    cc = ", ".join(directives)
    response.headers["Cache-Control"] = cc


def get_max_age(response):
    """
    Return the max-age from the response Cache-Control header as an integer,
    or None if it wasn't found or wasn't an integer.
    """
    if "Cache-Control" not in response.headers:
        return
    cc = dict(
        _to_tuple(el) for el in cc_delim_re.split(response.headers["Cache-Control"])
    )
    try:
        return int(cc["max-age"])
    except (ValueError, TypeError, KeyError):
        pass


def set_response_etag(response):
    if not response.streaming and response.content:
        response.headers["ETag"] = quote_etag(
            md5(response.content, usedforsecurity=False).hexdigest(),
        )
    return response


def _precondition_failed(request):
    response = Response(status=412)
    log_response(
        "Precondition Failed: %s",
        request.path,
        response=response,
        request=request,
    )
    return response


def _not_modified(request, response=None):
    new_response = ResponseNotModified()
    if response:
        # Preserve the headers required by RFC 9110 Section 15.4.5, as well as
        # Last-Modified.
        for header in (
            "Cache-Control",
            "Content-Location",
            "Date",
            "ETag",
            "Expires",
            "Last-Modified",
            "Vary",
        ):
            if header in response.headers:
                new_response.headers[header] = response.headers[header]

        # Preserve cookies as per the cookie specification: "If a proxy server
        # receives a response which contains a Set-cookie header, it should
        # propagate the Set-cookie header to the client, regardless of whether
        # the response was 304 (Not Modified) or 200 (OK).
        # https://curl.haxx.se/rfc/cookie_spec.html
        new_response.cookies = response.cookies
    return new_response


def get_conditional_response(request, etag=None, last_modified=None, response=None):
    # Only return conditional responses on successful requests.
    if response and not (200 <= response.status_code < 300):
        return response

    # Get HTTP request headers.
    if_match_etags = parse_etags(request.META.get("HTTP_IF_MATCH", ""))
    if_unmodified_since = request.META.get("HTTP_IF_UNMODIFIED_SINCE")
    if_unmodified_since = if_unmodified_since and parse_http_date_safe(
        if_unmodified_since
    )
    if_none_match_etags = parse_etags(request.META.get("HTTP_IF_NONE_MATCH", ""))
    if_modified_since = request.META.get("HTTP_IF_MODIFIED_SINCE")
    if_modified_since = if_modified_since and parse_http_date_safe(if_modified_since)

    # Evaluation of request preconditions below follows RFC 9110 Section
    # 13.2.2.
    # Step 1: Test the If-Match precondition.
    if if_match_etags and not _if_match_passes(etag, if_match_etags):
        return _precondition_failed(request)

    # Step 2: Test the If-Unmodified-Since precondition.
    if (
        not if_match_etags
        and if_unmodified_since
        and not _if_unmodified_since_passes(last_modified, if_unmodified_since)
    ):
        return _precondition_failed(request)

    # Step 3: Test the If-None-Match precondition.
    if if_none_match_etags and not _if_none_match_passes(etag, if_none_match_etags):
        if request.method in ("GET", "HEAD"):
            return _not_modified(request, response)
        else:
            return _precondition_failed(request)

    # Step 4: Test the If-Modified-Since precondition.
    if (
        not if_none_match_etags
        and if_modified_since
        and not _if_modified_since_passes(last_modified, if_modified_since)
        and request.method in ("GET", "HEAD")
    ):
        return _not_modified(request, response)

    # Step 5: Test the If-Range precondition (not supported).
    # Step 6: Return original response since there isn't a conditional response.
    return response


def _if_match_passes(target_etag, etags):
    """
    Test the If-Match comparison as defined in RFC 9110 Section 13.1.1.
    """
    if not target_etag:
        # If there isn't an ETag, then there can't be a match.
        return False
    elif etags == ["*"]:
        # The existence of an ETag means that there is "a current
        # representation for the target resource", even if the ETag is weak,
        # so there is a match to '*'.
        return True
    elif target_etag.startswith("W/"):
        # A weak ETag can never strongly match another ETag.
        return False
    else:
        # Since the ETag is strong, this will only return True if there's a
        # strong match.
        return target_etag in etags


def _if_unmodified_since_passes(last_modified, if_unmodified_since):
    """
    Test the If-Unmodified-Since comparison as defined in RFC 9110 Section
    13.1.4.
    """
    return last_modified and last_modified <= if_unmodified_since


def _if_none_match_passes(target_etag, etags):
    """
    Test the If-None-Match comparison as defined in RFC 9110 Section 13.1.2.
    """
    if not target_etag:
        # If there isn't an ETag, then there isn't a match.
        return True
    elif etags == ["*"]:
        # The existence of an ETag means that there is "a current
        # representation for the target resource", so there is a match to '*'.
        return False
    else:
        # The comparison should be weak, so look for a match after stripping
        # off any weak indicators.
        target_etag = target_etag.strip("W/")
        etags = (etag.strip("W/") for etag in etags)
        return target_etag not in etags


def _if_modified_since_passes(last_modified, if_modified_since):
    """
    Test the If-Modified-Since comparison as defined in RFC 9110 Section
    13.1.3.
    """
    return not last_modified or last_modified > if_modified_since


def patch_response_headers(response, cache_timeout=None):
    """
    Add HTTP caching headers to the given Response: Expires and
    Cache-Control.

    Each header is only added if it isn't already set.

    cache_timeout is in seconds. The CACHE_MIDDLEWARE_SECONDS setting is used
    by default.
    """
    if cache_timeout is None:
        cache_timeout = settings.CACHE_MIDDLEWARE_SECONDS
    if cache_timeout < 0:
        cache_timeout = 0  # Can't have max-age negative
    if "Expires" not in response.headers:
        response.headers["Expires"] = http_date(time.time() + cache_timeout)
    patch_cache_control(response, max_age=cache_timeout)


def add_never_cache_headers(response):
    """
    Add headers to a response to indicate that a page should never be cached.
    """
    patch_response_headers(response, cache_timeout=-1)
    patch_cache_control(
        response, no_cache=True, no_store=True, must_revalidate=True, private=True
    )


def patch_vary_headers(response, newheaders):
    """
    Add (or update) the "Vary" header in the given Response object.
    newheaders is a list of header names that should be in "Vary". If headers
    contains an asterisk, then "Vary" header will consist of a single asterisk
    '*'. Otherwise, existing headers in "Vary" aren't removed.
    """
    # Note that we need to keep the original order intact, because cache
    # implementations may rely on the order of the Vary contents in, say,
    # computing an MD5 hash.
    if "Vary" in response.headers:
        vary_headers = cc_delim_re.split(response.headers["Vary"])
    else:
        vary_headers = []
    # Use .lower() here so we treat headers as case-insensitive.
    existing_headers = {header.lower() for header in vary_headers}
    additional_headers = [
        newheader
        for newheader in newheaders
        if newheader.lower() not in existing_headers
    ]
    vary_headers += additional_headers
    if "*" in vary_headers:
        response.headers["Vary"] = "*"
    else:
        response.headers["Vary"] = ", ".join(vary_headers)


def _to_tuple(s):
    t = s.split("=", 1)
    if len(t) == 2:
        return t[0].lower(), t[1]
    return t[0].lower(), True
