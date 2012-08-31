"""
PT-specific Form helpers
"""
from __future__ import unicode_literals

import re

from djangocg.core.validators import EMPTY_VALUES
from djangocg.forms import ValidationError
from djangocg.forms.fields import Field, RegexField
from djangocg.utils.encoding import smart_text
from djangocg.utils.translation import ugettext_lazy as _

phone_digits_re = re.compile(r'^(\d{9}|(00|\+)\d*)$')


class PTZipCodeField(RegexField):
    default_error_messages = {
        'invalid': _('Enter a zip code in the format XXXX-XXX.'),
    }

    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(PTZipCodeField, self).__init__(r'^(\d{4}-\d{3}|\d{7})$',
            max_length, min_length, *args, **kwargs)

    def clean(self,value):
        cleaned = super(PTZipCodeField, self).clean(value)
        if len(cleaned) == 7:
           return '%s-%s' % (cleaned[:4],cleaned[4:])
        else:
           return cleaned

class PTPhoneNumberField(Field):
    """
    Validate local Portuguese phone number (including international ones)
    It should have 9 digits (may include spaces) or start by 00 or + (international)
    """
    default_error_messages = {
        'invalid': _('Phone numbers must have 9 digits, or start by + or 00.'),
    }

    def clean(self, value):
        super(PTPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''
        value = re.sub('(\.|\s)', '', smart_text(value))
        m = phone_digits_re.search(value)
        if m:
            return '%s' % value
        raise ValidationError(self.error_messages['invalid'])
