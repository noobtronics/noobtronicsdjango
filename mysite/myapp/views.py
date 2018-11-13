from django.shortcuts import render, redirect
from django.http import HttpResponse
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.http import HttpResponseForbidden
from django.http import JsonResponse, Http404
from products.models import *
from products.admin_views import get_cart_qty, process_prod_page, get_alltags_data, get_cart_state
from django.shortcuts import get_list_or_404, get_object_or_404
import math
import traceback


@ensure_csrf_cookie
def home_page(request):
    ps = HomePage.objects.all().order_by('rank')
    data = []
    for p in ps:
        t = {
            'id': p.prod_id.id,
            'name': p.prod_id.name,
            'pagetitle': p.prod_id.pagetitle,
            'price': p.prod_id.price,
            'mrp': p.prod_id.mrp_price,
            'image': p.prod_id.mainimage.img_data.th_home.image.url,
            'slug': p.prod_id.slug
        }
        data.append(t)
    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'cartqty': get_cart_qty(request)
    }
    return render(request, 'home-page.html', context)

@ensure_csrf_cookie
def product_page(request, prod_slug):
    prod = get_object_or_404(Product, slug=prod_slug)
    if prod.is_published:
        return process_prod_page(request, prod.id)
    else:
        raise Http404

def get_prod_data(menu_data, tag_query, page_number):
    last_idx = 0
    for i in menu_data:
        if i > 0:
            last_idx = i
        else:
            break
    if last_idx == 0:
        prods = Product.objects.all().order_by('rank')
    else:
        tag = Tags.objects.get(id=last_idx)
        prodids = set(tag.producttags_set.all().values_list('prod_id__id', flat=True))

        or_tags = []
        for key in tag_query:
            if tag_query[key] != 'true':
                continue
            tg = Tags.objects.get(id=key)
            if tg.is_standalone:
                new_prodids = set(tg.producttags_set.all().values_list('prod_id__id', flat=True))
                prodids = prodids.intersection(new_prodids)
            else:
                or_tags.append(tg)
        or_prod_ids = set()
        for tg in or_tags:
            new_prodids = set(tg.producttags_set.all().values_list('prod_id__id', flat=True))
            or_prod_ids = or_prod_ids.union(new_prodids)
        if len(or_tags) > 0:
            prodids = prodids.intersection(or_prod_ids)
        prods = Product.objects.filter(id__in=prodids).order_by('rank')

    total_count = prods.count()
    total_pages = math.ceil(total_count*1.0/12.0)
    prods = prods[(page_number-1)*12:(page_number)*12]
    data = []
    for prod in prods:
        t = {
            'id': prod.id,
            'name': prod.name,
            'cardtitle': prod.cardtitle,
            'in_stock': 'true' if prod.in_stock else 'false',
            'price': prod.price,
            'slug': prod.slug,
            'mrp': prod.mrp_price,
            'thumb': prod.mainimage.img_data.th_mini.image.url
        }
        data.append(t)
    return data, page_number, total_pages


@ensure_csrf_cookie
def shop_page(request):
    data = {}
    data['tags'] = get_alltags_data()
    data['tags_selected'] = [data['tags']['selected_id'], 0, 0, 0, 0]
    prod_data, page_number, total_pages = get_prod_data(data['tags_selected'], {}, 1)
    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'cartqty': get_cart_qty(request),
        'prod_data': prod_data,
        'total_pages': total_pages,
        'page_number': page_number
    }
    pprint(data)
    return render(request, 'shop-page.html', context)


def get_cart_prods(usr):
    cartprods = []
    cartprods_ids = {}
    subtotal = 0
    count_id = -1
    try:
        cart = Cart.objects.get(user_id=usr)
        cartprodids = cart.cartobjects_set.all().order_by('id')
        for cprod in cartprodids:
            temp = {
                'id': cprod.id,
                'qty': cprod.quantity,
                'title': cprod.prod_id.name,
                'subtitle': cprod.prod_id.pagetitle,
                'img': cprod.prod_id.mainimage.img_data.th_mini.image.url,
                'price': cprod.prod_id.price,
                'slug': cprod.prod_id.slug
            }
            temp['total'] = temp['price']*temp['qty']
            subtotal += temp['total']
            cartprods.append(temp)
            count_id += 1
            cartprods_ids[cprod.id] = count_id
    except:
        None
    return cartprods, cartprods_ids, subtotal


def get_delivery_charge(subtotal):
    delivery_charge = 59
    if subtotal > 200:
        delivery_charge = 49
    if subtotal > 950:
        delivery_charge = 39
    return delivery_charge


def get_cart_extracharge(usr):
    extra_chage = 0
    cart = Cart.objects.get(user_id=usr)
    if cart.paymode == 'COD':
        extra_chage = 31
    return extra_chage


def process_cart_json(usr):
    cartprods, cartprods_ids, subtotal = get_cart_prods(usr)
    data = {
        'cartprods': cartprods,
        'cartprods_ids': cartprods_ids,
        'subtotal': subtotal
    }
    data['deliverycharge'] = get_delivery_charge(data['subtotal'])
    data['extracharge'] = get_cart_extracharge(usr)
    data['total'] = data['subtotal'] + data['deliverycharge'] + data['extracharge']
    return data


@ensure_csrf_cookie
@login_required
def cart_page(request):
    data = {}
    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'cartqty': get_cart_qty(request),
        'state': get_cart_state(request)
    }
    cart_json = process_cart_json(request.user)
    context.update(cart_json)
    return render(request, 'cart-page.html', context)



def login_view(request):
    signed_in = False
    data = json.loads(request.body.decode('utf-8'))
    idinfo = id_token.verify_oauth2_token(data['id_token'], requests.Request(), settings.GOOGLE_API_CLIENT_ID)

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        return HttpResponseForbidden()
    user = User.objects.filter(email=idinfo['email'])
    if not user.exists():
        user = User(email=idinfo['email'], username=idinfo['email'],
                    first_name=idinfo['given_name'],
                    last_name=idinfo['family_name'])
        user.save()
    else:
        user = user[0]
    login(request, user)
    resp = {
        'success': True
    }
    print('login')
    return JsonResponse(resp)


@login_required
def logout_view(request):
    logout(request)
    resp = {
        'success': True
    }
    print('logout')
    return JsonResponse(resp)

@csrf_exempt
def serve_legalcontent(request):
    return render(request, 'legalcontent.html')

@csrf_exempt
def serve_returnpolicy(request):
    return render(request, 'returnpolicy.html')

@csrf_exempt
def serve_tandc(request):
    return render(request, 'termsandconditions.html')

@csrf_exempt
def serve_privacy_policy(request):
    return render(request, 'privacypolicy.html')


def fetch_catalog(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = request.POST.dict()
        menu_data = map(int, data['menu_data'].split(','))
        page_number = int(data['page_number'])
        del data['menu_data']
        del data['page_number']
        prod_data, page_number, total_pages = get_prod_data(menu_data, data, page_number)
        resp['products'] = prod_data
        resp['page_number'] = page_number
        resp['total_pages'] = total_pages
        resp['success'] = True
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)



@login_required
def edit_cart(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)
        action = data['action']
        cp_id = data['cp_id']
        cp = CartObjects.objects.get(id=cp_id)
        if action == 'remove':
            cp.delete()
        elif action == 'increase':
            cp.quantity += 1
            cp.save()
        elif  action == 'decrease':
            if cp.quantity > 1:
                cp.quantity -= 1
                cp.save()
        cart_json = process_cart_json(request.user)
        resp.update(cart_json)
        resp['success'] = True
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)


@login_required
def handle_checkout(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)
        usr_cart = Cart.objects.get(user_id=request.user)
        if data['checkout'] == True:
            usr_cart.cart_state = 'A'
            usr_cart.save()
            resp['success'] = True
        elif data['checkout'] == False:
            usr_cart.cart_state = 'C'
            usr_cart.save()
            resp['success'] = True
        resp['cart_state'] = get_cart_state(request)
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)
