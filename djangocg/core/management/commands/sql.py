from __future__ import unicode_literals

from optparse import make_option

from djangocg.core.management.base import AppCommand
from djangocg.core.management.sql import sql_create
from djangocg.db import connections, DEFAULT_DB_ALIAS

class Command(AppCommand):
    help = "Prints the CREATE TABLE SQL statements for the given app name(s)."

    option_list = AppCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to print the '
                'SQL for.  Defaults to the "default" database.'),
    )

    output_transaction = True

    def handle_app(self, app, **options):
        return '\n'.join(sql_create(app, self.style, connections[options.get('database')]))
