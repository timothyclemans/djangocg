from djangocg.db.backends.mysql.base import *
from djangocg.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from djangocg.contrib.gis.db.backends.mysql.creation import MySQLCreation
from djangocg.contrib.gis.db.backends.mysql.introspection import MySQLIntrospection
from djangocg.contrib.gis.db.backends.mysql.operations import MySQLOperations

class DatabaseWrapper(MySQLDatabaseWrapper):

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.creation = MySQLCreation(self)
        self.ops = MySQLOperations(self)
        self.introspection = MySQLIntrospection(self)
