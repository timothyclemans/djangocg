from djangocg.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
