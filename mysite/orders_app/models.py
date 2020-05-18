from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from orders_app.managers import CustomUserManager


def generate_uuid():
    return uuid.uuid4().hex


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    mobile = models.CharField(max_length=20, default='')
    token = models.CharField(max_length=100, default=generate_uuid, unique=True)
    address1 = models.CharField(max_length=50, default='')
    address2 = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email





class EmailSubscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    token = models.CharField(max_length=100, default=generate_uuid)
    is_unsubscribed = models.BooleanField(default=False)
    is_invalid = models.BooleanField(default=False)
    is_bounced = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)



class MobileSubscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mobile = models.CharField(max_length=20, default='')
    token = models.CharField(max_length=100, default=generate_uuid)
    is_unsubscribed = models.BooleanField(default=False)
    is_invalid = models.BooleanField(default=False)
    is_bounced = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
