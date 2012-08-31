from __future__ import unicode_literals

from djangocg.http import Http404
from djangocg.utils.translation import ugettext as _

def feed(request, url, feed_dict=None):
    """Provided for backwards compatibility."""
    if not feed_dict:
        raise Http404(_("No feeds are registered."))

    try:
        slug, param = url.split('/', 1)
    except ValueError:
        slug, param = url, ''

    try:
        f = feed_dict[slug]
    except KeyError:
        raise Http404(_("Slug %r isn't registered.") % slug)

    instance = f()
    instance.feed_url = getattr(f, 'feed_url', None) or request.path
    instance.title_template = f.title_template or ('feeds/%s_title.html' % slug)
    instance.description_template = f.description_template or ('feeds/%s_description.html' % slug)
    return instance(request)