from django.shortcuts import render, redirect
from django.http import HttpResponse
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json
from google.oauth2 import id_token
from google.auth.transport import requests as gog_requests
import google_auth_oauthlib.flow
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.http import JsonResponse, Http404
from products.models import *
from products.admin_views import get_cart_qty, process_prod_page, process_print_prod_page, get_alltags_data, get_cart_state
from django.shortcuts import get_list_or_404, get_object_or_404
import math
import traceback
import random
import time
import pytz
from paytm import Checksum as PaytmChecksum
from django.utils.timezone import make_aware
from datetime import datetime
from django.utils import timezone
from .email_tasks import send_confirm_mail, send_pwdreset_mail
from .models import *
import requests
import facebook
from htmlmin.decorators import minified_response


IST_TZ = pytz.timezone('Asia/Kolkata')


@ensure_csrf_cookie
def home_page(request):
    ps = HomePage.objects.all().order_by('rank')

    require_mobile = 0

    if request.user.is_authenticated:
        if request.user.usercode.mobile == '':
            require_mobile = 1

    browse_links = []
    browse_data = ShopLinks.objects.all().order_by('rank')
    for b in browse_data:
        browse_links.append({
            'url': b.url,
            'name': b.tag_id.name,
        })

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
        'cartqty': get_cart_qty(request),
        'whatsapp_on_mobile': True,
        'require_mobile': require_mobile,
        'browse_links': browse_links
    }
    return render(request, 'home-page.html', context)

@ensure_csrf_cookie
@minified_response
def product_page(request, prod_slug):
    prod = get_object_or_404(Product, slug=prod_slug)
    if prod.is_published:
        return process_prod_page(request, prod.id)
    else:
        raise Http404


@ensure_csrf_cookie
def print_product_page(request, prod_slug):
    prod = get_object_or_404(Product, slug=prod_slug)
    if prod.is_published:
        return process_print_prod_page(request, prod.id)
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
        prods = Product.objects.filter(is_published=True).order_by('rank')
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
                or_tags.append(key)
        or_prod_ids = set()
        for key in or_tags:
            tg = Tags.objects.get(id=key)
            new_prodids = set(tg.producttags_set.all().values_list('prod_id__id', flat=True))
            or_prod_ids = or_prod_ids.union(new_prodids)
        if len(or_tags) > 0:
            prodids = prodids.intersection(or_prod_ids)
        prods = Product.objects.filter(id__in=prodids, is_published=True).order_by('rank')

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
            'thumb': prod.mainimage.thumb_data.th_mini.image.url
        }
        data.append(t)
    return data, page_number, total_pages


@ensure_csrf_cookie
@minified_response
def shop_page(request):
    data = {}
    data['tags'] = get_alltags_data()
    data['tags_selected'] = [0, 0, 0, 0, 0]
    prod_data, page_number, total_pages = get_prod_data(data['tags_selected'], {}, 1)

    require_mobile = 0
    if request.user.is_authenticated:
        if request.user.usercode.mobile == '':
            require_mobile = 1

    browse_links = []
    browse_data = ShopLinks.objects.all().order_by('rank')
    for b in browse_data:
        browse_links.append({
            'url': b.url,
            'name': b.tag_id.name,
        })



    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'cartqty': get_cart_qty(request),
        'prod_data': prod_data,
        'total_pages': total_pages,
        'page_number': page_number,
        'require_mobile': require_mobile,
        'whatsapp_on_mobile': True,
        'browse_links': browse_links,
        'meta_title': 'Noobtronics Shop: Microcontrollers, Sensors, Modules, Electronic Hobby Kits | India',
        'meta_description': 'Our product offerings include Microcontroller Boards, All types of Sensors, Modules, Development Boards and Kits required for any Electronic Project'
    }
    return render(request, 'shop-page.html', context)


def get_parent_taglist(tag):
    output = []
    output.append(tag.id)
    while tag.parent is not None:
        tag = tag.parent
        output.append(tag.id)
    output = output[::-1]
    output.extend([0,0,0,0,0])
    return output[:5]


@ensure_csrf_cookie
@minified_response
def shop_slug_page(request, shop_slug):
    shop_link = get_object_or_404(ShopLinks, url=shop_slug)
    data = {}
    data['tags'] = get_alltags_data()
    data['tags_selected'] = get_parent_taglist(shop_link.tag_id)
    prod_data, page_number, total_pages = get_prod_data(data['tags_selected'], {}, 1)

    require_mobile = 0
    if request.user.is_authenticated:
        if request.user.usercode.mobile == '':
            require_mobile = 1

    browse_links = []
    browse_data = ShopLinks.objects.all().order_by('rank')
    for b in browse_data:
        browse_links.append({
            'url': b.url,
            'name': b.tag_id.name,
        })

    breadcrumbs = []
    if shop_link.breadcrumb:
        breads = shop_link.breadcrumb.breadentries.order_by('rank')
        for bread_entry in breads:
            temp = {
                'name': bread_entry.link_id.name,
                'url': bread_entry.link_id.url,
            }
            breadcrumbs.append(temp)

    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'cartqty': get_cart_qty(request),
        'prod_data': prod_data,
        'total_pages': total_pages,
        'page_number': page_number,
        'require_mobile': require_mobile,
        'whatsapp_on_mobile': True,
        'browse_links': browse_links,

        'meta_title': shop_link.meta_title,
        'meta_description': shop_link.meta_description,

        'breadcrumbs': breadcrumbs
    }
    return render(request, 'shop-page.html', context)


@ensure_csrf_cookie
@minified_response
def tags_page(request):

    tags_data = KeyWordTags.objects.all().order_by('name')

    tags_list = []
    for t in tags_data:
        temp = {
            'name': t.name,
            'count': t.count
        }
        tags_list.append(temp)

    context = {
        'loggedin': request.user.is_authenticated,
        'tags_list': tags_list,
        'cartqty': get_cart_qty(request),
        'whatsapp_on_mobile': True,
    }
    return render(request, 'all-tags-page.html', context)


@ensure_csrf_cookie
@minified_response
def tags_slug_page(request, tag_slug):
    keywordtag = get_object_or_404(KeyWordTags, name=tag_slug)
    data = {}

    prodids = keywordtag.keywordprods.all().values_list('prod_id__id', flat=True)
    prod_data = []
    for prod_id in prodids:
        prod = Product.objects.get(id=prod_id)
        t = {
            'id': prod.id,
            'name': prod.name,
            'cardtitle': prod.cardtitle,
            'in_stock': 'true' if prod.in_stock else 'false',
            'price': prod.price,
            'slug': prod.slug,
            'mrp': prod.mrp_price,
            'thumb': prod.mainimage.thumb_data.th_mini.image.url
        }
        prod_data.append(t)


    require_mobile = 0
    if request.user.is_authenticated:
        if request.user.usercode.mobile == '':
            require_mobile = 1


    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'cartqty': get_cart_qty(request),
        'prod_data': prod_data,
        'require_mobile': require_mobile,
        'whatsapp_on_mobile': True,
        'tag_name': keywordtag.name
    }
    return render(request, 'tag-shop-page.html', context)




def get_cart_prods(usr):
    cartprods = []
    cartprods_ids = {}
    subtotal = 0
    count_id = -1
    free_delivery = False
    try:
        cart = Cart.objects.get(user_id=usr)
        cartprodids = cart.cartobjects_set.all().order_by('id')

        prod_id_counts = {}
        for cprod in cartprodids:
            temp_id = cprod.prod_id.id
            if temp_id not in prod_id_counts:
                prod_id_counts[temp_id] = 0
            prod_id_counts[temp_id] += cprod.quantity

        special_price = {}

        if cart.is_referal_activated:
            referal_list = ReferalPriceList.objects.filter(code_id=cart.referal_obj)
            for obj in referal_list:
                if obj.prod_id.id in prod_id_counts:
                    if obj.moq <=  prod_id_counts[obj.prod_id.id]:
                        special_price[obj.prod_id.id] = obj.price


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
            if cprod.prod_id.id in special_price:
                temp['price'] = special_price[cprod.prod_id.id]
            temp['total'] = temp['price']*temp['qty']
            subtotal += temp['total']
            cartprods.append(temp)
            count_id += 1
            cartprods_ids[cprod.id] = count_id
            if cprod.prod_id.free_delivery:
                free_delivery = True

            if len(special_price) > 0:
                if cart.referal_obj.is_shipping_free:
                    free_delivery = True
    except:
        None
    return cartprods, cartprods_ids, subtotal, free_delivery


def get_delivery_charge(subtotal):
    delivery_charge = 50
    return delivery_charge


def get_cart_extracharge(usr):
    extra_chage = 0
    cart = Cart.objects.get(user_id=usr)
    if cart.paymode == 'COD':
        extra_chage = 75
    return extra_chage


def process_cart_json(usr):
    cartprods, cartprods_ids, subtotal, free_delivery = get_cart_prods(usr)
    data = {
        'cartprods': cartprods,
        'cartprods_ids': cartprods_ids,
        'subtotal': subtotal
    }

    if not free_delivery:
        data['deliverycharge'] = get_delivery_charge(data['subtotal'])
    else:
        data['deliverycharge'] = 0
    data['extracharge'] = get_cart_extracharge(usr)
    data['total'] = data['subtotal'] + data['deliverycharge'] + data['extracharge']


    return data


@ensure_csrf_cookie
@login_required
def cart_page(request):
    data = {}

    cart = get_object_or_404(Cart, user_id=request.user)
    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'state': get_cart_state(request),
        'whatsapp_on_mobile': False
    }

    cart_json = process_cart_json(request.user)
    context.update(cart_json)

    show_payment_failed = False
    txn_status = request.GET.get('status')
    if txn_status == 'fail':
        show_payment_failed = True
    context['show_payment_failed'] = show_payment_failed

    done_order_id = ''
    if txn_status == 'success':
        paymode = request.GET.get('mode')
        if paymode == 'paytm':
            done_order_id = finalize_paytm_payment(request.user)

    context['done_order_id'] = done_order_id
    context['cartqty'] = get_cart_qty(request)
    return render(request, 'cart-page.html', context)



def finalize_paytm_payment(usr):
    verified = False
    try:
        cart = Cart.objects.get(user_id = usr)
        order_id = cart.to_be_order_id
        paytm_hist = PaytmHistory.objects.filter(user_id=usr, order_id=order_id, status='TXN_SUCCESS')
        if paytm_hist.count() > 0:
            verified = True
    except:
        pass
    if verified:
        return add_cart_to_order(usr)
    return ''



def login_view(request):
    resp = {
        'success': False
    }
    signed_in = False
    data = json.loads(request.body.decode('utf-8'))
    idinfo = id_token.verify_oauth2_token(data['id_token'], gog_requests.Request(), settings.GOOGLE_API_CLIENT_ID)

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

    user_code = get_user_code(user)
    if not user_code:
        return JsonResponse(resp)

    login(request, user)
    resp['success'] = True
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
def serve_deliverycontent(request):
    return render(request, 'deliverycontent.html')


@csrf_exempt
def serve_aboutuscontent(request):
    return render(request, 'aboutuscontent.html')


@csrf_exempt
def serve_paymentcontent(request):
    return render(request, 'paymentcontent.html')

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


def get_address_data(usr):
    data = {
        'name': '',
        'mobile': '',
        'address1': '',
        'address2': '',
        'pincode': '',
        'pincodedisplay': ''
    }
    try:
        cart = Cart.objects.filter(user_id=usr)
        if cart.count() > 0:
            cart = cart[0]
            data['name'] = cart.address_name
            data['mobile'] = cart.mobile
            data['address1'] = cart.address1
            data['address2'] = cart.address2
            data['pincode'] = cart.zipcode
            data['pincodedisplay'] = cart.pincodedisplay
    except:
        pass
    return data


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
        address_data = get_address_data(request.user)
        resp.update(address_data)
        resp['cart_state'] = get_cart_state(request)
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)



@login_required
def get_pincode_data(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)
        zc = ZipCodes.objects.get(zipcode=data['pincode'])
        resp['pincodedisplay'] = '{0}, {1}'.format(zc.district, zc.state)
        resp['success'] = True
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)


@login_required
def save_address(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)
        zc = ZipCodes.objects.get(zipcode=data['pincode'])
        cart = Cart.objects.get(user_id=request.user)
        cart.address_name = data['name']
        cart.mobile = data['mobile']
        cart.address1 = data['address1']
        cart.address2 = data['address2']
        cart.zipcode = data['pincode']
        cart.district = zc.district
        cart.state = zc.state
        cart.save()
        cart.cart_state = 'P'
        cart.save()
        resp['success'] = True
        resp['cart_state'] = get_cart_state(request)
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)


@login_required
def save_paymode(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)
        cart = Cart.objects.get(user_id=request.user)
        paymode = data['paymode']
        if paymode == 'cod':
            cart.paymode = 'COD'
            cart.save()
        elif paymode == 'paytm':
            cart.paymode = 'PayTM'
            cart.save()
        elif paymode == 'payu':
            cart.paymode = 'PayU'
            cart.save()
        elif paymode == 'instamojo':
            cart.paymode = 'InstaM'
            cart.save()
        elif paymode == '':
            cart.paymode = ''
            cart.save()
        else:
            paymode = ''
        cart_json = process_cart_json(request.user)
        resp.update(cart_json)
        resp['paymode'] = paymode
        resp['success'] = True
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)



@login_required
def handle_undoaddress(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)
        cart = Cart.objects.get(user_id=request.user)
        if data['address'] == False:
            cart.cart_state = 'A'
            cart.save()
            address_data = get_address_data(request.user)
            resp.update(address_data)
            resp['cart_state'] = get_cart_state(request)
            resp['success'] = True
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)


def get_rand_number(n):
    n = int(n)
    random.seed(int(time.time()*100)+random.randint(1,100))
    num = random.randint(10**n, 10**(n+1)-1)
    return str(num)


def get_user_code(usr):
    found_code = None
    try:
        uc = UserCode.objects.filter(user_id=usr)
        if uc.count() > 0:
            found_code = uc[0].code
        else:
            found_uniq = False
            while not found_uniq:
                code = get_rand_number(6)
                uc = UserCode.objects.filter(code=code)
                if uc.count() == 0:
                    found_uniq = True
                    uc = UserCode(user_id = usr, code=code)
                    uc.save()
                    found_code = uc.code
    except Exception as e:
        print(traceback.format_exc())
        pass
    return found_code


def generate_order_id(usr):
    found_uniq = False
    found_order_id = None
    user_code = get_user_code(usr)
    while not found_uniq:
        prefix = get_rand_number(4)
        order_id = prefix+user_code
        oc = Orders.objects.filter(user_id = usr, order_id=order_id)
        if oc.count() == 0:
            found_uniq = True
            found_order_id = order_id
    return found_order_id



def add_cart_to_order(usr):
    cart = Cart.objects.get(user_id=usr)
    if cart.to_be_order_id == '' or cart.to_be_order_id is None:
        order_id = generate_order_id(usr)
    else:
        order_id = cart.to_be_order_id

    temp_data = process_cart_json(usr)
    delivery_charge = temp_data['deliverycharge']
    extra_charge = temp_data['extracharge']

    _, _, subtotal, _ = get_cart_prods(usr)

    total = subtotal + delivery_charge + extra_charge

    success = False
    try:
        ordr = Orders(order_id=order_id, user_id=usr,
                      paymode=cart.paymode, delivery_charge=delivery_charge,
                      extra_charge=extra_charge, total_amount=total,
                      address_name=cart.address_name,address1=cart.address1,
                      address2=cart.address2,district=cart.district, state=cart.state,
                      zipcode=cart.zipcode,mobile=cart.mobile
                      )
        ordr.save()
        if cart.is_referal_activated:
            ordr.referal_code = cart.referal_code
            ordr.save()

        cartobjs = cart.cartobjects_set.all().order_by('id')
        for cartobj in cartobjs:
            ordr_prd = OrderProducts(order_id=ordr, prod_id=cartobj.prod_id,
                                     quantity=cartobj.quantity,
                                     price=cartobj.prod_id.price)
            ordr_prd.save()
        cart.delete()

        send_confirm_mail(ordr.id)
        success = True
    except Exception as e:
        print(traceback.format_exc())
        pass

    if success:
        return order_id
    return


def get_order_data(order_id):
    data = {}
    try:
        ordr = Orders.objects.get(order_id=order_id)
        ordr_prods = ordr.orderprods.all().order_by('id')
    except Exception as e:
        print(traceback.format_exc())
        pass
    return data


@login_required
def handle_payment(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)
        paymode = data['paymode']
        if paymode == 'cod':
            order_id = add_cart_to_order(request.user)
            if order_id:
                order_data = get_order_data(order_id)
                resp.update(order_data)
                resp['cartqty'] = get_cart_qty(request)
                resp['cart_state'] = 3
                resp['success'] = True
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)


@login_required
def process_referral_code(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        cart = Cart.objects.get(user_id=request.user)
        data = json.loads(request.body)
        code = data['code'].upper()
        code_list = ReferalCodes.objects.filter(code=code, is_active=True)
        if code_list.count() == 0:
            return JsonResponse(resp)
        code_activated = code_list[0]
        cart.is_referal_activated = True
        cart.referal_code = code
        cart.referal_obj = code_activated
        cart.save()
        resp['referrer'] = code_activated.referer
        resp['referrer_details'] = code_activated.details
        cart_json = process_cart_json(request.user)
        resp.update(cart_json)
        resp['success'] = True

    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)



@login_required
def new_orders_page(request):
    order_data = []

    ordr = Orders.objects.filter(user_id=request.user).order_by('-id')[0]
    
    if ordr.order_state == 'P':
        if (timezone.now() - ordr.created).total_seconds() < 1800:
            return orders_page(request)

    return HttpResponseRedirect('/orders')



def handle_qr_code(request, qrcode):
    try:
        prod = Product.objects.filter(sku = qrcode)[0]
        return HttpResponseRedirect('/product/'+prod.slug)
    except:
        pass
    return HttpResponseRedirect('/')



@login_required
def orders_page(request):
    order_data = []

    ordrs = Orders.objects.filter(user_id=request.user).order_by('-id')[:50]

    for ordr in ordrs:
        temp = {
            'order_id': ordr.order_id,
            'order_time': ordr.created.astimezone(IST_TZ).strftime('%d %b %Y %I:%M%p'),
            'amount': ordr.total_amount,
            'status': ordr.get_order_state_display()
        }
        prod_data = []
        ord_prds = ordr.orderprods.all().order_by('id')
        for ord_prd in ord_prds:
            t = {
                'img': '',
                'title': '',
                'subtitle': '',
                'slug': '',
                'qty': ord_prd.quantity,
                'price': ord_prd.price
            }
            try:
                if ord_prd.prod_id:
                    t['img'] = ord_prd.prod_id.mainimage.img_data.th_mini.image.url
                    t['title'] = ord_prd.prod_id.name
                    t['subtitle'] = ord_prd.prod_id.pagetitle
                    t['slug'] = ord_prd.prod_id.slug
            except:
                pass
            prod_data.append(t)
        temp['prod_data'] = prod_data
        order_data.append(temp)

    order_data = order_data
    context = {
        'loggedin': request.user.is_authenticated,
        'cartqty': get_cart_qty(request),
        'order_data': order_data
    }
    return render(request, 'orders-page.html', context)


@login_required
def process_cancel_order(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)
        order_id = data['order_id']
        ordr = Orders.objects.get(user_id=request.user, order_id=order_id)
        if ordr.order_state == 'P':
            ordr.order_state = 'C'
            ordr.save()
            resp['success'] = True
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)


def get_order_state_num(order_state):
    if order_state == 'P':
        return 0
    elif order_state == 'PS':
        return 1
    elif order_state == 'S':
        return 2
    elif order_state == 'D':
        return 3
    return -1

@login_required
def order_details_page(request, order_id):
    ordr = get_object_or_404(Orders, user_id=request.user, order_id=order_id)

    temp = {
        'order_id': ordr.order_id,
        'order_time': ordr.created.astimezone(IST_TZ).strftime('%d %b %Y %I:%M%p'),
        'amount': ordr.total_amount,
        'status': ordr.get_order_state_display(),
        'order_state': ordr.order_state,
        'order_state_no': get_order_state_num(ordr.order_state),
        'tracking': ordr.tracking_no,
        'courier': ordr.courier,
        'delivery_charge': ordr.delivery_charge,
        'extra_charge': ordr.extra_charge,
        'subtotal': ordr.total_amount - (ordr.delivery_charge+ordr.extra_charge),
        'paymode': ordr.get_paymode_display(),

        'address_name': ordr.address_name,
        'address_mobile': ordr.mobile,
        'address1': ordr.address1,
        'address2': ordr.address2,
        'pincode': ordr.zipcode,
        'pincodedisplay': ordr.pincodedisplay,

        'referal_code': ordr.referal_code
    }
    prod_data = []
    ord_prds = ordr.orderprods.all().order_by('id')
    for ord_prd in ord_prds:
        t = {
            'img': '',
            'title': '',
            'subtitle': '',
            'slug': '',
            'qty': ord_prd.quantity,
            'price': ord_prd.price
        }
        try:
            if ord_prd.prod_id:
                t['img'] = ord_prd.prod_id.mainimage.img_data.th_mini.image.url
                t['title'] = ord_prd.prod_id.name
                t['subtitle'] = ord_prd.prod_id.pagetitle
                t['slug'] = ord_prd.prod_id.slug
        except:
            pass
        prod_data.append(t)
    temp['prod_data'] = prod_data

    order_data = temp

    context = {
        'loggedin': request.user.is_authenticated,
        'cartqty': get_cart_qty(request),
        'order': order_data
    }
    return render(request, 'order-details-page.html', context)




@login_required
def get_paytm_details(request):
    resp = {
        'success': False,
        'reason': '',
    }
    try:
        cart = Cart.objects.get(user_id=request.user)
        cart_json = process_cart_json(request.user)
        total = cart_json['total']
        if cart.to_be_order_id == '' or cart.to_be_order_id is None:
            cart.to_be_order_id = generate_order_id(request.user)
            cart.save()

        user_code = get_user_code(request.user)
        if not user_code:
            return JsonResponse(resp)

        order_id = cart.to_be_order_id +'_'+get_rand_number(4)

        data = {
            "MID": settings.PAYTM['MID'].encode("utf8"),
            "ORDER_ID": order_id.encode("utf8"),
            "CUST_ID": user_code.encode("utf8"),
            "TXN_AMOUNT": str(int(total)).encode("utf8"),
            "CHANNEL_ID": settings.PAYTM['CHANNEL_ID'].encode("utf8"),
            "WEBSITE": settings.PAYTM['WEBSITE'].encode("utf8"),
            "INDUSTRY_TYPE_ID": settings.PAYTM['INDUSTRY_TYPE_ID'].encode("utf8"),
            "CALLBACK_URL": settings.PAYTM['CALLBACK_URL'].encode('utf8')
        }
        checksum = PaytmChecksum.generate_checksum(data, settings.PAYTM["MERCHANT_KEY"].encode("utf8"))
        #print(PaytmChecksum.verify_checksum(data, settings.PAYTM["MERCHANT_KEY"].encode("utf8"), checksum))
        for key in data:
            data[key] = data[key].decode('utf8')

        data['CHECKSUMHASH'] = checksum
        resp['data'] = data
        resp['txn_url'] = settings.PAYTM['Transaction_URL']
        resp['success'] = True
    except Exception as e:
        resp['reason'] = traceback.print_exception()
    return JsonResponse(resp)



@csrf_exempt
def paytm_callback(request):
    success = True
    txn_success = False
    try:
        data = request.POST.dict()
        checksum = data['CHECKSUMHASH']
        d_data = {}
        for key in data:
            d_data[key] = data[key].encode('utf8')
        verify_checksum = PaytmChecksum.verify_checksum(d_data, settings.PAYTM["MERCHANT_KEY"].encode("utf8"), checksum)

        if not verify_checksum:
            return Http404
        if data['STATUS'] in ['TXN_SUCCESS', 'PENDING']:
            order_id = data['ORDERID'][:12]
            user_code = order_id[-7:]
            user_id = UserCode.objects.get(code=user_code)
            cart = Cart.objects.get(user_id = user_id.user_id)
            if cart.to_be_order_id == order_id:
                txn_amount = float(data['TXNAMOUNT'])
                txn_date = make_aware(datetime.strptime(data['TXNDATE'], '%Y-%m-%d %H:%M:%S.%f'))

                cart.cart_state = 'D'
                cart.payment_amount = txn_amount
                cart.paymode = 'PayTM'
                cart.save()

                paytm_hist = PaytmHistory(user_id = user_id.user_id, txn_amount = txn_amount,
                                          txn_date=txn_date, txn_id=data['TXNID'],
                                          status=data['STATUS'], paytm_orderid = data['ORDERID'],
                                          order_id=order_id, currency=data['CURRENCY'])
                paytm_hist.save()

                txn_success = True
        success = True
    except:
        print(traceback.format_exc())
    if not success:
        raise Exception
    else:
        if txn_success:
            return HttpResponseRedirect('/cart?status=success&mode=paytm')
        else:
            return HttpResponseRedirect('/cart?status=fail')




def generate_merchant_data(request):
    prods = Product.objects.filter(is_published=True, is_google=True)
    data = []
    heading = ['id','title','description','price','condition','link','availability','image_link','google_​​product_​​category', 'product_type']
    data.append(heading)
    for p in prods:
        available = 'in stock'
        if not p.in_stock:
            available = 'out of stock'
        modified_description = p.description.replace('\r', ' ').replace('\n', ' ').replace('\t',' ')
        modified_description = ' '.join(modified_description.split(' '))

        google_product_type = ''
        if p.breadcrumb:
            google_product_type = p.breadcrumb.google_product_taxonomy

        custom_product_type = ''
        if p.breadcrumb:
            bread_data = []
            breads = BreadEntry.objects.filter(bread_id=p.breadcrumb).order_by('rank')
            for b in breads:
                bread_data.append(b.link_id.name)
            custom_product_type = ' > '.join(bread_data)

        t = [p.sku,
             p.product_head,
             modified_description,
             str(p.price),
             'new',
             'https://noobtronics.ltd/product/'+p.slug,
             available,
             'https://noobtronics.ltd'+p.mainimage.img_data.th_home.image.url,
             google_product_type,
             custom_product_type
             ]
        data.append(t)

    output = ''
    for r in data:
        output += '\t'.join(r)
        output += '\n'

    return HttpResponse(output, content_type='text/plain; charset=utf8')



@ensure_csrf_cookie
def process_download(request, name):
    show_page = False
    title = ''
    big_title = ''
    windows_link = ''
    mac_link = ''
    ubuntu_link = ''

    dat = get_object_or_404(DownloadsModel,slug=name)

    context = {
        'title':dat.title,
        'big_title':dat.big_title,
        'windows_link':dat.windows_link,
        'mac_link':dat.mac_link,
        'ubuntu_link':dat.ubuntu_link,

        'loggedin': request.user.is_authenticated,
        'cartqty': get_cart_qty(request),
        'whatsapp_on_mobile': True
    }
    return render(request, 'download-page.html', context)


@ensure_csrf_cookie
def process_master(request, name):
    if name in ['atmega328p', 'atmega328pb'] :
        return HttpResponseRedirect('https://www.arduino.cc/en/Tutorial/BuiltInExamples')
    return Http404



@login_required
def savemobile(request):
    resp = {'success': False}
    try:
        data = json.loads(request.body.decode('utf-8'))
        if len(data['mobile']) == 10 and data['mobile'].isdigit():
            usrcode = request.user.usercode
            usrcode.mobile = data['mobile']
            usrcode.save()
            resp['success'] = True
    except:
        pass
    return JsonResponse(resp)




def process_google_callback(request):
    state = '/'
    try:
        state = request.GET['state']
        code = request.GET['code']

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'mysite/google_client_secret.json',
            scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
            redirect_uri='https://noobtronics.ltd/googlecallback'
        )

        flow.fetch_token(code=code)
        session = flow.authorized_session()
        data = session.get('https://www.googleapis.com/userinfo/v2/me').json()

        user = User.objects.filter(email=data['email'])
        if not user.exists():
            user = User(email=data['email'], username=data['email'],
                        first_name=data['given_name'],
                        last_name=data['family_name'])
            user.save()
        else:
            user = user[0]

        user_code = get_user_code(user)
        if not user_code:
            return JsonResponse(resp)

        login(request, user)

        return redirect(state)
    except:
        print(traceback.format_exc())
        pass
    raise Exception



def process_facebook_callback(request):
    state = '/'
    try:
        state = request.GET['state']
        code = request.GET['code']

        url = 'https://graph.facebook.com/v3.2/oauth/access_token?client_id=330900420888261&client_secret=096435e1e2ad77bd52f34fd654804d68&code='+code

        url += '&redirect_uri=https%3A%2F%2Fnoobtronics.ltd%2Ffacebookcallback'
        #url += '&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Ffacebookcallback'
        r = requests.get(url)

        data = json.loads(r.text)
        if 'access_token' not in data:
            raise ValueError("Access token not found")

        graph = facebook.GraphAPI(access_token=data['access_token'])
        user_data = graph.get_object(id='me', fields='email,first_name,last_name')

        user = User.objects.filter(email=user_data['email'])
        if not user.exists():
            user = User(email=user_data['email'], username=user_data['email'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'])
            user.save()
        else:
            user = user[0]

        user_code = get_user_code(user)
        if not user_code:
            return JsonResponse(resp)

        login(request, user)

        return redirect(state)

    except:
        print(traceback.format_exc())
        pass
    raise Exception



def handle_email_login(request):
    resp = {
        'success': False,
        'login_help': 'Error'
    }
    try:
        data = json.loads(request.body)

        user = User.objects.filter(email=data['email'])
        if not user.exists():
            user = User(email=data['email'], username=data['email'],
                        first_name=data['email'],
                        last_name='')
            user.set_password(data['password'])
            user.save()

        else:
            user = user[0]


        user_code = get_user_code(user)
        if not user_code:
            return JsonResponse(resp)

        user = authenticate(username=data['email'], password=data['password'])
        if user is not None:
            login(request, user)
            resp['success'] = True
            resp['login_help'] = ''
        else:
            resp['login_help'] = 'Account Exist, Invalid Password'

    except:
        print(traceback.format_exc())
        pass
    return JsonResponse(resp)


def handle_forgotpwd(request):
    resp = {
        'success': False,
        'login_help': 'Error'
    }
    try:
        data = json.loads(request.body)

        user = User.objects.filter(email=data['email'])
        if not user.exists():
            resp['login_help'] = 'Account does not exist'
        else:
            user = user[0]
        send_pwdreset_mail(user.id)
        resp['success'] = True
        resp['login_help'] = ''
    except:
        print(traceback.format_exc())
        pass
    return JsonResponse(resp)



def forgotpwd_view(request, code):
    success = False
    if request.method == 'POST':
        obj = get_object_or_404(ForgorPWDLink, code=code)
        pwd = request.POST.get('password')
        user = obj.user_id
        user.set_password(pwd)
        user.save()
        obj.delete()
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        obj = get_object_or_404(ForgorPWDLink, code=code)
        context = {
            'loggedin': request.user.is_authenticated,
            'cartqty': get_cart_qty(request),
            'whatsapp_on_mobile': True
        }
        return render(request, 'forgot_password.html',context)
    raise Exception


def my_http404_view(request, exception=''):
    context = {
        'loggedin': request.user.is_authenticated,
        'cartqty': get_cart_qty(request),
        'whatsapp_on_mobile': True
    }
    return render(request, 'http404_page.html',context, status=404)



def my_http500_view(request, exception=''):
    context = {
        'loggedin': request.user.is_authenticated,
        'cartqty': get_cart_qty(request),
        'whatsapp_on_mobile': True
    }
    return render(request, 'http500_page.html',context,status=500)