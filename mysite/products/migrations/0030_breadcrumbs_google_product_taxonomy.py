# Generated by Django 2.1.3 on 2019-06-13 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_auto_20190516_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='breadcrumbs',
            name='google_product_taxonomy',
            field=models.CharField(default='', max_length=400),
        ),
    ]
