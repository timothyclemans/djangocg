from djangocg.conf import settings
from djangocg.template import Library

register = Library()

if 'djangocg.contrib.staticfiles' in settings.INSTALLED_APPS:
    from djangocg.contrib.staticfiles.templatetags.staticfiles import static
else:
    from djangocg.templatetags.static import static

static = register.simple_tag(static)
