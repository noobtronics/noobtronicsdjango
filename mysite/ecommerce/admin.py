from django.contrib import admin
from django_object_actions import DjangoObjectActions
from django.conf import settings
import markdown
from github import Github
from bs4 import BeautifulSoup
from datetime import datetime
from siteconfig.models import Tag
from ecommerce.models import Product, ProductTag, ProductVariant
from pprint import pprint
import yaml
import re
import json


def update_prod_obj(prod_obj):
    g = Github(settings.GITHUB_KEY)
    repo  = g.get_repo("nikhilraut12/noobtronics_media")
    text = repo.get_contents("src/products/{0}.md".format(prod_obj.slug)).decoded_content.decode()
    md = markdown.Markdown(extensions=['tables', 'fenced_code'])
    html = md.convert(text)


    soup = BeautifulSoup(html, 'html.parser')

    config = {}

    yamls_html = soup.findAll('code', {'class': 'yaml'})
    yamls = []
    for t in yamls_html:
        yamls.append(t.contents)
        t.parent.decompose()
    for y in yamls:
        config.update(yaml.load(y[0], Loader=yaml.Loader))

    default_value = ''

    prod_obj.title = config.get('title', default_value)
    prod_obj.meta_description = config.get('meta_description', default_value)
    prod_obj.keywords = config.get('keywords', default_value)
    prod_obj.sku = config.get('sku', default_value)
    prod_obj.description = config.get('description', default_value)


    if 'tags' in config:
        tags = [x.strip().lower() for x in config['tags'].split(',')]
        ProductTag.objects.filter(prod=prod_obj).delete()
        for t in tags:
            tag, is_create = Tag.objects.get_or_create(tag=t)
            prodtag, is_create = ProductTag.objects.get_or_create(tag=tag, prod=prod_obj)


    h1 = soup.find('h1')
    prod_obj.name = h1.text
    h1.decompose()

    images_heading = soup.find('h2', text = re.compile('Images*'))
    images_paragraph = images_heading.findNext('p')
    images_tags = images_paragraph.findAll('img')
    images = []
    for img in images_tags:
        temp = {
            'src': img['src'],
            'alt': img['alt']
        }
        images.append(temp)
    prod_obj.images = json.dumps(images, indent=4)
    images_heading.decompose()
    images_paragraph.decompose()


    if 'variants' in config:
        variants = config['variants']
        ProductVariant.objects.filter(prod=prod_obj).delete()
        count = 0
        for v in variants:
            count += 1
            variant_img = images[int(v['image'])-1]
            variant_img['count'] = int(v['image'])
            prodtag, is_create = ProductVariant.objects.get_or_create(
                prod=prod_obj,
                name=v['name'],
                cardtitle=v['cardtitle'],
                image=json.dumps(variant_img, indent=4),
                price=int(v['price']),
                in_stock= v['in_stock'],
                rank=count,
            )

    #
    # images =  soup.findAll("img")
    # if len(images) > 0:
    #     blog_obj.image = images[0]['src']



    # prod_obj.markdown=text
    # prod_obj.html=str(soup)
    prod_obj.save()


class ProductAdmin(DjangoObjectActions, admin.ModelAdmin):
    def update_this(self, request, obj):
        update_prod_obj(obj)
    update_this.label = "Update"  # optional
    update_this.short_description = "Update from Github"  # optional
    change_actions = ('update_this', )

    list_display = ['slug', 'created_at', 'updated_at']

admin.site.register(Product, ProductAdmin)


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'prod']

admin.site.register(ProductTag, ProductTagAdmin)


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['prod', 'name', 'price']

admin.site.register(ProductVariant, ProductVariantAdmin)
