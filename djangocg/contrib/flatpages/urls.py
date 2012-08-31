from djangocg.conf.urls import patterns

urlpatterns = patterns('djangocg.contrib.flatpages.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)
