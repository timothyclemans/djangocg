"""
The GeoDjango GEOS module.  Please consult the GeoDjango documentation
for more details: 
  http://geodjangocg.org/docs/geos.html
"""
from djangocg.contrib.gis.geos.geometry import GEOSGeometry, wkt_regex, hex_regex
from djangocg.contrib.gis.geos.point import Point
from djangocg.contrib.gis.geos.linestring import LineString, LinearRing
from djangocg.contrib.gis.geos.polygon import Polygon
from djangocg.contrib.gis.geos.collections import GeometryCollection, MultiPoint, MultiLineString, MultiPolygon
from djangocg.contrib.gis.geos.error import GEOSException, GEOSIndexError
from djangocg.contrib.gis.geos.io import WKTReader, WKTWriter, WKBReader, WKBWriter
from djangocg.contrib.gis.geos.factory import fromfile, fromstr
from djangocg.contrib.gis.geos.libgeos import geos_version, geos_version_info, GEOS_PREPARE
