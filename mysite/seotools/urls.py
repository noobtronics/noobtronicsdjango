from django.urls import path, re_path
from seotools.views import *

urlpatterns = [
    re_path(r'striphtml/.*', strip_html),
]