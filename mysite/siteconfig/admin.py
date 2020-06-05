from django.contrib import admin
from siteconfig.models import *
from django_object_actions import DjangoObjectActions
from github import Github
from bs4 import BeautifulSoup
from datetime import datetime
from django.conf import settings
import markdown
import yaml
import re
import json
from ecommerce.admin import add_table_styles



def update_page_obj(page_obj):
    g = Github(settings.GITHUB_KEY)
    repo  = g.get_repo("nikhilraut12/noobtronics_media")
    text = repo.get_contents("src/pages/{0}.md".format(page_obj.name)).decoded_content.decode()

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

    page_obj.title = config.get('title', default_value)
    page_obj.meta_description = config.get('meta_description', default_value)
    page_obj.keywords = config.get('keywords', default_value)

    h1 = soup.find('h1')
    page_obj.h1 = h1.text
    h1.decompose()

    soup = add_table_styles(soup)

    page_obj.markdown=text
    page_obj.html=str(soup)

    page_obj.save()



def update_pages():
    cats = Page.objects.all()
    for cat in cats:
        update_page_obj(cat)


def download_pages():
    g = Github(settings.GITHUB_KEY)
    repo  = g.get_repo("nikhilraut12/noobtronics_media")
    for pg in repo.get_dir_contents("src/pages"):
        if pg.path.endswith('readme.md'):
            continue
        page_name = pg.path.replace('src/pages/','').replace('.md','')
        prod_obj, is_create = Page.objects.get_or_create(name=page_name)




class PageAdmin(DjangoObjectActions, admin.ModelAdmin):
    def update_this(self, request, obj):
        update_page_obj(obj)
    update_this.label = "Update"  # optional
    update_this.short_description = "Update from Github"  # optional
    change_actions = ('update_this', )

    def update_all(modeladmin, request, queryset):
        update_pages()

    def download_all(modeladmin, request, queryset):
        download_pages()

    changelist_actions = ('update_all', 'download_all',)

    list_display = ('name', 'slug', 'title', 'is_published', 'updated','created',)

admin.site.register(Page, PageAdmin)

admin.site.register(Tag)
