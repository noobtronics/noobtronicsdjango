# Generated by Django 2.2.12 on 2020-05-02 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('siteconfig', '0002_tag'),
        ('ecommerce', '0003_product_productvariant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productvariant',
            old_name='prod_id',
            new_name='prod',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='image_url',
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='image',
            field=models.TextField(default=''),
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='ecommerce.Product')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagprods', to='siteconfig.Tag')),
            ],
            options={
                'unique_together': {('prod', 'tag')},
            },
        ),
    ]
