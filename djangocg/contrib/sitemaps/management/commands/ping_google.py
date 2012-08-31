from djangocg.core.management.base import BaseCommand
from djangocg.contrib.sitemaps import ping_google


class Command(BaseCommand):
    help = "Ping Google with an updated sitemap, pass optional url of sitemap"

    def execute(self, *args, **options):
        if len(args) == 1:
            sitemap_url = args[0]
        else:
            sitemap_url = None
        ping_google(sitemap_url=sitemap_url)

