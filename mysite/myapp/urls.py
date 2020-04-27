from django.urls import path, re_path

from .new_views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('arduino-microcontrollers/arduino-uno', product_page),
]
