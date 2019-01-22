from .settings import *

DEBUG = False


PAYTM["CALLBACK_URL"] = "https://noobtronics.ltd/cart/paytm/callback"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'noobdb',
        'USER': 'noobuser',
        'PASSWORD': '123123',
        'HOST': 'localhost'
    }
}