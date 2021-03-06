"""
Regression tests for defer() / only() behavior.
"""

from djangocg.db import models
from djangocg.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Item(models.Model):
    name = models.CharField(max_length=15)
    text = models.TextField(default="xyzzy")
    value = models.IntegerField()
    other_value = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class RelatedItem(models.Model):
    item = models.ForeignKey(Item)

class Child(models.Model):
    name = models.CharField(max_length=10)
    value = models.IntegerField()

@python_2_unicode_compatible
class Leaf(models.Model):
    name = models.CharField(max_length=10)
    child = models.ForeignKey(Child)
    second_child = models.ForeignKey(Child, related_name="other", null=True)
    value = models.IntegerField(default=42)

    def __str__(self):
        return self.name

class ResolveThis(models.Model):
    num = models.FloatField()
    name = models.CharField(max_length=16)

class Proxy(Item):
    class Meta:
        proxy = True

@python_2_unicode_compatible
class SimpleItem(models.Model):
    name = models.CharField(max_length=15)
    value = models.IntegerField()

    def __str__(self):
        return self.name

class Feature(models.Model):
    item = models.ForeignKey(SimpleItem)

class ItemAndSimpleItem(models.Model):
    item = models.ForeignKey(Item)
    simple = models.ForeignKey(SimpleItem)
