from djangocg.contrib.formtools.tests.wizard.cookiestorage import TestCookieStorage
from djangocg.contrib.formtools.tests.wizard.forms import FormTests, SessionFormTests, CookieFormTests
from djangocg.contrib.formtools.tests.wizard.loadstorage import TestLoadStorage
from djangocg.contrib.formtools.tests.wizard.namedwizardtests.tests import (
    NamedSessionWizardTests,
    NamedCookieWizardTests,
    TestNamedUrlSessionWizardView,
    TestNamedUrlCookieWizardView,
    NamedSessionFormTests,
    NamedCookieFormTests,
)
from djangocg.contrib.formtools.tests.wizard.sessionstorage import TestSessionStorage
from djangocg.contrib.formtools.tests.wizard.wizardtests.tests import (
    SessionWizardTests,
    CookieWizardTests,
    WizardTestKwargs,
    WizardTestGenericViewInterface,
    WizardFormKwargsOverrideTests,
)
