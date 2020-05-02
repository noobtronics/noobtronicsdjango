from django.contrib import admin
from django_object_actions import DjangoObjectActions
from django.conf import settings
import markdown
from github import Github
from bs4 import BeautifulSoup
from datetime import datetime
from siteconfig.models import Tag
from ecommerce.models import Product, ProductTag, ProductVariant


def update_prod_obj(blog_obj):
    g = Github(settings.GITHUB_KEY)
    repo  = g.get_repo("nikhilraut12/electronicspi_media")
    text = repo.get_contents("src{0}.md".format(blog_obj.slug)).decoded_content.decode()
    md = markdown.Markdown(extensions=['tables', 'meta'])
    html = md.convert(text)
    meta = md.Meta

    if 'title' in meta:
        blog_obj.title = meta['title'][0]
    if 'description' in meta:
        blog_obj.description = meta['description'][0]
    if 'shortinfo' in meta:
        blog_obj.shortinfo = meta['shortinfo'][0]
    if 'keywords' in meta:
        blog_obj.keywords = meta['keywords'][0]

    if 'author' in meta:
        blog_obj.author = meta['author'][0]
    else:
        blog_obj.author = 'Kunal Kashyap'

    if 'created' in meta:
        blog_obj.created_at = datetime.strptime(meta['created'][0],'%Y-%m-%dT%H:%M:%S.%fZ')


    if 'tags' in meta:
        tags = [x.strip().lower() for x in meta['tags'][0].split(',')]
        BlogTags.objects.filter(blog=blog_obj).delete()
        for t in tags:
            tag, is_create = Tag.objects.get_or_create(tag=t)
            blogtag, is_create = BlogTags.objects.get_or_create(tag=tag, blog=blog_obj)



    soup = BeautifulSoup(html, 'html.parser')
    h1 = soup.find('h1')
    blog_obj.heading = h1.text
    h1.decompose()

    images =  soup.findAll("img")
    if len(images) > 0:
        blog_obj.image = images[0]['src']



    blog_obj.markdown=text
    blog_obj.html=str(soup)
    blog_obj.save()


class ProductAdmin(DjangoObjectActions, admin.ModelAdmin):
    def update_this(self, request, obj):
        update_prod_obj(obj)
    update_this.label = "Update"  # optional
    update_this.short_description = "Update from Github"  # optional
    change_actions = ('update_this', )

    list_display = ['slug', 'created_at', 'updated_at']

admin.site.register(Product, ProductAdmin)
