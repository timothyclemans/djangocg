from __future__ import absolute_import

from djangocg.http import HttpResponse
from djangocg.shortcuts import get_object_or_404

from .models import Person


def get_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    return HttpResponse(person.name)