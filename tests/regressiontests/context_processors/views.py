from djangocg.core import context_processors
from djangocg.shortcuts import render_to_response
from djangocg.template.context import RequestContext


def request_processor(request):
    return render_to_response('context_processors/request_attrs.html',
        RequestContext(request, {}, processors=[context_processors.request]))
