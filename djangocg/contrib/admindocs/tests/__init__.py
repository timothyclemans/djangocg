from __future__ import absolute_import, unicode_literals

from djangocg.contrib.admindocs import views
from djangocg.db.models import fields as builtin_fields
from djangocg.utils import unittest
from djangocg.utils.translation import ugettext as _

from . import fields


class TestFieldType(unittest.TestCase):
    def setUp(self):
        pass

    def test_field_name(self):
        self.assertRaises(AttributeError,
            views.get_readable_field_data_type, "NotAField"
        )

    def test_builtin_fields(self):
        self.assertEqual(
            views.get_readable_field_data_type(builtin_fields.BooleanField()),
            _('Boolean (Either True or False)')
        )

    def test_custom_fields(self):
        self.assertEqual(
            views.get_readable_field_data_type(fields.CustomField()),
            _('A custom field type')
        )
        self.assertEqual(
            views.get_readable_field_data_type(fields.DescriptionLackingField()),
            _('Field of type: %(field_type)s') % {
                'field_type': 'DescriptionLackingField'
            }
        )
