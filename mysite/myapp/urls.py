from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page),
    path('api/login', login_view),
    path('api/logout', logout_view),
    path('api/legalcontent', serve_legalcontent),
    path('legal/returnpolicy', serve_returnpolicy),
    path('legal/termsandconditions', serve_tandc),
    path('legal/privacypolicy', serve_privacy_policy),
]