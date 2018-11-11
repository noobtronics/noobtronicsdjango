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
from products.admin_views import get_cart_qty, process_prod_page
from django.shortcuts import get_list_or_404, get_object_or_404


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


def get_parents_tags(parent, depth):
    if parent:
        tgs = Tags.objects.filter(parent=parent).order_by('rank')
    else:
        tgs = Tags.objects.filter(parent__isnull=True).order_by('rank')
    data = {}
    childs = []
    for t in tgs:
        cdepth = depth
        if t.type == 'M':
            cdepth = depth + 1
        t = {
            'data': get_parents_tags(t, cdepth),
            'name': t.name,
            'id': t.id,
            'type': t.type
        }
        childs.append(t)

    html = ''
    if parent:
        if len(childs) == 0:
            if parent.type == 'T':
                html = '<li><label class="checkbox">' \
                       '<input name="{0}" type="checkbox">{1}' \
                       '</label></li>'.format(parent.id, parent.name)
        else:
            html = ''
            child_html = ''
            for c in childs:
                child_html += c['data']['html']

            if parent.type=='S':
                html = '<li class="menusection">{0}</li>'.format(parent.name)
                html += child_html
            elif parent.type=='M':
                html = '<li><a class="" v-on:click="change_menu({2},{1})" v-bind:class="{{ \'is-active\': menu_selected[{2}]=={1}}}">{0}</a></li>'.format(parent.name, parent.id, depth-1)
                if child_html != '':
                    html += '<ul class="menu-list children" v-bind:class="{{\'showchildren\': menu_selected[{1}]=={0}}}">'.format(parent.id, depth-1)
                    html += child_html
                    html += '</ul>'
    else:
        html = ''
        for c in childs:
            html += c['data']['html']
    id = ''
    if parent:
        id = parent.id
    selected_id = ''
    if len(childs)>0:
        selected_id = childs[0]['data']['id']

    data = {
       # 'childs': childs,
        'html': html,
        'depth': depth,
        'id': id,
        'selected_id': selected_id
    }
    return data


def get_prod_data():
    prods = Product.objects.all().order_by('-id')[:5]
    data = []
    for prod in prods:
        t = {
            'id': prod.id,
            'name': prod.name,
            'cardtitle': prod.cardtitle,
            'price': prod.price,
            'slug': prod.slug,
            'mrp': prod.mrp_price,
            'thumb': prod.mainimage.img_data.th_mini.image.url
        }
        data.append(t)
        data.append(t)
        data.append(t)
        data.append(t)
        data.append(t)
        data.append(t)
        data.append(t)
        data.append(t)
        data.append(t)

    return data

def get_alltags_data():
    return get_parents_tags(None, 0)


@ensure_csrf_cookie
def shop_page(request):
    data = {}
    data['tags'] = get_alltags_data()
    data['tags_selected'] = [data['tags']['selected_id'], 0, 0, 0, 0]
    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'cartqty': get_cart_qty(request),
        'prod_data': get_prod_data()
    }
    pprint(data)
    return render(request, 'shop-page.html', context)




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


