from djangocg.conf.urls import url
from djangocg.conf.urls.i18n import i18n_patterns
from djangocg.utils.translation import ugettext_lazy as _
from djangocg.views.generic import TemplateView


view = TemplateView.as_view(template_name='dummy.html')

urlpatterns = i18n_patterns('',
    url(_(r'^register/$'), view, name='register'),
)
