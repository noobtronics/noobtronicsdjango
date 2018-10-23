from django.urls import path
from .views import *


urlpatterns = [
    path('storeadmin', show_storeadmin),
]