from django.db import models
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from pathlib import Path
from django.contrib.auth.models import User
import os


class Product(models.Model):
    name = models.CharField(max_length=21)
    slug = models.CharField(max_length=100, unique=True)
    pagetitle = models.CharField(max_length=50)
    cardtitle = models.CharField(max_length=24)
    price = models.IntegerField()
    mrp_price = models.IntegerField()
    quantity_available = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=False)
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


class ImageData(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='imagesdata')
    img_id = models.OneToOneField(Image, on_delete=models.CASCADE)
    th_home = models.ForeignKey(Thumbnail, on_delete=models.CASCADE, related_name='image_data_home')
    th_mini = models.ForeignKey(Thumbnail, on_delete=models.CASCADE, related_name='image_data_mini')
    th_micro = models.ForeignKey(Thumbnail, on_delete=models.CASCADE, related_name='image_data_micro')
    rank = models.IntegerField()


class MainImage(models.Model):
    prod_id = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='mainimage')
    img_data = models.ForeignKey(ImageData, on_delete=models.CASCADE)


class HomePage(models.Model):
    prod_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    rank = models.IntegerField()


class Cart(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class CartObjects(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


class Waitlist(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class ProductDetails(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    rank = models.IntegerField()
    name = models.CharField(max_length=50)
    html = models.TextField()


class Tags(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rank = models.IntegerField()
    type = models.CharField(max_length=3, choices=(
        ('M', 'Menu'),
        ('S', 'Section'),
        ('T', 'Tag'),
    ))
