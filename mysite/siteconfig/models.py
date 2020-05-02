from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.tag



class Page(models.Model):
    name = models.CharField(max_length = 200, unique=True)
    url = models.CharField(max_length=500, unique=True, blank=True)
    title = models.CharField(max_length = 400, default='', blank=True)
    h1 = models.CharField(max_length = 400, default='', blank=True)
    description = models.CharField(max_length = 500, default='', blank=True)
    keywords = models.CharField(max_length = 400, default='', blank=True)
    config = models.TextField(default='', blank=True)
    is_published = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
