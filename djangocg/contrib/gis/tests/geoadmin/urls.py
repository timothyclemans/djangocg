from djangocg.conf.urls import patterns, include
from djangocg.contrib import admin

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)
