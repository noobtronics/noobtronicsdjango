from django.urls import path, re_path
from api_app.views import *

urlpatterns = [
    path('homepage', homepage_api.as_view()),
]
