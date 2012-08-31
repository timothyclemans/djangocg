from djangocg.conf.urls import url
from djangocg.conf.urls import patterns
from djangocg.views.generic import TemplateView


view = TemplateView.as_view(template_name='dummy.html')

urlpatterns = patterns('',
    url(r'^nl/foo/', view, name='not-translated'),
)
