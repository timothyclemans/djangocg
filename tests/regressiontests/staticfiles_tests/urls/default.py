from djangocg.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'djangocg.contrib.staticfiles.views.serve'),
)
