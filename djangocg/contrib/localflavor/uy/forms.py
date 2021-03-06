# -*- coding: utf-8 -*-
"""
UY-specific form helpers.
"""

from __future__ import absolute_import, unicode_literals

from djangocg.core.validators import EMPTY_VALUES
from djangocg.forms.fields import Select, RegexField
from djangocg.forms import ValidationError
from djangocg.utils.translation import ugettext_lazy as _
from djangocg.contrib.localflavor.uy.util import get_validation_digit


class UYDepartamentSelect(Select):
    """
    A Select widget that uses a list of Uruguayan departaments as its choices.
    """
    def __init__(self, attrs=None):
        from djangocg.contrib.localflavor.uy.uy_departaments import DEPARTAMENT_CHOICES
        super(UYDepartamentSelect, self).__init__(attrs, choices=DEPARTAMENT_CHOICES)


class UYCIField(RegexField):
    """
    A field that validates Uruguayan 'Cedula de identidad' (CI) numbers.
    """
    default_error_messages = {
        'invalid': _("Enter a valid CI number in X.XXX.XXX-X,"
                     "XXXXXXX-X or XXXXXXXX format."),
        'invalid_validation_digit': _("Enter a valid CI number."),
    }

    def __init__(self, *args, **kwargs):
        super(UYCIField, self).__init__(r'(?P<num>(\d{6,7}|(\d\.)?\d{3}\.\d{3}))-?(?P<val>\d)',
                                        *args, **kwargs)

    def clean(self, value):
        """
        Validates format and validation digit.

        The official format is [X.]XXX.XXX-X but usually dots and/or slash are
        omitted so, when validating, those characters are ignored if found in
        the correct place. The three typically used formats are supported:
        [X]XXXXXXX, [X]XXXXXX-X and [X.]XXX.XXX-X.
        """

        value = super(UYCIField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''
        match = self.regex.match(value)
        if not match:
            raise ValidationError(self.error_messages['invalid'])

        number = int(match.group('num').replace('.', ''))
        validation_digit = int(match.group('val'))

        if not validation_digit == get_validation_digit(number):
            raise ValidationError(self.error_messages['invalid_validation_digit'])

        return value
