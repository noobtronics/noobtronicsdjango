# Generated by Django 2.1.3 on 2019-06-13 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0030_breadcrumbs_google_product_taxonomy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(default='', max_length=3200),
        ),
    ]
