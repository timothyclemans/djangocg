import os
from djangocg.conf import settings
from djangocg.contrib.auth.models import AnonymousUser, User
from djangocg.template import Template, Context, TemplateSyntaxError
from djangocg.test import TestCase
from djangocg.test.utils import override_settings


@override_settings(
    MIDDLEWARE_CLASSES=(
        'djangocg.middleware.common.CommonMiddleware',
        'djangocg.contrib.sessions.middleware.SessionMiddleware',
        'djangocg.middleware.csrf.CsrfViewMiddleware',
        'djangocg.contrib.auth.middleware.AuthenticationMiddleware',
        'djangocg.contrib.messages.middleware.MessageMiddleware',
        'djangocg.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    ),
    TEMPLATE_DIRS=(
        os.path.join(os.path.dirname(__file__), 'templates'),
    ),
    SITE_ID=1,
)
class FlatpageTemplateTagTests(TestCase):
    fixtures = ['sample_flatpages']
    urls = 'djangocg.contrib.flatpages.tests.urls'

    def setUp(self):
        self.me = User.objects.create_user('testuser', 'test@example.com', 's3krit')

    def test_get_flatpages_tag(self):
        "The flatpage template tag retrives unregistered prefixed flatpages by default"
        out = Template(
                "{% load flatpages %}"
                "{% get_flatpages as flatpages %}"
                "{% for page in flatpages %}"
                "{{ page.title }},"
                "{% endfor %}"
            ).render(Context())
        self.assertEqual(out, "A Flatpage,A Nested Flatpage,")

    def test_get_flatpages_tag_for_anon_user(self):
        "The flatpage template tag retrives unregistered flatpages for an anonymous user"
        out = Template(
                "{% load flatpages %}"
                "{% get_flatpages for anonuser as flatpages %}"
                "{% for page in flatpages %}"
                "{{ page.title }},"
                "{% endfor %}"
            ).render(Context({
                'anonuser': AnonymousUser()
            }))
        self.assertEqual(out, "A Flatpage,A Nested Flatpage,")

    def test_get_flatpages_tag_for_user(self):
        "The flatpage template tag retrives all flatpages for an authenticated user"
        out = Template(
                "{% load flatpages %}"
                "{% get_flatpages for me as flatpages %}"
                "{% for page in flatpages %}"
                "{{ page.title }},"
                "{% endfor %}"
            ).render(Context({
                'me': self.me
            }))
        self.assertEqual(out, "A Flatpage,A Nested Flatpage,Sekrit Nested Flatpage,Sekrit Flatpage,")

    def test_get_flatpages_with_prefix(self):
        "The flatpage template tag retrives unregistered prefixed flatpages by default"
        out = Template(
                "{% load flatpages %}"
                "{% get_flatpages '/location/' as location_flatpages %}"
                "{% for page in location_flatpages %}"
                "{{ page.title }},"
                "{% endfor %}"
            ).render(Context())
        self.assertEqual(out, "A Nested Flatpage,")

    def test_get_flatpages_with_prefix_for_anon_user(self):
        "The flatpage template tag retrives unregistered prefixed flatpages for an anonymous user"
        out = Template(
                "{% load flatpages %}"
                "{% get_flatpages '/location/' for anonuser as location_flatpages %}"
                "{% for page in location_flatpages %}"
                "{{ page.title }},"
                "{% endfor %}"
            ).render(Context({
                'anonuser': AnonymousUser()
            }))
        self.assertEqual(out, "A Nested Flatpage,")

    def test_get_flatpages_with_prefix_for_user(self):
        "The flatpage template tag retrive prefixed flatpages for an authenticated user"
        out = Template(
                "{% load flatpages %}"
                "{% get_flatpages '/location/' for me as location_flatpages %}"
                "{% for page in location_flatpages %}"
                "{{ page.title }},"
                "{% endfor %}"
            ).render(Context({
                'me': self.me
            }))
        self.assertEqual(out, "A Nested Flatpage,Sekrit Nested Flatpage,")

    def test_get_flatpages_with_variable_prefix(self):
        "The prefix for the flatpage template tag can be a template variable"
        out = Template(
                "{% load flatpages %}"
                "{% get_flatpages location_prefix as location_flatpages %}"
                "{% for page in location_flatpages %}"
                "{{ page.title }},"
                "{% endfor %}"
            ).render(Context({
                'location_prefix': '/location/'
            }))
        self.assertEqual(out, "A Nested Flatpage,")

    def test_parsing_errors(self):
        "There are various ways that the flatpages template tag won't parse"
        render = lambda t: Template(t).render(Context())

        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages %}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages as %}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages cheesecake flatpages %}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages as flatpages asdf%}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages cheesecake user as flatpages %}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages for user as flatpages asdf%}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages prefix for user as flatpages asdf%}")

