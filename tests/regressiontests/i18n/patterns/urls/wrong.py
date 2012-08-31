from djangocg.conf.urls import include, url
from djangocg.conf.urls.i18n import i18n_patterns
from djangocg.utils.translation import ugettext_lazy as _


urlpatterns = i18n_patterns('',
    url(_(r'^account/'), include('regressiontests.i18n.patterns.urls.wrong_namespace', namespace='account')),
)
