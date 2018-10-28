from django.shortcuts import render, redirect
from django.http import HttpResponse
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from myapp.decorators import staff_or_404
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.http import HttpResponseForbidden
from django.http import JsonResponse
import PIL
from .models import *
import pathlib
import uuid
from io import BytesIO
import traceback



@login_required
def add_to_cart(request):
    resp = {
        'success': False,
        'reason': '',
    }
    try:
        data = json.loads(request.body)
        prod = Product.objects.get(id=data['prod_id'])
        cart_filter = Cart.objects.filter(user_id=request.user)
        if cart_filter.count() == 0:
            cart = Cart(user_id=request.user)
            cart.save()
        else:
            cart = cart_filter[0]
        cartobj = CartObjects(cart_id=cart, prod_id=prod, quantity=data['quantity'])
        cartobj.save()
        resp['cartcount'] = CartObjects.objects.filter(cart_id=cart).count()
        resp['success'] = True

    except Exception as e:
        resp['reason'] = traceback.print_exception()
    return JsonResponse(resp)



@login_required
def add_to_waitlist(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)
        prod = Product.objects.get(id=data['prod_id'])
        wl = Waitlist(prod_id=prod, user_id=request.user)
        wl.save()
        resp['success'] = True

    except Exception as e:
        resp['reason'] = traceback.print_exception()
    return JsonResponse(resp)
