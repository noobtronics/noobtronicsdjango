# Generated by Django 2.1.3 on 2019-07-27 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0036_blog_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='keywords',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='blog',
            name='name',
            field=models.TextField(),
        ),
    ]
