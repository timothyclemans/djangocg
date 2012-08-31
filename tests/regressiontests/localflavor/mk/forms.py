from __future__ import absolute_import

from djangocg.forms import ModelForm

from .models import MKPerson


class MKPersonForm(ModelForm):

    class Meta:
        model = MKPerson
