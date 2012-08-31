import re
from djangocg.conf import settings
from djangocg.conf.urls import patterns, url
from djangocg.core.exceptions import ImproperlyConfigured

def static(prefix, view='djangocg.views.static.serve', **kwargs):
    """
    Helper function to return a URL pattern for serving files in debug mode.

    from djangocg.conf import settings
    from djangocg.conf.urls.static import static

    urlpatterns = patterns('',
        # ... the rest of your URLconf goes here ...
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    """
    # No-op if not in debug mode or an non-local prefix
    if not settings.DEBUG or (prefix and '://' in prefix):
        return []
    elif not prefix:
        raise ImproperlyConfigured("Empty static prefix not permitted")
    return patterns('',
        url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
    )
