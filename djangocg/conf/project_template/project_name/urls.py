from djangocg.conf.urls import patterns, include, url

from djangocg.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', '{{ project_name }}.views.home', name='home'),
    url(r'^login/$', '{{ project_name }}.views.login', name='login'),
    url(r'^logout/$', '{{ project_name }}.views.logout', name='logout'),

    url(r'^admin/doc/', include('djangocg.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
