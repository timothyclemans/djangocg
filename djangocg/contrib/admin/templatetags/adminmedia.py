import warnings
from djangocg.template import Library
from djangocg.templatetags.static import PrefixNode

register = Library()

@register.simple_tag
def admin_media_prefix():
    """
    Returns the string contained in the setting ADMIN_MEDIA_PREFIX.
    """
    warnings.warn(
        "The admin_media_prefix template tag is deprecated. "
        "Use the static template tag instead.", DeprecationWarning)
    return PrefixNode.handle_simple("ADMIN_MEDIA_PREFIX")
