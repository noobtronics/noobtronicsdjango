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
import traceback
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




def store_image_files(prod, media_path, img, store_main, rank):
    uuid_name = str(uuid.uuid4())
    file_name =  uuid_name + '.png'
    file_name_h = uuid_name + '_500.png'
    file_name_s = uuid_name + '_300.png'
    file_name_u = uuid_name + '_64.png'

    main_path = media_path + '/' + file_name
    im_home_path = media_path + '/' + file_name_h
    mini_path = media_path + '/' + file_name_s
    micro_path = media_path + '/' + file_name_u

    img_h = img.resize([500, 500], PIL.Image.ANTIALIAS)
    img_m = img.resize([300,300],PIL.Image.ANTIALIAS)
    img_u = img.resize([64,64],PIL.Image.ANTIALIAS)

    img.save(main_path)
    img_h.save(im_home_path)
    img_m.save(mini_path)
    img_u.save(micro_path)

    img_main = Image(prod_id=prod, image = main_path)
    img_main.save()
    tn_home = Thumbnail(img_id=img_main, image=im_home_path)
    tn_home.save()
    tn_mini = Thumbnail(img_id=img_main, image=mini_path)
    tn_mini.save()
    tn_micro = Thumbnail(img_id=img_main, image=micro_path)
    tn_micro.save()

    if store_main:
        rank = 1

    imgData = ImageData(prod_id=prod, img_id=img_main, th_home=tn_home,
                        th_mini=tn_mini, th_micro=tn_micro, rank=rank)
    imgData.save()

    if store_main:
        main_ = MainImage(prod_id = prod, img_data=imgData)
        main_.save()



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

        if image.size > 4096000:
            resp['reason'] = 'Image size should be < 4000KB'
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
        store_image_files(prod, media_path, im, True, 1)
        resp['success'] = True

    except Exception as e:
        resp['reason'] = traceback.format_exc()
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
        resp['reason'] = traceback.print_exception()
    return JsonResponse(resp)


@staff_or_404
def admin_upload_images(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = request.POST.dict()
        prod = Product.objects.get(id=data['prod_id'])
        files = request.FILES

        im_data = []

        for name in files:
            image = request.FILES[name]

            if image.content_type != 'image/png':
                resp['reason'] = 'Only PNG Image are supported '+image.name
                return JsonResponse(resp)

            if image.size > 4096000:
                resp['reason'] = 'Image size should be < 4000KB '+ image.name
                return JsonResponse(resp)

            im = PIL.Image.open(image)
            im_w, im_h = im.size


            if im_w != im_h:
                resp['reason'] = 'Image is not square '+image.name
                return JsonResponse(resp)

            im_data.append(im)

        media_path = 'media/' + prod.slug
        rank = 1
        for im in im_data:
            rank += 1
            store_image_files(prod, media_path, im, False, rank)
        resp['success'] = True

    except Exception as e:
        resp['reason'] = traceback.format_exc()
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
            'thumb': prod.mainimage.img_data.th_mini.image.url
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
        'image': prod.mainimage.img_data.th_home.image.url
    }
    data = []
    data.append(t)
    data.append(t)
    context = {
        'loggedin': request.user.is_authenticated,
        'data': data
    }
    return render(request, 'admin-demo-home-page.html', context)


@staff_or_404
def show_demo_prod(request, prod_id):
    prod = get_object_or_404(Product,id=prod_id)

    icon_images = []
    home_images = []
    large_images = []

    main_id = prod.mainimage.img_data.id
    icon_images.append(prod.mainimage.img_data.th_micro.image.url)
    home_images.append(prod.mainimage.img_data.th_home.image.url)
    large_images.append(prod.mainimage.img_data.img_id.image.url)

    imgdatas = prod.imagesdata.all().order_by('rank')
    for imgdata in imgdatas:
        if imgdata.id == main_id:
            continue
        icon_images.append(imgdata.th_micro.image.url)
        home_images.append(imgdata.th_home.image.url)
        large_images.append(imgdata.img_id.image.url)

    data = {
        'id': prod.id,
        'name': prod.name,
        'pagetitle': prod.pagetitle,
        'price': prod.price,
        'mrp': prod.mrp_price,
        'in_stock': True,
        'waitlisted': False
    }

    image_data = {
        'icon_images': icon_images,
        'home_images': home_images,
        'large_images': large_images
    }
    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'image_data': json.dumps(image_data)
    }
    for key in image_data:
        context[key]=image_data[key]
    return render(request, 'product-page.html', context)