
from django.urls import path, include
from orders_app.views import *


urlpatterns = [
    path('api/subscribe_email', add_email_subscriber_api),
]
