from djangocg.conf.urls import patterns, url
from djangocg.utils.translation import ugettext_lazy as _
from djangocg.views.generic import TemplateView


view = TemplateView.as_view(template_name='dummy.html')

urlpatterns = patterns('',
    url(_(r'^register/$'), view, name='register'),
    url(_(r'^register-without-slash$'), view, name='register-without-slash'),
)
