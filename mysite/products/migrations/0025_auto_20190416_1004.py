# Generated by Django 2.1.3 on 2019-04-16 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_auto_20190416_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(default='', max_length=320),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_head',
            field=models.CharField(default='', max_length=70),
        ),
    ]
