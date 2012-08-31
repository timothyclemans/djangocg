"""
Colombian-specific form helpers.
"""

from __future__ import absolute_import

from djangocg.contrib.localflavor.co.co_departments import DEPARTMENT_CHOICES
from djangocg.forms.fields import Select


class CODepartmentSelect(Select):
    """
    A Select widget that uses a list of Colombian states as its choices.
    """
    def __init__(self, attrs=None):
        super(CODepartmentSelect, self).__init__(attrs, choices=DEPARTMENT_CHOICES)
