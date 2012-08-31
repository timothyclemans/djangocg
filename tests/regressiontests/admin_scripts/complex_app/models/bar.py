from __future__ import absolute_import

from djangocg.db import models

from ..admin import foo


class Bar(models.Model):
    name = models.CharField(max_length=5)
    class Meta:
        app_label = 'complex_app'
