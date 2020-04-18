# Generated by Django 2.2 on 2020-04-18 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=15, unique=True)),
                ('mmid', models.CharField(blank=True, default='', max_length=80)),
                ('location', models.TextField(blank=True, default='')),
                ('country', models.CharField(blank=True, default='', max_length=20)),
                ('state', models.CharField(blank=True, default='', max_length=20)),
                ('city', models.CharField(blank=True, default='', max_length=20)),
            ],
        ),
    ]
