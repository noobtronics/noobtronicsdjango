from django.contrib import admin
from siteconfig.models import *

class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'title', 'is_published', 'updated','created',)

admin.site.register(Page, PageAdmin)

admin.site.register(Tag)
