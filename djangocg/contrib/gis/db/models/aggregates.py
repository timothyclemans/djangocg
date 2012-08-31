from djangocg.db.models import Aggregate
from djangocg.contrib.gis.db.models.sql import GeomField

class Collect(Aggregate):
    name = 'Collect'

class Extent(Aggregate):
    name = 'Extent'

class Extent3D(Aggregate):
    name = 'Extent3D'

class MakeLine(Aggregate):
    name = 'MakeLine'

class Union(Aggregate):
    name = 'Union'
