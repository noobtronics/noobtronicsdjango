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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *


admin.site.site_header = 'Noobtronics Administration'
admin.site.site_title = 'Noobtronics Administration'



sitemaps = {
}



urlpatterns = [
    path('convert/', include('lazysignup.urls')),

    path('myadmin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),

    path('seotools/', include('seotools.urls')),

    path('', include('orders_app.urls')),
    path('', include('ecommerce.urls')),

]

if settings.DEBUG:
    urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)
    urlpatterns += static('/storage/', document_root=settings.STORAGE_ROOT)


# handler404 = 'myapp.views.my_http404_view'
# handler500 = 'myapp.views.my_http500_view'
