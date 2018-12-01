from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'pagetitle', 'price', 'mrp_price', 'quantity_available', 'in_stock', 'is_published')
admin.site.register(Product, ProductAdmin)

admin.site.register(MainImage)
admin.site.register(Image)
admin.site.register(Thumbnail)
admin.site.register(HomePage)


class UserCodeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'code')
    search_fields = ('code',)
admin.site.register(UserCode, UserCodeAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'cart_state', 'created')
    search_fields = ('user_id',)
admin.site.register(Cart, CartAdmin)


admin.site.register(CartObjects)


class WaitlistAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'user_id', 'created')
    search_fields = ('prod_id',)
admin.site.register(Waitlist, WaitlistAdmin)


class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('name','prod_id', 'rank')
    search_fields = ('prod_id',)
admin.site.register(ProductDetails, ProductDetailsAdmin)


admin.site.register(Tags)

class PaytmHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'txn_amount', 'txn_date', 'status')
    search_fields = ('user_id',)

admin.site.register(PaytmHistory, PaytmHistoryAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'order_state')
    search_fields = ('order_id',)
admin.site.register(Orders, OrderAdmin)