import warnings

from djangocg.contrib.gis import geoip
HAS_GEOIP = geoip.HAS_GEOIP
if HAS_GEOIP:
    BaseGeoIP = geoip.GeoIP
    GeoIPException = geoip.GeoIPException

    class GeoIP(BaseGeoIP):
        def __init__(self, *args, **kwargs):
            warnings.warn('GeoIP class has been moved to `djangocg.contrib.gis.geoip`, and '
                          'this shortcut will disappear in Django v1.6.',
                          DeprecationWarning, stacklevel=2)
            super(GeoIP, self).__init__(*args, **kwargs)
