import os
from djangocg.conf.urls import patterns

here = os.path.dirname(__file__)

urlpatterns = patterns('',
    (r'^custom_templates/(?P<path>.*)$', 'djangocg.views.static.serve', {
        'document_root': os.path.join(here, 'custom_templates'),
    }),
)
