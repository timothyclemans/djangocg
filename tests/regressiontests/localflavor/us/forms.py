from __future__ import absolute_import

from djangocg.forms import ModelForm

from .models import USPlace


class USPlaceForm(ModelForm):

    class Meta:
        model = USPlace
