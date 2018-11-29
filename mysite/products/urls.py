from django.urls import path
from .views import *
from .admin_views import *


urlpatterns = [
    path('storeadmin', show_storeadmin),
    path('storeadmin/addtags/<int:prod_id>', show_demo_shop),
    path('storeadmin/demohome/<int:prod_id>', show_demo_home),
    path('storeadmin/demoprod/<int:prod_id>', show_demo_prod),
    path('storeadmin/make_media_backup', handle_media_backup),

    path('adminapi/add/add_prod_tags', admin_add_prod_tags),

    path('adminapi/add_product', admin_add_product),
    path('adminapi/add_product_details', admin_add_product_details),
    path('adminapi/add_to_home', admin_add_to_home),
    path('adminapi/uploadimages', admin_upload_images),
    path('adminapi/fetch/products', admin_fetch_product),
    path('adminapi/fetch/menulist', admin_fetch_menulist),
    path('adminapi/add_menu', admin_add_menu),

    path('api/add/add_to_cart', add_to_cart),
    path('api/add/add_to_waitlist', add_to_waitlist),


]