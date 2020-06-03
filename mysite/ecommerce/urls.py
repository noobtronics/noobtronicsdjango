from django.urls import path, re_path
from ecommerce.views import *

urlpatterns = [
    path('<slug:category_slug>/<slug:prod_slug>', product_page),
    path('shop', shop_page, name='shop_page'),
    path('', home_page, name='home'),
]
