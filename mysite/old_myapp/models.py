from django.db import models

# Create your models here.
class DownloadsModel(models.Model):
    slug = models.CharField(max_length = 100, unique=True)
    title = models.CharField(max_length=500)
    big_title = models.CharField(max_length=500)
    windows_link = models.CharField(max_length=500)
    ubuntu_link = models.CharField(max_length=500)
    mac_link = models.CharField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug



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
