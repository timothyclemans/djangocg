import warnings
warnings.warn("djangocg.conf.urls.defaults is deprecated; use djangocg.conf.urls instead",
              DeprecationWarning)

from djangocg.conf.urls import (handler403, handler404, handler500,
        include, patterns, url)
