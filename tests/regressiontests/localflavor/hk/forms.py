from __future__ import absolute_import

from djangocg.forms import ModelForm

from .models import HKPlace


class HKPlaceForm(ModelForm):

    class Meta:
        model = HKPlace
