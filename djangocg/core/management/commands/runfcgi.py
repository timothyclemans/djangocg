from djangocg.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Runs this project as a FastCGI application. Requires flup."
    args = '[various KEY=val options, use `runfcgi help` for help]'

    def handle(self, *args, **options):
        from djangocg.conf import settings
        from djangocg.utils import translation
        # Activate the current language, because it won't get activated later.
        try:
            translation.activate(settings.LANGUAGE_CODE)
        except AttributeError:
            pass
        from djangocg.core.servers.fastcgi import runfastcgi
        runfastcgi(args)
        
    def usage(self, subcommand):
        from djangocg.core.servers.fastcgi import FASTCGI_HELP
        return FASTCGI_HELP
