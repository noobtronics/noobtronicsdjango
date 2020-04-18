from django.contrib import admin
from products.models import UrlHistory

# Register your models here.
class UrlHistoryAdmin(admin.ModelAdmin):
    list_display = ('url', 'mmid', 'csrf_token','referer', 'remote_addr','visited')


admin.site.register(UrlHistory, UrlHistoryAdmin)
