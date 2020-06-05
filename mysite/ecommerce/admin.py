from django.contrib import admin
from django_object_actions import DjangoObjectActions
from django.conf import settings
import markdown
from github import Github
from bs4 import BeautifulSoup
from datetime import datetime
from siteconfig.models import Tag
from ecommerce.models import Category, SubCategory, Product, ProductTag, ProductVariant
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
    text = repo.get_contents("src/products/{0}.md".format(prod_obj.github)).decoded_content.decode()
    urls = prod_obj.github.split('/')

    slug = '/'.join(urls[1:])
    cat_url = urls[0]
    sub_cat_url = urls[1]

    cat_name = cat_url.replace('-',' ').title()
    sub_cat_name = sub_cat_url.replace('-',' ').title()

    cat, is_create = Category.objects.get_or_create(name=cat_name, slug=cat_url)
    sub_cat, is_create = SubCategory.objects.get_or_create(name=sub_cat_name, category=cat, slug=sub_cat_url)

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
    prod_obj.shortname = config.get('shortname', default_value)
    prod_obj.meta_description = config.get('meta_description', default_value)
    prod_obj.keywords = config.get('keywords', default_value)
    prod_obj.sku = urls[-1]
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
    images_data = {}
    images_idlist = []
    for img in images_tags:
        temp = {
            'jpg': img['src'],
            'webp': img['src'].replace('.jpg','.webp'),
            'alt': img['alt'],
            'id': 'img{0}'.format(hash(img['src'])% (10 ** 8)),
        }
        images_data[temp['id']] = temp
        images_idlist.append(temp['id'])
    images = {}
    images['mainimage'] = images_data[images_idlist[0]]
    images['data'] = images_data
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
            variant_img = images_data[images_idlist[int(v['image'])-1]]
            variant_img['count'] = int(v['image'])
            prodvar, is_create = ProductVariant.objects.get_or_create(
                prod=prod_obj,
                name=v['name'],
            )
            prodvar.cardname=v['cardname']
            prodvar.cardtitle=v['cardtitle']
            prodvar.image=json.dumps(variant_img, indent=4)
            prodvar.price=int(v['price'])
            prodvar.in_stock= v['in_stock']
            prodvar.rank=count
            if 'is_shop' in v:
                prodvar.is_shop= v['is_shop']
            prodvar.save()

            if prodvar.id in prodvar_ids:
                prodvar_ids.remove(prodvar.id)
        ProductVariant.objects.filter(pk__in=prodvar_ids).delete()


    soup = add_table_styles(soup)

    prod_obj.markdown=text
    prod_obj.html=str(soup)
    prod_obj.category = cat
    prod_obj.sub_category = sub_cat
    prod_obj.slug = slug

    prod_obj.save()


def download_products():
    g = Github(settings.GITHUB_KEY)
    repo  = g.get_repo("nikhilraut12/noobtronics_media")
    for category in repo.get_dir_contents("src/products"):
        if category.path.endswith('readme.md'):
            continue
        for sub_category in repo.get_dir_contents(category.path):
            if sub_category.path.endswith('readme.md'):
                continue
            for product in repo.get_dir_contents(sub_category.path):
                if product.path.endswith('readme.md'):
                    continue
                prod_url = product.path.replace('src/products/','').replace('.md','')
                prod_obj, is_create = Product.objects.get_or_create(github=prod_url)


def update_products():
    prods = Product.objects.all()
    for prod_obj in prods:
        update_prod_obj(prod_obj)


class ProductAdmin(DjangoObjectActions, admin.ModelAdmin):
    def update_this(self, request, obj):
        update_prod_obj(obj)
    update_this.label = "Update"  # optional
    update_this.short_description = "Update from Github"  # optional
    change_actions = ('update_this', )

    def download_all(modeladmin, request, queryset):
        download_products()
    def update_all(modeladmin, request, queryset):
        update_products()

    changelist_actions = ('download_all', 'update_all')

    list_display = ['name', 'category', 'sub_category','github', 'slug', 'created_at', 'updated_at']


admin.site.register(Product, ProductAdmin)


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'prod']

admin.site.register(ProductTag, ProductTagAdmin)


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['prod', 'name', 'price']

admin.site.register(ProductVariant, ProductVariantAdmin)


def update_category_obj(category_obj):
    g = Github(settings.GITHUB_KEY)
    repo  = g.get_repo("nikhilraut12/noobtronics_media")
    text = repo.get_contents("src/products/{0}/readme.md".format(category_obj.slug)).decoded_content.decode()

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

    category_obj.title = config.get('title', default_value)
    category_obj.meta_description = config.get('meta_description', default_value)
    category_obj.keywords = config.get('keywords', default_value)

    h1 = soup.find('h1')
    category_obj.h1 = h1.text
    h1.decompose()

    soup = add_table_styles(soup)

    category_obj.markdown=text
    category_obj.html=str(soup)

    category_obj.save()


def update_categorys():
    cats = Category.objects.all()
    for cat in cats:
        update_category_obj(cat)


class CategoryAdmin(DjangoObjectActions, admin.ModelAdmin):
    def update_this(self, request, obj):
        update_category_obj(obj)
    update_this.label = "Update"  # optional
    update_this.short_description = "Update from Github"  # optional
    change_actions = ('update_this', )

    def update_all(modeladmin, request, queryset):
        update_categorys()

    changelist_actions = ('update_all',)

    list_display = ['name', 'slug', 'h1', 'title']


admin.site.register(Category, CategoryAdmin)



def update_subcategory_obj(category_obj):
    g = Github(settings.GITHUB_KEY)
    repo  = g.get_repo("nikhilraut12/noobtronics_media")
    text = repo.get_contents("src/products/{0}/{1}/readme.md".format(category_obj.category.slug, category_obj.slug)).decoded_content.decode()

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

    category_obj.title = config.get('title', default_value)
    category_obj.meta_description = config.get('meta_description', default_value)
    category_obj.keywords = config.get('keywords', default_value)

    h1 = soup.find('h1')
    category_obj.h1 = h1.text
    h1.decompose()

    soup = add_table_styles(soup)

    category_obj.markdown=text
    category_obj.html=str(soup)

    category_obj.save()


def update_subcategorys():
    cats = SubCategory.objects.all()
    for cat in cats:
        update_subcategory_obj(cat)



class SubCategoryAdmin(DjangoObjectActions, admin.ModelAdmin):
    def update_this(self, request, obj):
        update_subcategory_obj(obj)
    update_this.label = "Update"  # optional
    update_this.short_description = "Update from Github"  # optional
    change_actions = ('update_this', )

    def update_all(modeladmin, request, queryset):
        update_subcategorys()

    changelist_actions = ('update_all',)

    list_display = ['name', 'slug', 'h1', 'title']


admin.site.register(SubCategory, SubCategoryAdmin)
