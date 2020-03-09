# Generated by Django 2.1.3 on 2019-04-16 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_auto_20190416_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyWordTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductKeywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('keytag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywordprods', to='products.KeyWordTags')),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywordtags', to='products.Product')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='productkeywords',
            unique_together={('prod_id', 'keytag_id')},
        ),
    ]
