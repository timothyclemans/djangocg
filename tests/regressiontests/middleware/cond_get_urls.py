from djangocg.conf.urls import patterns
from djangocg.http import HttpResponse

urlpatterns = patterns('',
    (r'^$', lambda request: HttpResponse('root is here')),
)
