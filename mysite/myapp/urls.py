from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', home_page, name='home'),
    path('product/<slug:prod_slug>', product_page),
    path('productprint/<slug:prod_slug>', print_product_page),


    re_path(r'shop/(?P<shop_slug>.+)', shop_slug_page),
    path('shop', shop_page, name='shop'),

    path('tags/<slug:tag_slug>', tags_slug_page),
    path('tags', tags_page),


    path('cart', cart_page),
    path('cart/paytm/callback', paytm_callback),
    path('orders', orders_page),
    path('neworder', new_orders_page),
    path('order/<slug:order_id>', order_details_page),
    path('qr/<slug:qrcode>', handle_qr_code),

    path('forgot-password/<slug:code>', forgotpwd_view),

    path('merchant-data.txt', generate_merchant_data),



    path('api/cart/edit_cart', edit_cart),
    path('api/cart/checkout', handle_checkout),
    path('api/cart/pincode', get_pincode_data),
    path('api/cart/address', save_address),
    path('api/cart/paymode', save_paymode),
    path('api/cart/pay', handle_payment),
    path('api/cart/undoaddress', handle_undoaddress),
    path('api/cart/get_paytm_details', get_paytm_details),


    path('api/order/cancel', process_cancel_order),

    path('api/login', login_view),
    path('api/emaillogin', handle_email_login),
    path('api/forgotpwd', handle_forgotpwd),
    path('api/logout', logout_view),
    path('api/legalcontent', serve_legalcontent),
    path('api/deliverycontent', serve_deliverycontent),
    path('api/aboutuscontent', serve_aboutuscontent),
    path('api/paymentcontent', serve_paymentcontent),

    path('api/savemobile', savemobile),

    path('legal/returnpolicy', serve_returnpolicy),
    path('legal/termsandconditions', serve_tandc),
    path('legal/privacypolicy', serve_privacy_policy),
    path('api/fetch/catalog', fetch_catalog),

    path('googlecallback', process_google_callback),
    path('facebookcallback', process_facebook_callback),


    path('download/<slug:name>/', process_download),
    path('downloadl/<slug:name>/', process_download),

    path('master/<slug:name>/', process_master),
]