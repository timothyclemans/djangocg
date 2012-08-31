from djangocg.views.generic.base import View, TemplateView, RedirectView
from djangocg.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView,
                                     WeekArchiveView, DayArchiveView, TodayArchiveView,
                                     DateDetailView)
from djangocg.views.generic.detail import DetailView
from djangocg.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from djangocg.views.generic.list import ListView


class GenericViewError(Exception):
    """A problem in a generic view."""
    pass
