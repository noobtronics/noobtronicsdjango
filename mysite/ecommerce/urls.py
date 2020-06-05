from django.urls import path, re_path
from ecommerce.views import *

urlpatterns = [
    path('<slug:category_slug>/<slug:prod_slug>', product_page),
    path('shop/<slug:category_slug>', shop_category_page, name='shop_category_page'),
    path('shop', shop_page, name='shop_page'),
    path('', home_page, name='home'),
]
