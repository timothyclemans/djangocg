from djangocg.core.xheaders import populate_xheaders
from djangocg.http import HttpResponse
from djangocg.utils.decorators import decorator_from_middleware
from djangocg.views.generic import View
from djangocg.middleware.doc import XViewMiddleware

from .models import Article

xview_dec = decorator_from_middleware(XViewMiddleware)

def xview(request):
    return HttpResponse()

def xview_xheaders(request, object_id):
    response = HttpResponse()
    populate_xheaders(request, response, Article, 1)
    return response

class XViewClass(View):
    def get(self, request):
        return HttpResponse()
