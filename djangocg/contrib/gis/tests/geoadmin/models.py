from djangocg.contrib.gis.db import models
from djangocg.contrib.gis import admin
from djangocg.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(max_length=30)
    point = models.PointField()
    objects = models.GeoManager()
    def __str__(self): return self.name

admin.site.register(City, admin.OSMGeoAdmin)
