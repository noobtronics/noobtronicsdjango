from django.db import models
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from pathlib import Path
import os


class Product(models.Model):
    name = models.CharField(max_length=21)
    slug = models.CharField(max_length=100, unique=True)
    pagetitle = models.CharField(max_length=50)
    cardtitle = models.CharField(max_length=24)
    price = models.IntegerField()
    mrp_price = models.IntegerField()
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

@receiver(post_delete, sender=Product, dispatch_uid='delete_product_signal')
def delete_product(sender, instance, using, **kwargs):
    media_path = 'media/'+instance.slug
    p = Path(media_path)
    if p.exists():
        p.rmdir()


class Image(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)

@receiver(pre_delete, sender=Image, dispatch_uid='delete_image_signal')
def delete_image(sender, instance, using, **kwargs):
    p = '.' + instance.image.url
    if os.path.isfile(p):
        os.remove(p)


class Thumbnail(models.Model):
    img_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)


@receiver(pre_delete, sender=Thumbnail, dispatch_uid='delete_thumbnail_signal')
def delete_thumbnail(sender, instance, using, **kwargs):
    p = '.' + instance.image.url
    if os.path.isfile(p):
        os.remove(p)


class MainImage(models.Model):
    prod_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    main_img = models.ForeignKey(Image, on_delete=models.CASCADE)
    main_thumb = models.ForeignKey(Thumbnail, on_delete=models.CASCADE)


class HomePage(models.Model):
    prod_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    rank = models.IntegerField()

