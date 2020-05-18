from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import *



class UserCustomAdmin(UserAdmin):
    model = User
    list_display = ( 'email','mobile','address1', 'address2', 'city', 'state', 'country',)
    search_fields = ('email','mobile',)
    ordering = ('email','mobile',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        (None, {'fields':('mobile','address1', 'address2', 'city', 'state', 'country')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile','address1', 'address2', 'city', 'state', 'country')}
        ),
    )



admin.site.register(User, UserCustomAdmin)
