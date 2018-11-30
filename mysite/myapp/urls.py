from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('product/<slug:prod_slug>', product_page),
    path('shop', shop_page, name='shop'),
    path('cart', cart_page),
    path('cart/paytm/callback', paytm_callback),
    path('orders', orders_page),
    path('order/<slug:order_id>', order_details_page),

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
    path('api/logout', logout_view),
    path('api/legalcontent', serve_legalcontent),
    path('api/deliverycontent', serve_deliverycontent),
    path('api/aboutuscontent', serve_aboutuscontent),
    path('api/paymentcontent', serve_paymentcontent),
    path('legal/returnpolicy', serve_returnpolicy),
    path('legal/termsandconditions', serve_tandc),
    path('legal/privacypolicy', serve_privacy_policy),
    path('api/fetch/catalog', fetch_catalog),
]