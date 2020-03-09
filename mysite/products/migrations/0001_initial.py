# Generated by Django 2.2 on 2020-03-09 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=1500, unique=True)),
                ('name', models.TextField()),
                ('keywords', models.TextField(default='')),
                ('markdown', models.TextField()),
                ('html', models.TextField()),
                ('short_html', models.TextField(default='')),
                ('short_markdown', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('rank', models.IntegerField(default=100)),
                ('is_published', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BreadCrumbs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('google_product_taxonomy', models.CharField(default='', max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cart_state', models.CharField(choices=[('C', 'Cart'), ('A', 'Address'), ('P', 'Payment'), ('D', 'Done')], default='C', max_length=3)),
                ('address_name', models.CharField(default='', max_length=100)),
                ('address1', models.CharField(default='', max_length=100)),
                ('address2', models.CharField(default='', max_length=100)),
                ('district', models.CharField(default='', max_length=100)),
                ('state', models.CharField(default='', max_length=100)),
                ('zipcode', models.CharField(default='', max_length=6)),
                ('mobile', models.CharField(default='', max_length=10)),
                ('email_id', models.CharField(default='', max_length=100)),
                ('paymode', models.CharField(blank=True, choices=[('COD', 'Cash on Delivery'), ('PayTM', 'PayTM'), ('PayU', 'PayU Money'), ('InstaM', 'Instamojo'), ('RAZORPAY', 'RAZORPAY')], max_length=10, null=True)),
                ('to_be_order_id', models.CharField(blank=True, max_length=20, null=True)),
                ('payment_amount', models.FloatField(default=0)),
                ('ip_data', models.TextField(blank=True, default='')),
                ('referal_code', models.CharField(default='', max_length=20)),
                ('is_referal_activated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('img_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.Image')),
            ],
        ),
        migrations.CreateModel(
            name='KeyWordTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200, unique=True)),
                ('meta_title', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('shopping_description', models.TextField(default='')),
                ('keywords', models.TextField(default='')),
                ('product_head', models.CharField(default='', max_length=70)),
                ('pagetitle', models.CharField(max_length=200)),
                ('cardtitle', models.CharField(max_length=200)),
                ('sku', models.CharField(max_length=8, unique=True)),
                ('price', models.IntegerField()),
                ('mrp_price', models.IntegerField()),
                ('quantity_available', models.IntegerField(default=0)),
                ('in_stock', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('rank', models.IntegerField(default=0)),
                ('free_delivery', models.BooleanField(default=False)),
                ('is_google', models.BooleanField(default=False)),
                ('is_amazon', models.BooleanField(default=False)),
                ('amazon_link', models.CharField(default='', max_length=300)),
                ('hide_description', models.BooleanField(default=False)),
                ('hide_shop', models.BooleanField(default=False)),
                ('breadcrumb', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.BreadCrumbs')),
            ],
        ),
        migrations.CreateModel(
            name='RazopayIDMaps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rp_id', models.CharField(max_length=100)),
                ('order_id', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReferalCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('referer', models.CharField(max_length=200)),
                ('details', models.CharField(max_length=400)),
                ('is_shipping_free', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ZipCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipcode', models.CharField(max_length=6, unique=True)),
                ('district', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Waitlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('mobile', models.CharField(blank=True, default='', max_length=10)),
                ('ip_data', models.TextField(blank=True, default='')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('img_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Image')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rank', models.IntegerField()),
                ('type', models.CharField(choices=[('M', 'Menu'), ('S', 'Section'), ('T', 'Tag')], max_length=3)),
                ('is_standalone', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Tags')),
            ],
        ),
        migrations.CreateModel(
            name='SimilarProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=1)),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='simprods', to='products.Product')),
                ('sim_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ShopLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(default='', max_length=100)),
                ('meta_title', models.CharField(default='', max_length=200)),
                ('meta_description', models.CharField(default='', max_length=200)),
                ('rank', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('breadcrumb', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.BreadCrumbs')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Tags')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=1)),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relprods', to='products.Product')),
                ('sim_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ReferalPriceList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('moq', models.IntegerField()),
                ('code_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ReferalCodes')),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='RazorpayHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=40)),
                ('txn_amount', models.FloatField()),
                ('txn_date', models.DateTimeField()),
                ('status', models.CharField(max_length=40)),
                ('details', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('link_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ShopLinks')),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoplinks', to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('html', models.TextField()),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductBullets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=100)),
                ('rank', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prodbullets', to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='PaytmHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txn_amount', models.FloatField()),
                ('txn_date', models.DateTimeField()),
                ('txn_id', models.CharField(max_length=400)),
                ('status', models.CharField(max_length=40)),
                ('paytm_orderid', models.CharField(max_length=40)),
                ('order_id', models.CharField(max_length=40)),
                ('currency', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=20, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order_state', models.CharField(choices=[('P', 'Processing'), ('PS', 'Preparing Shipment'), ('S', 'Shipped'), ('D', 'Delivered'), ('C', 'Cancelled')], default='P', max_length=3)),
                ('paymode', models.CharField(choices=[('COD', 'Cash on Delivery'), ('PayTM', 'PayTM'), ('PayU', 'PayU Money'), ('InstaM', 'Instamojo')], max_length=10)),
                ('delivery_charge', models.IntegerField()),
                ('extra_charge', models.IntegerField()),
                ('total_amount', models.IntegerField()),
                ('courier', models.CharField(default='', max_length=100)),
                ('tracking_no', models.CharField(default='', max_length=100)),
                ('address_name', models.CharField(max_length=100)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=6)),
                ('mobile', models.CharField(max_length=10)),
                ('email_id', models.CharField(default='', max_length=100)),
                ('email_sent_confirm', models.BooleanField(default=False)),
                ('email_sent_shipped', models.BooleanField(default=False)),
                ('email_sent_delivered', models.BooleanField(default=False)),
                ('referal_code', models.CharField(default='', max_length=20)),
                ('ip_data', models.TextField(blank=True, default='')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderprods', to='products.Orders')),
                ('prod_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='MainImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ImageData')),
                ('prod_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mainimage', to='products.Product')),
                ('thumb_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='products.ImageData')),
            ],
        ),
        migrations.AddField(
            model_name='imagedata',
            name='prod_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagesdata', to='products.Product'),
        ),
        migrations.AddField(
            model_name='imagedata',
            name='th_home',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_data_home', to='products.Thumbnail'),
        ),
        migrations.AddField(
            model_name='imagedata',
            name='th_micro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_data_micro', to='products.Thumbnail'),
        ),
        migrations.AddField(
            model_name='imagedata',
            name='th_mini',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_data_mini', to='products.Thumbnail'),
        ),
        migrations.AddField(
            model_name='image',
            name='prod_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('prod_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ForgorPWDLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartObjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Cart')),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='referal_obj',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ReferalCodes'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BreadEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bread_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breadentries', to='products.BreadCrumbs')),
                ('link_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ShopLinks')),
            ],
        ),
        migrations.CreateModel(
            name='BlogPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=1000, upload_to=products.models.blogimage_upload_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('main_image', models.BooleanField(default=False)),
                ('blog_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogphotos', to='products.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Tags')),
            ],
            options={
                'unique_together': {('prod_id', 'tag_id')},
            },
        ),
        migrations.CreateModel(
            name='ProductKeywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('keytag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywordprods', to='products.KeyWordTags')),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywordtags', to='products.Product')),
            ],
            options={
                'unique_together': {('prod_id', 'keytag_id')},
            },
        ),
    ]