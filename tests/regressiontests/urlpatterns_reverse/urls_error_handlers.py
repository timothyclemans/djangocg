# Used by the ErrorHandlerResolutionTests test case.

from djangocg.conf.urls import patterns

urlpatterns = patterns('')

handler404 = 'regressiontests.urlpatterns_reverse.views.empty_view'
handler500 = 'regressiontests.urlpatterns_reverse.views.empty_view'
