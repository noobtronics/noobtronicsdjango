from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from django.forms import TextInput, Textarea
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple



admin.site.unregister(User)


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.all(),
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance


admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)



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

    def has_change_permission(self, request):
        # Nobody is allowed to add
        return True

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False
admin.site.register(User, UserAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'pagetitle', 'price', 'mrp_price', 'quantity_available', 'in_stock', 'is_published')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})}
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ProductAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description':
            formfield.widget = Textarea(attrs=formfield.widget.attrs)
        return formfield

admin.site.register(Product, ProductAdmin)


class ProductBulletsAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'data', 'rank', 'created')
admin.site.register(ProductBullets, ProductBulletsAdmin)

class ImageDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_url')
admin.site.register(ImageData, ImageDataAdmin)

class MainImageAdmin(admin.ModelAdmin):
    list_display = ('prod_id',)
admin.site.register(MainImage, MainImageAdmin)


admin.site.register(Image)
admin.site.register(Thumbnail)
admin.site.register(HomePage)


class UserCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'mobile', 'ip_data')
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
    list_display = ('user_id', 'cart_state', 'created', 'payment_amount', 'mobile','address_name', 'address1', 'address2', 'district', 'state', 'zipcode', 'ip_data')
    search_fields = ('user_id',)

    # disables edits
    list_display_links = None

    def has_add_permission(self, request):
        # Nobody is allowed to add
        return False

    def has_change_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False
admin.site.register(Cart, CartAdmin)


class CartObjectsAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'prod_id', 'quantity','created')
    def has_add_permission(self, request):
        # Nobody is allowed to add
        return False

    def has_change_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False

admin.site.register(CartObjects, CartObjectsAdmin)


class WaitlistAdmin(admin.ModelAdmin):
    list_display = ('prod_name', 'prod_title', 'email', 'created')
    search_fields = ('prod_id__name','prod_id__pagetitle', 'user_id__email')
admin.site.register(Waitlist, WaitlistAdmin)


class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('name','prod_id', 'rank')
    search_fields = ('prod_id',)
admin.site.register(ProductDetails, ProductDetailsAdmin)


admin.site.register(Tags)

class ProductTagsAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'prod_id')
admin.site.register(ProductTags, ProductTagsAdmin)

class ShopLinksAdmin(admin.ModelAdmin):
    list_display = ('url', 'tag_id')
admin.site.register(ShopLinks, ShopLinksAdmin)

class BreadCrumbsAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(BreadCrumbs, BreadCrumbsAdmin)


class BreadEntryAdmin(admin.ModelAdmin):
    list_display = ('bread_id', 'link_id', 'rank')
admin.site.register(BreadEntry, BreadEntryAdmin)

class KeyWordTagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')
admin.site.register(KeyWordTags, KeyWordTagsAdmin)

class ProductKeywordsAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'keytag_id', 'rank')
admin.site.register(ProductKeywords, ProductKeywordsAdmin)


class ProductLinksAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'link_id', 'rank')
admin.site.register(ProductLinks, ProductLinksAdmin)



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
    list_display = ('order_id', 'email', 'order_state', 'paymode', 'total_amount', 'state','district', 'mobile', 'ip_data')
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


class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'prod_id')
    search_fields = ('order_id',)

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False

admin.site.register(OrderProducts, OrderProductsAdmin)




class SimilarProdAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'sim_id', 'rank')


admin.site.register(SimilarProducts, SimilarProdAdmin)
admin.site.register(RelatedProducts, SimilarProdAdmin)

admin.site.register(ReferalCodes)
admin.site.register(ReferalPriceList)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'created', 'is_published')
admin.site.register(Blog, BlogAdmin)


class BlogPhotoAdmin(admin.ModelAdmin):
    list_display = ('blog_id', 'image', 'created')
admin.site.register(BlogPhotos, BlogPhotoAdmin)


class RazopayIDMapsAdmin(admin.ModelAdmin):
    list_display = ('rp_id', 'order_id', 'created')
admin.site.register(RazopayIDMaps, RazopayIDMapsAdmin)


class RazorpayHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'order_id', 'txn_amount','status', 'txn_date','created')
admin.site.register(RazorpayHistory, RazorpayHistoryAdmin)
