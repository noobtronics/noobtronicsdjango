# Generated by Django 2.1.3 on 2019-06-16 16:03

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_auto_20190613_2300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=1500, unique=True)),
                ('name', models.CharField(max_length=1000)),
                ('markdown', models.TextField()),
                ('html', models.TextField()),
                ('short_html', models.TextField(default='')),
                ('short_markdown', models.TextField(default='')),
                ('description', models.CharField(default='', max_length=3000)),
                ('rank', models.IntegerField(default=100)),
                ('is_published', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=1000, upload_to=products.models.blogimage_upload_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('blog_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogphotos', to='products.Blog')),
            ],
        ),
    ]
