from djangocg.db.backends.postgresql_psycopg2.base import *
from djangocg.db.backends.postgresql_psycopg2.base import DatabaseWrapper as Psycopg2DatabaseWrapper
from djangocg.contrib.gis.db.backends.postgis.creation import PostGISCreation
from djangocg.contrib.gis.db.backends.postgis.introspection import PostGISIntrospection
from djangocg.contrib.gis.db.backends.postgis.operations import PostGISOperations

class DatabaseWrapper(Psycopg2DatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.creation = PostGISCreation(self)
        self.ops = PostGISOperations(self)
        self.introspection = PostGISIntrospection(self)
