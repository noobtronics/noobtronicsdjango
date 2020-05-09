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


def wrap_soup(to_wrap, wrap_in):
    contents = to_wrap.replace_with(wrap_in)
    wrap_in.append(contents)


def add_table_styles(soup):
    tables = soup.findAll('table')

    for table in tables:
        table_cont_tag = soup.new_tag("div")
        table_cont_tag['class'] = 'table-container'
        table['class'] = 'table is-bordered is-narrow is-hoverable'
        wrap_soup(table, table_cont_tag)
    return soup


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
    if 'description' in config:
        prod_obj.description = ' '.join(config['description'])


    if 'tags' in config:
        tags = [x.strip().lower() for x in config['tags'].split(',')]
        prodtag_ids = ProductTag.objects.filter(prod=prod_obj).all().values_list('id', flat=True)
        prodtag_ids = list(prodtag_ids)
        for t in tags:
            tag, is_create = Tag.objects.get_or_create(tag=t)
            prodtag, is_create = ProductTag.objects.get_or_create(tag=tag, prod=prod_obj)
            if prodtag.id in prodtag_ids:
                prodtag_ids.remove(prodtag.id)
        ProductTag.objects.filter(pk__in=prodtag_ids).delete()

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
        prodvar_ids = ProductVariant.objects.filter(prod=prod_obj).values_list('id', flat=True)
        prodvar_ids = list(prodvar_ids)
        count = 0
        for v in variants:
            count += 1
            variant_img = images[int(v['image'])-1]
            variant_img['count'] = int(v['image'])
            prodvar, is_create = ProductVariant.objects.get_or_create(
                prod=prod_obj,
                name=v['name'],
                cardtitle=v['cardtitle'],
                image=json.dumps(variant_img, indent=4),
                price=int(v['price']),
                in_stock= v['in_stock'],
                rank=count,
            )
            if prodvar.id in prodvar_ids:
                prodvar_ids.remove(prodvar.id)
        ProductVariant.objects.filter(pk__in=prodvar_ids).delete()


    soup = add_table_styles(soup)

    prod_obj.markdown=text
    prod_obj.html=str(soup)

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
