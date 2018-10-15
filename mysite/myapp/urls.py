from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page),
    path('login/', login_view),
    path('logout/', logout_view)
]