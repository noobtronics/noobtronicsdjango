"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from captcha_admin import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from products.models import *

admin.site.site_header = 'Noobtronics Administration'
admin.site.site_title = 'Noobtronics Administration'

product_sitemap = {
    'queryset': Product.objects.filter(is_published=True),
    'date_field': 'updated',
}

sitemaps = {
    'product': GenericSitemap(product_sitemap, priority=1.0),
}



urlpatterns = [
    path('', include('myapp.urls')),
    path('', include('products.urls')),
    path('myadmin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)
