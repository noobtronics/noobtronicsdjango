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
from PIL import Image as PIL_IMAGE
from .models import *
import pathlib
import uuid
from io import BytesIO
from django.shortcuts import get_list_or_404, get_object_or_404
import tarfile
from django.utils.encoding import smart_str


@staff_or_404
@ensure_csrf_cookie
def show_storeadmin(request):
    context = {
    }
    return render(request, 'storeadmin_dashboard.html', context)



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
                       '<input name="{0}" value="{0}" type="checkbox" v-on:change="update_menu_prods(1)">{1}' \
                       '</label></li>'.format(parent.id, parent.name)
            if parent.type == 'M':
                html = '<li><a class="" v-on:click="change_menu({2},{1})" v-bind:class="{{ \'is-active\': menu_selected[{2}]=={1}}}">{0}</a></li>'.format(parent.name, parent.id, depth-1)
        else:
            child_html = ''
            for c in childs:
                child_html += c['data']['html']

            if parent.type=='S':
                html = '<li class="menusection">{0}</li>'.format(parent.name)
                html += child_html
            elif parent.type=='M':
                html = '<li><a class="" v-on:click="change_menu({2},{1})" v-bind:class="{{ \'is-active\': menu_selected[{2}]=={1}}}">{0}</a></li>'.format(parent.name, parent.id, depth-1)
                if child_html != '':
                    html += '<ul class="menu-list" v-bind:class="{{\'nochildren\': menu_selected[{1}]!={0}}}">'.format(parent.id, depth-1)
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
        'childs': childs,
        'html': html,
        'depth': depth,
        'id': id,
        'selected_id': selected_id
    }
    return data

def get_alltags_data():
    data = get_parents_tags(None, 0)
    pprint(data)
    return data



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

    img_h = img.resize([500, 500], PIL_IMAGE.ANTIALIAS)
    img_m = img.resize([300,300],PIL_IMAGE.ANTIALIAS)
    img_u = img.resize([64,64],PIL_IMAGE.ANTIALIAS)

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

        im = PIL_IMAGE.open(image)
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

            im = PIL_IMAGE.open(image)
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
        'data': data,
        'cartqty': get_cart_qty(request)
    }
    return render(request, 'admin-demo-home-page.html', context)



def get_cart_qty(request):
    cartqty = 0
    if request.user.is_authenticated:
        cart_query = Cart.objects.filter(user_id=request.user)
        if cart_query.count() > 0:
            cartqty = CartObjects.objects.filter(cart_id=cart_query[0]).count()
    return cartqty


def get_cart_state(request):
    cart_state = 0
    if request.user.is_authenticated:
        cart_query = Cart.objects.filter(user_id=request.user)
        if cart_query.count() > 0:
            cart = cart_query[0]
            if cart.cart_state == 'A':
                cart_state = 1
            elif cart.cart_state == 'P':
                cart_state = 2
            elif cart.cart_state == 'D':
                cart_state = 3
    return cart_state


def process_prod_page(request, prod_id):
    prod = get_object_or_404(Product, id=prod_id)

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

    in_stock = prod.in_stock
    waitlisted = False
    if not in_stock:
        if request.user.is_authenticated:
            if Waitlist.objects.filter(prod_id=prod, user_id=request.user).count() > 0:
                waitlisted = True

    pds = ProductDetails.objects.filter(prod_id=prod).order_by('rank')
    prod_details = []
    pd_counter = 0
    for pd in pds:
        pd_counter += 1
        t = {
            'name': pd.name,
            'rank': pd_counter,
            'html': pd.html
        }
        prod_details.append(t)

    pprint(prod_details)

    data = {
        'id': prod.id,
        'name': prod.name,
        'pagetitle': prod.pagetitle,
        'price': prod.price,
        'mrp': prod.mrp_price,
        'in_stock': in_stock,
        'waitlisted': waitlisted,
        'prod_details': prod_details
    }

    image_data = {
        'icon_images': icon_images,
        'home_images': home_images,
        'large_images': large_images
    }
    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'image_data': json.dumps(image_data),
        'cartqty': get_cart_qty(request)
    }
    for key in image_data:
        context[key] = image_data[key]
    return render(request, 'product-page.html', context)


@staff_or_404
def show_demo_prod(request, prod_id):
    return process_prod_page(request, prod_id)



@staff_or_404
def admin_add_product_details(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = request.POST.dict()
        prod = Product.objects.get(id=data['prod_id'])
        name_list = [i for i in data.keys() if i.startswith('name')]
        name_list.sort()
        form_data = []
        for nm in name_list:
            key = nm[4:]
            temp = [data[nm], data['html'+key]]
            form_data.append(temp)
        rank = 0
        for d in form_data:
            rank += 1
            name, html = d
            pd = ProductDetails(prod_id=prod, rank=rank, name=name, html=html)
            pd.save()
        resp['success'] = True

    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)


@staff_or_404
def admin_fetch_menulist(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)
        info = ''
        parent = None
        parents = []
        if data['parent_id'] == '':
            ml = Tags.objects.filter(parent__isnull=True).order_by('rank')
        else:
            parent = Tags.objects.get(id=data['parent_id'])
            ml = Tags.objects.filter(parent=parent).order_by('rank')
        while parent:
            parents.append(parent.name)
            parent = parent.parent
        parents.reverse()
        parents.append('')
        info = ' &rarr; '.join(parents)
        output = []
        for tag in ml:
            temp = {
                'id': tag.id,
                'name': tag.name,
                'type': tag.type
            }
            output.append(temp)
        resp['data'] = output
        resp['info'] = info
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)


@staff_or_404
def admin_add_menu(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = request.POST.dict()
        parent = None
        rank = Tags.objects.filter(parent__isnull=True).count()+1
        if data['parent_id'] != '':
            parent = Tags.objects.get(id=data['parent_id'])
            rank = Tags.objects.filter(parent=parent).count() + 1

        t = Tags(parent=parent, name=data['name'], type=data['type'], rank=rank)
        t.save()
        resp['success'] = True
    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)


@staff_or_404
@ensure_csrf_cookie
def show_demo_shop(request, prod_id):
    prod = Product.objects.get(id=prod_id)
    data = {}
    data['tags'] = get_alltags_data()
    data['tags_selected'] = [data['tags']['selected_id'], 0, 0, 0, 0]
    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,
        'cartqty': get_cart_qty(request),
        'prod_data': [
            {
                'id': prod.id,
                'name': prod.name,
                'cardtitle': prod.cardtitle,
                'in_stock': 'true' if prod.in_stock else 'false',
                'price': prod.price,
                'slug': prod.slug,
                'mrp': prod.mrp_price,
                'thumb': prod.mainimage.img_data.th_mini.image.url
            }
        ]
    }
    return render(request, 'admin-shop-page.html', context)


@staff_or_404
def admin_add_prod_tags(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = request.POST.dict()
        prod = Product.objects.get(id=data['prod_id'])
        ProductTags.objects.filter(prod_id=prod).delete()

        menu_data = data['menu_data'].split(',')
        tags_list = []
        for mid in menu_data:
            if int(mid) > 0:
                tg = Tags.objects.get(id=mid)
                tags_list.append(tg)
            else:
                break

        del data['prod_id']
        del data['menu_data']

        for key in data:
            if data[key] == 'true':
                tg = Tags.objects.get(id=key)
                tags_list.append(tg)

        for tg in tags_list:
            ptg = ProductTags(prod_id=prod, tag_id = tg)
            ptg.save()


        resp['success'] = True

    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)


def handle_media_backup(request):
    dt = timezone.now()
    archive_name = 'media_'+dt.strftime("%d-%b-%Y_%H-%M-%S")
    fil_name = archive_name + '.tar.bz2'
    fil_path = "backup/"+fil_name
    with tarfile.open(fil_name, mode='w:bz2') as archive:
        archive.add('media')
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fil_name)
    response['X-Accel-Redirect'] = smart_str(fil_path)

    return response
