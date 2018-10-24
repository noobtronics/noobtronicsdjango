from django.urls import path
from .views import *


urlpatterns = [
    path('storeadmin', show_storeadmin),
    path('adminapi/add_product', admin_add_product)
]