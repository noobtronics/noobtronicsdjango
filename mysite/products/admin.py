from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(MainImage)
admin.site.register(Image)
admin.site.register(Thumbnail)
admin.site.register(HomePage)

admin.site.register(UserCode)
admin.site.register(Cart)
admin.site.register(CartObjects)
admin.site.register(Waitlist)


admin.site.register(ProductDetails)

admin.site.register(Tags)