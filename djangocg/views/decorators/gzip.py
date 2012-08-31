from djangocg.utils.decorators import decorator_from_middleware
from djangocg.middleware.gzip import GZipMiddleware

gzip_page = decorator_from_middleware(GZipMiddleware)
gzip_page.__doc__ = "Decorator for views that gzips pages if the client supports it."
