from django.db import models
from siteconfig.models import Tag
import uuid


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True, null=True, blank=True)
    rank = models.IntegerField(default=100)

    def __str__(self):
        return str(self.name)

class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=200, unique=True, null=True, blank=True)
    rank = models.IntegerField(default=100)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    github = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_products', null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subcat_products', null=True, blank=True)
    sku = models.CharField(max_length=30, unique=True, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    shortname = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    title = models.TextField(default='', null=True, blank=True)
    meta_description = models.TextField(default='', null=True, blank=True)
    keywords = models.TextField(default='', null=True, blank=True)
    images = models.TextField(default='', null=True, blank=True)

    markdown = models.TextField(default='', null=True, blank=True)
    html = models.TextField(default='', null=True, blank=True)


    rank = models.IntegerField(default=100)
    hide_shop = models.BooleanField(default=False)
    hide_ads = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.github)


class ProductTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tagprods")
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tags")

    class Meta:
        constraints = [
                models.UniqueConstraint(fields= ['tag','prod'], name='prod_tag'),
            ]


class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=300)
    image = models.TextField(default='')
    cardname = models.CharField(max_length=200, null=True, blank=True)
    cardtitle = models.CharField(max_length=200, null=True, blank=True)
    is_main = models.BooleanField(default=False)

    price = models.IntegerField(null=True, blank=True)
    quantity_available = models.IntegerField(default=0, null=True, blank=True)
    is_shop = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=False)

    rank = models.IntegerField(default=0)

    class Meta:
        constraints = [
                models.UniqueConstraint(fields= ['prod','name'], name='prod_variant'),
            ]
