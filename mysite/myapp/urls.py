from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page),
    path('api/login', login_view),
    path('api/logout', logout_view)
]