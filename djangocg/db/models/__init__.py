from djangocg.conf import settings
from djangocg.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from djangocg.db import connection
from djangocg.db.models.loading import get_apps, get_app, get_models, get_model, register_models
from djangocg.db.models.query import Q
from djangocg.db.models.expressions import F
from djangocg.db.models.manager import Manager
from djangocg.db.models.base import Model
from djangocg.db.models.aggregates import *
from djangocg.db.models.fields import *
from djangocg.db.models.fields.subclassing import SubfieldBase
from djangocg.db.models.fields.files import FileField, ImageField
from djangocg.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField, ManyToOneRel, ManyToManyRel, OneToOneRel
from djangocg.db.models.deletion import CASCADE, PROTECT, SET, SET_NULL, SET_DEFAULT, DO_NOTHING, ProtectedError
from djangocg.db.models import signals
from djangocg.utils.decorators import wraps


def permalink(func):
    """
    Decorator that calls urlresolvers.reverse() to return a URL using
    parameters returned by the decorated function "func".

    "func" should be a function that returns a tuple in one of the
    following formats:
        (viewname, viewargs)
        (viewname, viewargs, viewkwargs)
    """
    from djangocg.core.urlresolvers import reverse
    @wraps(func)
    def inner(*args, **kwargs):
        bits = func(*args, **kwargs)
        return reverse(bits[0], None, *bits[1:3])
    return inner
