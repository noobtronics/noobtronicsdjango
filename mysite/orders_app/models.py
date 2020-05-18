from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from orders_app.managers import CustomUserManager



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    mobile = models.CharField(max_length=20, default='')
    address1 = models.CharField(max_length=50, default='')
    address2 = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
