from djangocg.conf.urls import patterns, url
from djangocg.contrib.auth import context_processors
from djangocg.contrib.auth.urls import urlpatterns
from djangocg.contrib.auth.views import password_reset
from djangocg.contrib.auth.decorators import login_required
from djangocg.contrib.messages.api import info
from djangocg.http import HttpResponse
from djangocg.shortcuts import render_to_response
from djangocg.template import Template, RequestContext
from djangocg.views.decorators.cache import never_cache

@never_cache
def remote_user_auth_view(request):
    "Dummy view for remote user tests"
    t = Template("Username is {{ user }}.")
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def auth_processor_no_attr_access(request):
    r1 = render_to_response('context_processors/auth_attrs_no_access.html',
        RequestContext(request, {}, processors=[context_processors.auth]))
    # *After* rendering, we check whether the session was accessed
    return render_to_response('context_processors/auth_attrs_test_access.html',
        {'session_accessed':request.session.accessed})

def auth_processor_attr_access(request):
    r1 = render_to_response('context_processors/auth_attrs_access.html',
        RequestContext(request, {}, processors=[context_processors.auth]))
    return render_to_response('context_processors/auth_attrs_test_access.html',
        {'session_accessed':request.session.accessed})

def auth_processor_user(request):
    return render_to_response('context_processors/auth_attrs_user.html',
        RequestContext(request, {}, processors=[context_processors.auth]))

def auth_processor_perms(request):
    return render_to_response('context_processors/auth_attrs_perms.html',
        RequestContext(request, {}, processors=[context_processors.auth]))

def auth_processor_messages(request):
    info(request, "Message 1")
    return render_to_response('context_processors/auth_attrs_messages.html',
         RequestContext(request, {}, processors=[context_processors.auth]))

def userpage(request):
    pass

# special urls for auth test cases
urlpatterns = urlpatterns + patterns('',
    (r'^logout/custom_query/$', 'djangocg.contrib.auth.views.logout', dict(redirect_field_name='follow')),
    (r'^logout/next_page/$', 'djangocg.contrib.auth.views.logout', dict(next_page='/somewhere/')),
    (r'^remote_user/$', remote_user_auth_view),
    (r'^password_reset_from_email/$', 'djangocg.contrib.auth.views.password_reset', dict(from_email='staffmember@example.com')),
    (r'^login_required/$', login_required(password_reset)),
    (r'^login_required_login_url/$', login_required(password_reset, login_url='/somewhere/')),

    (r'^auth_processor_no_attr_access/$', auth_processor_no_attr_access),
    (r'^auth_processor_attr_access/$', auth_processor_attr_access),
    (r'^auth_processor_user/$', auth_processor_user),
    (r'^auth_processor_perms/$', auth_processor_perms),
    (r'^auth_processor_messages/$', auth_processor_messages),
    url(r'^userpage/(.+)/$', userpage, name="userpage"),
)

