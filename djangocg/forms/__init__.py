"""
Django validation and HTML form handling.

TODO:
    Default value for field
    Field labels
    Nestable Forms
    FatalValidationError -- short-circuits all other validators on a form
    ValidationWarning
    "This form field requires foo.js" and form.js_includes()
"""

from __future__ import absolute_import

from djangocg.core.exceptions import ValidationError
from djangocg.forms.fields import *
from djangocg.forms.forms import *
from djangocg.forms.models import *
from djangocg.forms.widgets import *
