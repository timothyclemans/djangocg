from djangocg.core.management.base import CommandError
from djangocg.core.management.templates import TemplateCommand
from djangocg.utils.importlib import import_module
import os

class Command(TemplateCommand):
    help = ("Creates a Django app directory structure for the given app "
            "name in the current directory or optionally in the given "
            "directory.")

    def handle(self, app_name=None, target=None, **options):
        if app_name is None:
            raise CommandError("you must provide an app name")

        # Check that the app_name cannot be imported.
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError("%r conflicts with the name of an existing "
                               "Python module and cannot be used as an app "
                               "name. Please try another name." % app_name)

        # add app to urls.py
        base_dir = os.getcwd()
        project = base_dir[-base_dir[::-1].index('/'):]
        main_urls_path = os.path.join(os.path.join(os.getcwd(), project), 'urls.py')
        f = open(main_urls_path, 'r')
        main_urls_lines = f.readlines()
        f.close()
        for i, line in enumerate(main_urls_lines):
             if line.startswith('urlpatterns = patterns'):
                 start = i
                 break
        for i, line in enumerate(main_urls_lines[start:]):
             if line.startswith(')'):
                 stop = start + i
                 break
        new_url_pattern = "    url(r'^%s/', include('%s.urls')),\n" % (app_name, app_name)
        main_urls_lines.insert(stop, new_url_pattern)
        new_urls = ''.join(main_urls_lines)
        f = open(main_urls_path, 'w')
        f.write(new_urls)
        f.close()

        # ensure there is a templates directory
        projects_templates_dir = os.path.join(base_dir, "templates")
        if not os.path.exists(projects_templates_dir):
            os.makedirs(projects_templates_dir)

        # create directory in templates directory
        os.mkdir(os.path.join(projects_templates_dir, app_name))

        super(Command, self).handle('app', app_name, target, **options)
