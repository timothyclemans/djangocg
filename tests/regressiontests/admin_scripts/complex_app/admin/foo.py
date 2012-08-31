from __future__ import absolute_import

from djangocg.contrib import admin

from ..models.foo import Foo


admin.site.register(Foo)
