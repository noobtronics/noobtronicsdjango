from django.contrib import sitemaps
from products.models import *
from datetime import datetime


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

