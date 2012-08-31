# Getting the normal admin routines, classes, and `site` instance.
from djangocg.contrib.admin import autodiscover, site, AdminSite, ModelAdmin, StackedInline, TabularInline, HORIZONTAL, VERTICAL

# Geographic admin options classes and widgets.
from djangocg.contrib.gis.admin.options import GeoModelAdmin
from djangocg.contrib.gis.admin.widgets import OpenLayersWidget

try:
    from djangocg.contrib.gis.admin.options import OSMGeoAdmin
    HAS_OSM = True
except ImportError:
    HAS_OSM = False
