from django import forms
from djangocg.core import validators
from djangocg.core.exceptions import ValidationError
from djangocg.utils.unittest import TestCase


class TestFieldWithValidators(TestCase):
    def test_all_errors_get_reported(self):
        field = forms.CharField(
            validators=[validators.validate_integer, validators.validate_email]
        )
        self.assertRaises(ValidationError, field.clean, 'not int nor mail')
        try:
            field.clean('not int nor mail')
        except ValidationError as e:
            self.assertEqual(2, len(e.messages))
