from django.db import models
from siteconfig.models import Tag


class Product(models.Model):
    slug = models.CharField(max_length=200, unique=True)
    sku = models.CharField(max_length=30, unique=True, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    title = models.TextField(default='', null=True, blank=True)
    meta_description = models.TextField(default='', null=True, blank=True)
    keywords = models.TextField(default='', null=True, blank=True)
    images = models.TextField(default='', null=True, blank=True)

    markdown = models.TextField(default='', null=True, blank=True)
    html = models.TextField(default='', null=True, blank=True)


    rank = models.IntegerField(default=0)
    hide_shop = models.BooleanField(default=False)
    hide_ads = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class ProductTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tagprods")
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tags")

    class Meta:
        constraints = [
                models.UniqueConstraint(fields= ['tag','prod'], name='prod_tag'),
            ]


class ProductVariant(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=300)
    image = models.TextField(default='')
    cardtitle = models.CharField(max_length=200)
    is_main = models.BooleanField(default=False)

    price = models.IntegerField()
    quantity_available = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=False)

    rank = models.IntegerField(default=0)

    class Meta:
        constraints = [
                models.UniqueConstraint(fields= ['prod','name'], name='prod_variant'),
            ]
