from __future__ import absolute_import

from djangocg.contrib import admin

from .models import Story


admin.site.register(Story)
raise Exception("Bad admin module")
