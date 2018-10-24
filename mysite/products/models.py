from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from pathlib import Path


class Product(models.Model):
    name = models.CharField(max_length=21)
    slug = models.CharField(max_length=100, unique=True)
    pagetitle = models.CharField(max_length=50)
    cardtitle = models.CharField(max_length=24)
    price = models.IntegerField()
    mrp_price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

@receiver(pre_delete, sender=Product, dispatch_uid='delete_product_signal')
def delete_product(sender, instance, using, **kwargs):
    media_path = 'media/'+instance.slug
    p = Path(media_path)
    if p.exists():
        p.rmdir()


class Image(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)


class Thumbnail(models.Model):
    img_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)


class MainImage(models.Model):
    prod_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    img_id = models.ForeignKey(Image, on_delete=models.CASCADE)

