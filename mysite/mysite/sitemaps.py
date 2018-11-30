from django.contrib import sitemaps
from products.models import *
from django.urls import reverse


class ProductSitemap(sitemaps.Sitemap):
    changefreq = "hourly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Product.objects.all()

    def lastmod(self, item):
        return item.updated

    def location(self, item):
        return '/product/'+item.slug


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'shop']

    def location(self, item):
        return reverse(item)