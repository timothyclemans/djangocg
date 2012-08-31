from djangocg.conf.urls import patterns

urlpatterns = patterns('djangocg.views',
    (r'^(?P<content_type_id>\d+)/(?P<object_id>.*)/$', 'defaults.shortcut'),
)
