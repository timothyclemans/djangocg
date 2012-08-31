from djangocg.test import TestCase

from djangocg.contrib.formtools.tests.wizard.storage import TestStorage
from djangocg.contrib.formtools.wizard.storage.session import SessionStorage


class TestSessionStorage(TestStorage, TestCase):
    def get_storage(self):
        return SessionStorage
