# The views used below are normally mapped in djangocg.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from djangocg.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/$', 'djangocg.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'djangocg.contrib.auth.views.logout', name='logout'),
    url(r'^password_change/$', 'djangocg.contrib.auth.views.password_change', name='password_change'),
    url(r'^password_change/done/$', 'djangocg.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password_reset/$', 'djangocg.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'djangocg.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'djangocg.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'djangocg.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
)
