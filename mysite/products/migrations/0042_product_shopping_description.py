# Generated by Django 2.1.3 on 2019-10-17 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0041_product_hide_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shopping_description',
            field=models.TextField(default=''),
        ),
    ]
