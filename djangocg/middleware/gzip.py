import re

from djangocg.utils.text import compress_string
from djangocg.utils.cache import patch_vary_headers

re_accepts_gzip = re.compile(r'\bgzip\b')

class GZipMiddleware(object):
    """
    This middleware compresses content if the browser allows gzip compression.
    It sets the Vary header accordingly, so that caches will base their storage
    on the Accept-Encoding header.
    """
    def process_response(self, request, response):
        # It's not worth attempting to compress really short responses.
        if len(response.content) < 200:
            return response

        patch_vary_headers(response, ('Accept-Encoding',))

        # Avoid gzipping if we've already got a content-encoding.
        if response.has_header('Content-Encoding'):
            return response

        # MSIE have issues with gzipped response of various content types.
        if "msie" in request.META.get('HTTP_USER_AGENT', '').lower():
            ctype = response.get('Content-Type', '').lower()
            if not ctype.startswith("text/") or "javascript" in ctype:
                return response

        ae = request.META.get('HTTP_ACCEPT_ENCODING', '')
        if not re_accepts_gzip.search(ae):
            return response

        # Return the compressed content only if it's actually shorter.
        compressed_content = compress_string(response.content)
        if len(compressed_content) >= len(response.content):
            return response

        if response.has_header('ETag'):
            response['ETag'] = re.sub('"$', ';gzip"', response['ETag'])

        response.content = compressed_content
        response['Content-Encoding'] = 'gzip'
        response['Content-Length'] = str(len(response.content))
        return response
