"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json
import traceback
from pprint import pprint

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '123456p2ggu#xx_zjy2^5ljg!(3dc%&um@rk$iqf7)3fd#e$af'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'noobtronics.ltd',
    'localhost',
    '*'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_object_actions',
    'lazysignup',
    'django_q',
    'siteconfig',
    'ecommerce',
    'orders_app',
    'seotools',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mysite.mysite_context_processors.webpack_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'noobdb_v2',
        'USER': 'noobuser',
        'PASSWORD': 'noob123',
        'HOST': 'localhost'
    }
}

APP_ENV_PROD = False
if os.environ.get('ENV'):
    if os.environ.get('ENV').startswith("PROD"):
        print("Prod Environment....")
        APP_ENV_PROD = True


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
  'lazysignup.backends.LazySignupBackend',
)



# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/'

STATIC_ROOT = os.path.join(BASE_DIR, "collectstatic")
MEDIA_ROOT = os.path.join(BASE_DIR, "../../noobtronics_media/media")
STORAGE_ROOT = os.path.join(BASE_DIR, "../../noobtronics_media/storage")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

LOGIN_URL = '/login'

GOOGLE_API_CLIENT_ID = '436152518040-289nirmcqqh1dik5409htqhgsrrjr140.apps.googleusercontent.com'

RECAPTCHA_PUBLIC_KEY = '6Lf4QWgUAAAAAKeoRqnrPqyo6bL3hTwhBkR3ml95'
RECAPTCHA_PRIVATE_KEY = '6Lf4QWgUAAAAAF2rn6N8P5f1Z5cWnwXkjJsDaKsu'
NOCAPTCHA = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760




# # Stagging
# PAYTM = {
#     "MID": "LUMINO30908270212107",
#     "CHANNEL_ID": "WEB",
#     "WEBSITE": "WEBSTAGING",
#     "INDUSTRY_TYPE_ID": "Retail",
#     "MERCHANT_KEY": "9bz1jMoShd5bLiQC",
#     "Transaction_URL": "https://securegw-stage.paytm.in/theia/processTransaction",
#     "Status_URL": "https://securegw-stage.paytm.in/merchant-status/getTxnStatus",
#     "CALLBACK_URL": "http://localhost:8000/cart/paytm/callback"
# }



# Production
PAYTM = {
    "MID": "LUMINO65914372097499",
    "CHANNEL_ID": "WEB",
    "WEBSITE": "WEBPROD",
    "INDUSTRY_TYPE_ID": "Retail",
    "MERCHANT_KEY": "dKFylaPL@kSlyIti",
    "Transaction_URL": "https://securegw.paytm.in/theia/processTransaction",
    "Status_URL": "https://securegw.paytm.in/merchant-status/getTxnStatus",
    "CALLBACK_URL": "http://localhost:8000/cart/paytm/callback"
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail14.mymailcheap.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@noobtronics.ltd'
EMAIL_HOST_PASSWORD = 'Nikhil123'



RAZORPAY = {
    'key_id': 'rzp_test_XoQ8s98p900rIr',
    'key_secret': 'AtXZQM8OOjOzjpHcmZZ1VEZk',
    'callback_url':'http://localhost:8000/cart/razorpay/callback',
    'cancel_url':'http://localhost:8000/cart?status=fail',
}



Q_CLUSTER = {
    'name': 'noobtronics',
    'workers': 1,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0, }
}

AUTH_USER_MODEL = 'orders_app.User'
LAZYSIGNUP_USER_MODEL = 'orders_app.User'

GITHUB_KEY = "c046dfbdeeb4b80681b5e86f52b9997d7458fe07"

webpack_js = []
webpack_css = []

try:
    with open('frontend/webpack-stats.json', 'r') as fil:
        webpack_config = json.loads(fil.read())

    #pprint(webpack_config)

    js_list = []
    vuejs = ''
    appjs = ''

    for url in webpack_config['chunks']['app']:
        if url.endswith('.js'):
            if '.vue.' in url:
                url = '/static/dist/' + url
                vuejs = url
            elif '/app.' in url:
                url = '/static/dist/' + url
                appjs = url
            else:
                js_list.append(url)
        if url.endswith('.css'):
            webpack_css.append(url)


    sizes = {}
    for js in js_list:
        path = 'static/dist'+ webpack_config['assets'][js]['publicPath']
        sizes[js] = os.path.getsize(path)


    temp = [vuejs,]
    webpack_js.append(temp)

    counter = 0
    temp = []
    for url in js_list:
        counter += sizes[url]
        url = '/static/dist/' + url
        temp.append(url)
        if counter > 20000:
            webpack_js.append(temp)
            temp = []
            counter = 0
    if len(temp) > 0:
        webpack_js.append(temp)
        temp = []

    temp = [appjs,]
    webpack_js.append(temp)

    #pprint(webpack_js)
    # print(webpack_css)
except:
    traceback.print_exc()
    pass
