"""
Django Unit Test and Doctest framework.
"""

from djangocg.test.client import Client, RequestFactory
from djangocg.test.testcases import (TestCase, TransactionTestCase,
    SimpleTestCase, LiveServerTestCase, skipIfDBFeature,
    skipUnlessDBFeature)
from djangocg.test.utils import Approximate
