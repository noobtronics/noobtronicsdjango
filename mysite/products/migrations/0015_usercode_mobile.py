# Generated by Django 2.1.3 on 2019-02-09 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20190208_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercode',
            name='mobile',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
