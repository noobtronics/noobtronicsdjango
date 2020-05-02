# Generated by Django 2.2.12 on 2020-05-02 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('url', models.CharField(blank=True, max_length=500, unique=True)),
                ('title', models.CharField(blank=True, default='', max_length=400)),
                ('h1', models.CharField(blank=True, default='', max_length=400)),
                ('description', models.CharField(blank=True, default='', max_length=500)),
                ('keywords', models.CharField(blank=True, default='', max_length=400)),
                ('config', models.TextField(blank=True, default='')),
                ('is_published', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
