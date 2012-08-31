from djangocg.db import models
from djangocg.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Artist(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'professional artist'
        verbose_name_plural = 'professional artists'

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('artist_detail', (), {'pk': self.id})

@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Book(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    pages = models.IntegerField()
    authors = models.ManyToManyField(Author)
    pubdate = models.DateField()

    class Meta:
        ordering = ['-pubdate']

    def __str__(self):
        return self.name

class Page(models.Model):
    content = models.TextField()
    template = models.CharField(max_length=300)

class BookSigning(models.Model):
    event_date = models.DateTimeField()
