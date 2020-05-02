from django.contrib import admin
from .models import *


admin.site.register(DownloadsModel)



class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'title', 'is_published', 'updated','created',)

admin.site.register(Page, PageAdmin)
