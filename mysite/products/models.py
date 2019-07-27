from django.db import models
from django.db.models.signals import pre_delete, post_delete, post_save
from django.dispatch import receiver
from pathlib import Path
from django.contrib.auth.models import User
import os
from django.conf import settings


class BreadCrumbs(models.Model):
    name = models.CharField(max_length=200)
    google_product_taxonomy = models.CharField(max_length=400, default='')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    meta_title = models.CharField(max_length=300, default='')
    description = models.CharField(max_length=3200, default='')
    product_head = models.CharField(max_length=70, default='')
    pagetitle = models.CharField(max_length=200)
    cardtitle = models.CharField(max_length=200)
    breadcrumb = models.ForeignKey(BreadCrumbs, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    sku = models.CharField(max_length=8, unique=True)
    price = models.IntegerField()
    mrp_price = models.IntegerField()
    quantity_available = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    rank = models.IntegerField(default=0)
    free_delivery = models.BooleanField(default=False)
    is_google = models.BooleanField(default=False)
    is_amazon = models.BooleanField(default=False)
    amazon_link = models.CharField(max_length=300, default='')
    hide_description = models.BooleanField(default=False)


    def __str__(self):
        return self.name+' | '+self.pagetitle

    def get_absolute_url(self):
        return '/product/'+self.slug




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


class ProductBullets(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prodbullets')
    data = models.CharField(max_length=100)
    rank = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


class ImageData(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='imagesdata')
    img_id = models.OneToOneField(Image, on_delete=models.CASCADE)
    th_home = models.ForeignKey(Thumbnail, on_delete=models.CASCADE, related_name='image_data_home')
    th_mini = models.ForeignKey(Thumbnail, on_delete=models.CASCADE, related_name='image_data_mini')
    th_micro = models.ForeignKey(Thumbnail, on_delete=models.CASCADE, related_name='image_data_micro')
    rank = models.IntegerField()

    def img_url(self):
        return self.th_home.image


class MainImage(models.Model):
    prod_id = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='mainimage')
    img_data = models.ForeignKey(ImageData, on_delete=models.CASCADE)
    thumb_data = models.ForeignKey(ImageData, on_delete=models.CASCADE, related_name='+')




class HomePage(models.Model):
    prod_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    rank = models.IntegerField()


class ReferalCodes(models.Model):
    code = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    referer = models.CharField(max_length=200)
    details = models.CharField(max_length=400)
    is_shipping_free = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)



class Cart(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    cart_state = models.CharField(max_length=3, choices=(
        ('C', 'Cart'),
        ('A', 'Address'),
        ('P', 'Payment'),
        ('D', 'Done'),
    ),default='C')
    address_name = models.CharField(max_length=100, default='')
    address1 = models.CharField(max_length=100, default='')
    address2 = models.CharField(max_length=100, default='')
    district = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    zipcode = models.CharField(max_length=6, default='')
    mobile = models.CharField(max_length=10, default='')
    paymode = models.CharField(max_length=10, choices=(
        ('COD', 'Cash on Delivery'),
        ('PayTM', 'PayTM'),
        ('PayU', 'PayU Money'),
        ('InstaM', 'Instamojo'),
        ('RAZORPAY', 'RAZORPAY')
    ), null=True, blank=True)
    to_be_order_id = models.CharField(max_length=20, blank=True, null=True)
    payment_amount = models.FloatField(default = 0)

    referal_code = models.CharField(max_length=20, default='')
    is_referal_activated = models.BooleanField(default=False)
    referal_obj = models.ForeignKey(ReferalCodes, on_delete=models.SET_NULL, null=True, blank=True, default=None)


    @property
    def pincodedisplay(self):
        pincodedisplay = ''
        if self.zipcode != '':
            zc = ZipCodes.objects.filter(zipcode=self.zipcode)
            if zc.count() > 0:
                zc = zc[0]
                pincodedisplay = '{0}, {1}'.format(zc.district, zc.state)
        return pincodedisplay

    def email(self):
        return self.user_id.email

    def __str__(self):
        return self.user_id.email


class CartObjects(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


class Waitlist(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def email(self):
        return self.user_id.email

    def prod_name(self):
        return self.prod_id.name

    def prod_title(self):
        return self.prod_id.pagetitle



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
    is_standalone = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductTags(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tags, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('prod_id', 'tag_id',)

    def __str__(self):
        return self.prod_id.name + ' ' + self.tag_id.name




class ShopLinks(models.Model):
    url = models.CharField(max_length=100, unique = True)
    name = models.CharField(max_length=100, default='')
    tag_id = models.ForeignKey(Tags, on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=200, default='')
    meta_description = models.CharField(max_length=200, default='')
    breadcrumb = models.ForeignKey(BreadCrumbs, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    rank = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url


class ProductLinks(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shoplinks')
    link_id = models.ForeignKey(ShopLinks, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


class BreadEntry(models.Model):
    bread_id = models.ForeignKey(BreadCrumbs, on_delete=models.CASCADE, related_name='breadentries')
    link_id = models.ForeignKey(ShopLinks, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


class KeyWordTags(models.Model):
    name = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name





class ReferalPriceList(models.Model):
    code_id = models.ForeignKey(ReferalCodes, on_delete=models.CASCADE)
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    moq = models.IntegerField()



class ProductKeywords(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='keywordtags')
    keytag_id =  models.ForeignKey(KeyWordTags, on_delete=models.CASCADE, related_name='keywordprods')
    rank = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('prod_id', 'keytag_id',)


@receiver(post_save, sender=ProductKeywords, dispatch_uid='postsave_keywordtag_signal')
def update_keywordtag_count(sender, instance, using, **kwargs):
    keytag_id = instance.keytag_id
    count = ProductKeywords.objects.filter(keytag_id = keytag_id).count()
    keytag_id.count = count
    keytag_id.save()


class ZipCodes(models.Model):
    zipcode = models.CharField(max_length=6, unique=True)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)



class UserCode(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10, blank=True, default='')

    def email(self):
        return self.user_id.email


class ForgorPWDLink(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    order_id = models.CharField(max_length=20, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    order_state = models.CharField(max_length=3, choices=(
        ('P', 'Processing'),
        ('PS', 'Preparing Shipment'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Cancelled'),
    ), default='P')

    paymode = models.CharField(max_length=10, choices=(
        ('COD', 'Cash on Delivery'),
        ('PayTM', 'PayTM'),
        ('PayU', 'PayU Money'),
        ('InstaM', 'Instamojo'),
    ))
    delivery_charge = models.IntegerField()
    extra_charge = models.IntegerField()
    total_amount = models.IntegerField()

    courier = models.CharField(max_length=100, default='')
    tracking_no = models.CharField(max_length=100, default='')

    address_name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=6)
    mobile = models.CharField(max_length=10)
    email_sent_confirm = models.BooleanField(default=False)
    email_sent_shipped = models.BooleanField(default=False)
    email_sent_delivered = models.BooleanField(default=False)
    referal_code = models.CharField(max_length=20, default='')


    @property
    def pincodedisplay(self):
        return '{0}, {1}'.format(self.district, self.state)

    def email(self):
        return self.user_id.email


class OrderProducts(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='orderprods')
    prod_id = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()

    @property
    def subtotal(self):
        return self.quantity * self.price

class RazopayIDMaps(models.Model):
    rp_id = models.CharField(max_length = 100)
    order_id = models.CharField(max_length = 50)
    created = models.DateTimeField(auto_now_add=True)


class RazorpayHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length = 40)
    txn_amount = models.FloatField()
    txn_date = models.DateTimeField()
    status = models.CharField(max_length = 40)
    details = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class PaytmHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    txn_amount = models.FloatField()
    txn_date = models.DateTimeField()
    txn_id = models.CharField(max_length = 400)
    status = models.CharField(max_length = 40)
    paytm_orderid = models.CharField(max_length = 40)
    order_id = models.CharField(max_length = 40)
    currency = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)


    def email(self):
        return self.user_id.email


class SimilarProducts(models.Model):
    prod_id = models.ForeignKey(Product, related_name='simprods', on_delete=models.CASCADE)
    sim_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')
    rank = models.IntegerField(default=1)


class RelatedProducts(models.Model):
    prod_id = models.ForeignKey(Product, related_name='relprods', on_delete=models.CASCADE)
    sim_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')
    rank = models.IntegerField(default=1)


class Blog(models.Model):
    slug = models.CharField(max_length = 1500, unique=True)
    name = models.TextField()
    keywords = mmodels.TextField(default='')
    markdown = models.TextField()
    html = models.TextField()
    short_html = models.TextField(default='')
    short_markdown = models.TextField(default='')
    description = models.CharField(max_length = 3000, default='')
    rank = models.IntegerField(default=100)
    is_published = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

@receiver(post_delete, sender=Blog, dispatch_uid='delete_blog_signal')
def delete_blog(sender, instance, using, **kwargs):
    media_path = './media/blog/'+instance.slug
    p = Path(media_path)
    if p.exists():
        p.rmdir()


def blogimage_upload_path(instance, filename):
    directory =  'blog/'+instance.blog_id.slug
    os.makedirs(directory, exist_ok=True)
    file_path =  directory+'/'+filename
    if os.path.exists(file_path) and os.path.isfile(file_path):
        raise Exception
    return file_path


class BlogPhotos(models.Model):
    blog_id = models.ForeignKey(Blog, related_name='blogphotos',on_delete=models.CASCADE)
    image = models.ImageField(upload_to=blogimage_upload_path, max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    main_image = models.BooleanField(default=False)


@receiver(pre_delete, sender=BlogPhotos, dispatch_uid='delete_blogimage_signal')
def delete_blog_image(sender, instance, using, **kwargs):
    p = './media/' + instance.image.url
    if os.path.isfile(p):
        os.remove(p)
