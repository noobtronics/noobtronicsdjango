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


RAZORPAY = {
    'key_id': 'rzp_live_yke0EGCry8eh0Q',
    'key_secret': 'RXU23lw9jIvkGgTYh0MDWyUk',
    'callback_url':'https://noobtronics.ltd/cart/razorpay/callback',
    'cancel_url':'https://noobtronics.ltd/cart?status=fail',
}
