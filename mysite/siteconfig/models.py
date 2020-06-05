from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.tag



class Page(models.Model):
    name = models.CharField(max_length = 200, unique=True)
    slug = models.CharField(max_length=500, unique=True, blank=True)

    h1 = models.TextField(default='', null=True, blank=True)
    title = models.TextField(default='', null=True, blank=True)
    meta_description = models.TextField(default='', null=True, blank=True)
    keywords = models.TextField(default='', null=True, blank=True)

    markdown = models.TextField(default='', null=True, blank=True)
    html = models.TextField(default='', null=True, blank=True)

    is_published = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug
