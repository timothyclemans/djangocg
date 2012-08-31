from djangocg.conf.urls import patterns, include

# special urls for flatpage test cases
urlpatterns = patterns('',
    (r'^flatpage_root', include('djangocg.contrib.flatpages.urls')),
    (r'^accounts/', include('djangocg.contrib.auth.urls')),
)

