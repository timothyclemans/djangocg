from djangocg.conf import settings
from djangocg.core.exceptions import ImproperlyConfigured
from djangocg.utils.importlib import import_module

geom_backend = getattr(settings, 'GEOMETRY_BACKEND', 'geos')

try:
    module = import_module('.%s' % geom_backend, 'djangocg.contrib.gis.geometry.backend')
except ImportError:
    try:
        module = import_module(geom_backend)
    except ImportError:
        raise ImproperlyConfigured('Could not import user-defined GEOMETRY_BACKEND '
                                   '"%s".' % geom_backend)

try:
    Geometry = module.Geometry
    GeometryException = module.GeometryException
except AttributeError:
    raise ImproperlyConfigured('Cannot import Geometry from the "%s" '
                               'geometry backend.' % geom_backend)
