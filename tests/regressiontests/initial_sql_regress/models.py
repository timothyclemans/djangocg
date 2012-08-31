"""
Regression tests for initial SQL insertion.
"""

from djangocg.db import models


class Simple(models.Model):
    name = models.CharField(max_length = 50)

