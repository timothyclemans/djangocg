from djangocg.conf.urls import patterns
from djangocg.contrib import messages
from djangocg.core.urlresolvers import reverse
from djangocg.http import HttpResponseRedirect, HttpResponse
from djangocg.template import RequestContext, Template
from djangocg.template.response import TemplateResponse
from djangocg.views.decorators.cache import never_cache

TEMPLATE = """{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>
        {{ message }}
    </li>
    {% endfor %}
</ul>
{% endif %}
"""

@never_cache
def add(request, message_type):
    # don't default to False here, because we want to test that it defaults
    # to False if unspecified
    fail_silently = request.POST.get('fail_silently', None)
    for msg in request.POST.getlist('messages'):
        if fail_silently is not None:
            getattr(messages, message_type)(request, msg,
                                            fail_silently=fail_silently)
        else:
            getattr(messages, message_type)(request, msg)

    show_url = reverse('djangocg.contrib.messages.tests.urls.show')
    return HttpResponseRedirect(show_url)

@never_cache
def add_template_response(request, message_type):
    for msg in request.POST.getlist('messages'):
        getattr(messages, message_type)(request, msg)

    show_url = reverse('djangocg.contrib.messages.tests.urls.show_template_response')
    return HttpResponseRedirect(show_url)

@never_cache
def show(request):
    t = Template(TEMPLATE)
    return HttpResponse(t.render(RequestContext(request)))

@never_cache
def show_template_response(request):
    return TemplateResponse(request, Template(TEMPLATE))

urlpatterns = patterns('',
    ('^add/(debug|info|success|warning|error)/$', add),
    ('^show/$', show),
    ('^template_response/add/(debug|info|success|warning|error)/$', add_template_response),
    ('^template_response/show/$', show_template_response),
)
