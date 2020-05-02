from django.urls import path, re_path
from ecommerce.views import *

urlpatterns = [
    path('arduino-microcontrollers/arduino-uno', product_page),
    path('', home_page, name='home'),
]
