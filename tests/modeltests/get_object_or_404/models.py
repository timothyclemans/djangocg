"""
35. DB-API Shortcuts

``get_object_or_404()`` is a shortcut function to be used in view functions for
performing a ``get()`` lookup and raising a ``Http404`` exception if a
``DoesNotExist`` exception was raised during the ``get()`` call.

``get_list_or_404()`` is a shortcut function to be used in view functions for
performing a ``filter()`` lookup and raising a ``Http404`` exception if a
``DoesNotExist`` exception was raised during the ``filter()`` call.
"""

from djangocg.db import models
from djangocg.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ArticleManager(models.Manager):
    def get_query_set(self):
        return super(ArticleManager, self).get_query_set().filter(authors__name__icontains='sir')

@python_2_unicode_compatible
class Article(models.Model):
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=50)
    objects = models.Manager()
    by_a_sir = ArticleManager()

    def __str__(self):
        return self.title
