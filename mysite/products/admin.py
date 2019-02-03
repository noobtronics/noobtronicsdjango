from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)


class ReadOnlyAdmin(admin.ModelAdmin):
    # disables edits
    list_display_links = None

    def has_add_permission(self, request):
        # Nobody is allowed to add
        return False

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined')
    ordering = ('-date_joined',)
    search_fields = ('email',)

    # disables edits
    list_display_links = None

    def has_add_permission(self, request):
        # Nobody is allowed to add
        return False

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False
admin.site.register(User, UserAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'pagetitle', 'price', 'mrp_price', 'quantity_available', 'in_stock', 'is_published')
admin.site.register(Product, ProductAdmin)

admin.site.register(MainImage)
admin.site.register(Image)
admin.site.register(Thumbnail)
admin.site.register(HomePage)


class UserCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code')
    readonly_fields = ['email', 'code']
    search_fields = ('code','user_id__email')

    # disables edits
    list_display_links = None

    def has_add_permission(self, request):
        # Nobody is allowed to add
        return False

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False

admin.site.register(UserCode, UserCodeAdmin)



class CartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'cart_state', 'created')
    search_fields = ('user_id',)

    # disables edits
    list_display_links = None

    def has_add_permission(self, request):
        # Nobody is allowed to add
        return False

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False
admin.site.register(Cart, CartAdmin)


admin.site.register(CartObjects, ReadOnlyAdmin)


class WaitlistAdmin(admin.ModelAdmin):
    list_display = ('prod_name', 'prod_title', 'email', 'created')
    search_fields = ('prod_id__name','prod_id__pagetitle', 'user_id__email')
admin.site.register(Waitlist, WaitlistAdmin)


class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('name','prod_id', 'rank')
    search_fields = ('prod_id',)
admin.site.register(ProductDetails, ProductDetailsAdmin)


admin.site.register(Tags)

class PaytmHistoryAdmin(admin.ModelAdmin):
    list_display = ('email', 'txn_amount', 'txn_date', 'status', 'txn_id', 'paytm_orderid')
    search_fields = ('user_id__email',)
    ordering = ('-created',)

    # disables edits
    list_display_links = None

    def has_add_permission(self, request):
        # Nobody is allowed to add
        return False

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False


admin.site.register(PaytmHistory, PaytmHistoryAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'email', 'order_state', 'paymode', 'total_amount', 'state','district', 'mobile')
    search_fields = ('order_id',)
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        editable_fields = ['courier','tracking_no', 'order_state']
        d = [f.name for f in self.model._meta.fields if f.name not in editable_fields]
        return d

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False

admin.site.register(Orders, OrderAdmin)


class SimilarProdAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'sim_id', 'rank')


admin.site.register(SimilarProducts, SimilarProdAdmin)
admin.site.register(RelatedProducts, SimilarProdAdmin)