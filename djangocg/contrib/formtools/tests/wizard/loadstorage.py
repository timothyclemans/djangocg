from djangocg.test import TestCase

from djangocg.contrib.formtools.wizard.storage import (get_storage,
                                                     MissingStorageModule,
                                                     MissingStorageClass)
from djangocg.contrib.formtools.wizard.storage.base import BaseStorage


class TestLoadStorage(TestCase):
    def test_load_storage(self):
        self.assertEqual(
            type(get_storage('djangocg.contrib.formtools.wizard.storage.base.BaseStorage', 'wizard1')),
            BaseStorage)

    def test_missing_module(self):
        self.assertRaises(MissingStorageModule, get_storage,
            'djangocg.contrib.formtools.wizard.storage.idontexist.IDontExistStorage', 'wizard1')

    def test_missing_class(self):
        self.assertRaises(MissingStorageClass, get_storage,
            'djangocg.contrib.formtools.wizard.storage.base.IDontExistStorage', 'wizard1')

