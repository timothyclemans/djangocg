"""
Existing related object instance caching.

Test that queries are not redone when going back through known relations.
"""

from djangocg.db import models

class Tournament(models.Model):
    name = models.CharField(max_length=30)

class Pool(models.Model):
    name = models.CharField(max_length=30)
    tournament = models.ForeignKey(Tournament)

class PoolStyle(models.Model):
    name = models.CharField(max_length=30)
    pool = models.OneToOneField(Pool)

