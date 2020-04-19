# Generated by Django 2.2 on 2020-04-19 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('url', models.CharField(max_length=500, unique=True)),
                ('title', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=500)),
                ('keywords', models.CharField(default='', max_length=400)),
                ('config', models.TextField()),
                ('is_published', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]