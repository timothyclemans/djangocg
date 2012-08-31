from djangocg.contrib.auth.models import User
from djangocg.contrib.sites.models import Site
from djangocg.test import TestCase


class SitemapTestsBase(TestCase):
    protocol = 'http'
    domain = 'example.com' if Site._meta.installed else 'testserver'
    urls = 'djangocg.contrib.sitemaps.tests.urls.http'

    def setUp(self):
        self.base_url = '%s://%s' % (self.protocol, self.domain)
        self.old_Site_meta_installed = Site._meta.installed
        # Create a user that will double as sitemap content
        User.objects.create_user('testuser', 'test@example.com', 's3krit')

    def tearDown(self):
        Site._meta.installed = self.old_Site_meta_installed
