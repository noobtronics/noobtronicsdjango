from django.urls import path
from .views import *
from .admin_views import *


urlpatterns = [
    path('storeadmin', show_storeadmin),
    path('adminapi/add_product', admin_add_product)
    path('adminapi/fetch/product', admin_fetch_product)
]