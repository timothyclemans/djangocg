from djangocg.conf.urls import patterns, include

from . import admin


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)
