from django.urls import path
from .views import *
from .admin_views import *


urlpatterns = [
    path('storeadmin', show_storeadmin),
    path('storeadmin/demohome/<int:prod_id>', show_demo_home),
    path('storeadmin/demoprod/<int:prod_id>', show_demo_prod),
    path('adminapi/add_product', admin_add_product),
    path('adminapi/add_to_home', admin_add_to_home),
    path('adminapi/fetch/products', admin_fetch_product)
]