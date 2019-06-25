from django.contrib import sitemaps
from products.models import *
from django.urls import reverse
from myapp.models import *

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
    protocol = 'https'

    def items(self):
        return ['home', 'shop']

    def location(self, item):
        return reverse(item)


class ShopLinkSitemaps(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return ShopLinks.objects.all()

    def lastmod(self, item):
        return item.created

    def location(self, item):
        return '/shop/'+item.url


class BlogLinkSitemaps(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Blog.objects.filter(is_published=True)

    def lastmod(self, item):
        return item.updated

    def location(self, item):
        return '/blog/'+item.slug


class DownloadsSitemap(sitemaps.Sitemap):
    changefreq = "hourly"
    priority = 0.4
    protocol = 'https'

    def items(self):
        return DownloadsModel.objects.all()

    def lastmod(self, item):
        return item.updated

    def location(self, item):
        return '/download/'+item.slug
