# Generated by Django 2.2.12 on 2020-06-05 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteconfig', '0002_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='url',
            new_name='slug',
        ),
        migrations.RemoveField(
            model_name='page',
            name='config',
        ),
        migrations.RemoveField(
            model_name='page',
            name='description',
        ),
        migrations.AddField(
            model_name='page',
            name='html',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='markdown',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='meta_description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='h1',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='keywords',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
