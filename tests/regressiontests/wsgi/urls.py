from djangocg.conf.urls import url, patterns
from djangocg.http import HttpResponse

def helloworld(request):
    return HttpResponse("Hello World!")

urlpatterns = patterns(
    "",
    url("^$", helloworld)
    )
