from djangocg.contrib.auth.tests.auth_backends import (BackendTest,
    RowlevelBackendTest, AnonymousUserBackendTest, NoBackendsTest,
    InActiveUserBackendTest)
from djangocg.contrib.auth.tests.basic import BasicTestCase
from djangocg.contrib.auth.tests.context_processors import AuthContextProcessorTests
from djangocg.contrib.auth.tests.decorators import LoginRequiredTestCase
from djangocg.contrib.auth.tests.forms import (UserCreationFormTest,
    AuthenticationFormTest, SetPasswordFormTest, PasswordChangeFormTest,
    UserChangeFormTest, PasswordResetFormTest)
from djangocg.contrib.auth.tests.remote_user import (RemoteUserTest,
    RemoteUserNoCreateTest, RemoteUserCustomTest)
from djangocg.contrib.auth.tests.management import (
    GetDefaultUsernameTestCase,
    ChangepasswordManagementCommandTestCase,
)
from djangocg.contrib.auth.tests.models import (ProfileTestCase, NaturalKeysTestCase,
    LoadDataWithoutNaturalKeysTestCase, LoadDataWithNaturalKeysTestCase,
    UserManagerTestCase)
from djangocg.contrib.auth.tests.hashers import TestUtilsHashPass
from djangocg.contrib.auth.tests.signals import SignalTestCase
from djangocg.contrib.auth.tests.tokens import TokenGeneratorTest
from djangocg.contrib.auth.tests.views import (AuthViewNamedURLTests,
    PasswordResetTest, ChangePasswordTest, LoginTest, LogoutTest,
    LoginURLSettings)

# The password for the fixture data users is 'password'
