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
from django.shortcuts import get_list_or_404, get_object_or_404


@staff_or_404
@ensure_csrf_cookie
def show_storeadmin(request):
    context = {
    }
    return render(request, 'storeadmin_dashboard.html', context)




def store_image_files(prod, media_path, img, store_main):
    uuid_name = str(uuid.uuid4())
    file_name =  uuid_name + '.png'
    file_name_s = uuid_name + '_300.png'
    file_name_u = uuid_name + '_64.png'
    main_path = media_path + '/' + file_name
    mini_path = media_path + '/' + file_name_s
    micro_path = media_path + '/' + file_name_u

    img_m = img.resize([300,300],PIL.Image.ANTIALIAS)
    img_u = img.resize([64,64],PIL.Image.ANTIALIAS)

    img.save(main_path)
    img_m.save(mini_path)
    img_u.save(micro_path)
    img_main = Image(prod_id=prod, image = main_path)
    img_main.save()
    tn_mini = Thumbnail(img_id=img_main, image=mini_path)
    tn_mini.save()
    if store_main:
        main_ = MainImage(prod_id = prod, main_img=img_main, main_thumb=tn_mini)
        main_.save()
    tn_micro = Thumbnail(img_id=img_main, image=micro_path)
    tn_micro.save()


@staff_or_404
def admin_add_product(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = request.POST.dict()
        image = request.FILES['image']
        if image.content_type != 'image/png':
            resp['reason'] = 'Only PNG Image are supported'
            return JsonResponse(resp)

        if image.size > 512000:
            resp['reason'] = 'Image size should be < 500KB'
            return JsonResponse(resp)

        im = PIL.Image.open(image)
        im_w, im_h = im.size


        if im_w != im_h:
            resp['reason'] = 'Image is not square'
            return JsonResponse(resp)

        prod = Product(name=data['name'], cardtitle=data['cardsubtitle'],
                       pagetitle=data['prodsubtitle'], slug=data['slug'],
                       price=data['price'], mrp_price=data['mrpprice'])
        prod.save()
        media_path = 'media/'+data['slug']
        pathlib.Path(media_path).mkdir(parents=True, exist_ok=True)
        store_image_files(prod, media_path, im, True)
        resp['success'] = True

    except Exception as e:
        resp['reason'] = str(e)
    return JsonResponse(resp)


@staff_or_404
def admin_add_to_home(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = request.POST.dict()
        prod = Product.objects.get(id=data['prod_id'])
        if not prod.is_published:
            resp['reason'] = 'Product is unpublished'
            return JsonResponse(resp)
        hp = HomePage(prod_id=prod, rank=data['rank'])
        hp.save()
        resp['success'] = True

    except Exception as e:
        resp['reason'] = str(e)
    return JsonResponse(resp)

@staff_or_404
def admin_fetch_product(request):
    prods = Product.objects.all().order_by('-id')[:5]
    data = []
    for prod in prods:
        t = {
            'id': prod.id,
            'name': prod.name,
            'cardtitle': prod.cardtitle,
            'price': prod.price,
            'mrp': prod.mrp_price,
            'thumb': prod.mainimage.main_thumb.image.url
        }
        data.append(t)
    resp = {
        'data': data
    }
    return JsonResponse(resp)


@staff_or_404
def show_demo_home(request, prod_id):
    prod = get_object_or_404(Product,id=prod_id)
    t = {
        'id': prod.id,
        'name': prod.name,
        'pagetitle': prod.pagetitle,
        'price': prod.price,
        'mrp': prod.mrp_price,
        'image': prod.mainimage.main_img.image.url
    }
    data = []
    data.append(t)
    data.append(t)
    context = {
        'loggedin': request.user.is_authenticated,
        'data': data
    }
    return render(request, 'admin-demo-home-page.html', context)