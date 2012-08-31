from djangocg.db import models


class Article(models.Model):
    text = models.TextField()
