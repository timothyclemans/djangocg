import locale
import traceback

from djangocg.contrib.auth.management.commands import createsuperuser
from djangocg.contrib.auth.models import User, AnonymousUser
from djangocg.core.management import call_command
from djangocg.test import TestCase
from djangocg.utils.six import StringIO


class BasicTestCase(TestCase):
    def test_user(self):
        "Check that users can be created and can set their password"
        u = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        self.assertTrue(u.has_usable_password())
        self.assertFalse(u.check_password('bad'))
        self.assertTrue(u.check_password('testpw'))

        # Check we can manually set an unusable password
        u.set_unusable_password()
        u.save()
        self.assertFalse(u.check_password('testpw'))
        self.assertFalse(u.has_usable_password())
        u.set_password('testpw')
        self.assertTrue(u.check_password('testpw'))
        u.set_password(None)
        self.assertFalse(u.has_usable_password())

        # Check authentication/permissions
        self.assertTrue(u.is_authenticated())
        self.assertFalse(u.is_staff)
        self.assertTrue(u.is_active)
        self.assertFalse(u.is_superuser)

        # Check API-based user creation with no password
        u2 = User.objects.create_user('testuser2', 'test2@example.com')
        self.assertFalse(u.has_usable_password())

    def test_user_no_email(self):
        "Check that users can be created without an email"
        u = User.objects.create_user('testuser1')
        self.assertEqual(u.email, '')

        u2 = User.objects.create_user('testuser2', email='')
        self.assertEqual(u2.email, '')

        u3 = User.objects.create_user('testuser3', email=None)
        self.assertEqual(u3.email, '')

    def test_anonymous_user(self):
        "Check the properties of the anonymous user"
        a = AnonymousUser()
        self.assertEqual(a.pk, None)
        self.assertFalse(a.is_authenticated())
        self.assertFalse(a.is_staff)
        self.assertFalse(a.is_active)
        self.assertFalse(a.is_superuser)
        self.assertEqual(a.groups.all().count(), 0)
        self.assertEqual(a.user_permissions.all().count(), 0)

    def test_superuser(self):
        "Check the creation and properties of a superuser"
        super = User.objects.create_superuser('super', 'super@example.com', 'super')
        self.assertTrue(super.is_superuser)
        self.assertTrue(super.is_active)
        self.assertTrue(super.is_staff)

    def test_createsuperuser_management_command(self):
        "Check the operation of the createsuperuser management command"
        # We can use the management command to create a superuser
        new_io = StringIO()
        call_command("createsuperuser",
            interactive=False,
            username="joe",
            email="joe@somewhere.org",
            stdout=new_io
        )
        command_output = new_io.getvalue().strip()
        self.assertEqual(command_output, 'Superuser created successfully.')
        u = User.objects.get(username="joe")
        self.assertEqual(u.email, 'joe@somewhere.org')

        # created password should be unusable
        self.assertFalse(u.has_usable_password())

        # We can supress output on the management command
        new_io = StringIO()
        call_command("createsuperuser",
            interactive=False,
            username="joe2",
            email="joe2@somewhere.org",
            verbosity=0,
            stdout=new_io
        )
        command_output = new_io.getvalue().strip()
        self.assertEqual(command_output, '')
        u = User.objects.get(username="joe2")
        self.assertEqual(u.email, 'joe2@somewhere.org')
        self.assertFalse(u.has_usable_password())


        new_io = StringIO()
        call_command("createsuperuser",
            interactive=False,
            username="joe+admin@somewhere.org",
            email="joe@somewhere.org",
            stdout=new_io
        )
        u = User.objects.get(username="joe+admin@somewhere.org")
        self.assertEqual(u.email, 'joe@somewhere.org')
        self.assertFalse(u.has_usable_password())

    def test_createsuperuser_nolocale(self):
        """
        Check that createsuperuser does not break when no locale is set. See
        ticket #16017.
        """

        old_getdefaultlocale = locale.getdefaultlocale
        old_getpass = createsuperuser.getpass
        try:
            # Temporarily remove locale information
            locale.getdefaultlocale = lambda: (None, None)

            # Temporarily replace getpass to allow interactive code to be used
            # non-interactively
            class mock_getpass: pass
            mock_getpass.getpass = staticmethod(lambda p=None: "nopasswd")
            createsuperuser.getpass = mock_getpass

            # Call the command in this new environment
            new_io = StringIO()
            call_command("createsuperuser", interactive=True, username="nolocale@somewhere.org", email="nolocale@somewhere.org", stdout=new_io)

        except TypeError as e:
            self.fail("createsuperuser fails if the OS provides no information about the current locale")

        finally:
            # Re-apply locale and getpass information
            createsuperuser.getpass = old_getpass
            locale.getdefaultlocale = old_getdefaultlocale

        # If we were successful, a user should have been created
        u = User.objects.get(username="nolocale@somewhere.org")
        self.assertEqual(u.email, 'nolocale@somewhere.org')