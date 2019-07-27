from django.shortcuts import render, redirect
from django.http import HttpResponse
from pprint import pprint, pformat
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
from django.utils import timezone
import requests
from paytm import Checksum as PaytmChecksum
from myapp.structured_data import *
import math



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
                       '<input name="{0}" value="{0}" type="checkbox" v-on:change="update_checkbox_prods(1,{0})">{1}' \
                       '</label></li>'.format(parent.id, parent.name,depth )
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
        main_ = MainImage(prod_id = prod, img_data=imgData, thumb_data=imgData)
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
                       description=data['description'],
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

    data_conf = json.loads(request.body)
    count_per_page = 20
    prod_counts = Product.objects.all().count()
    total_pages = int(math.ceil(prod_counts/1.0/count_per_page))
    current_page = 1

    if 'page' in data_conf:
        current_page = data_conf['page']

    prods = Product.objects.all().order_by('-id')[(current_page-1)*count_per_page:count_per_page*current_page]
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
        'data': data,
        'current_page': current_page,
        'total_pages': total_pages
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



def get_similar_prod(prod_id):
    has_similar_prod = False
    similar_prod = []
    try:
        prod = Product.objects.get(id=prod_id)
        similar_prods = SimilarProducts.objects.filter(prod_id=prod).order_by('rank')
        for entry in similar_prods:
            sim_prod = entry.sim_id
            temp = {
                'id': sim_prod.id,
                'name': sim_prod.name,
                'cardtitle': sim_prod.cardtitle,
                'price': sim_prod.price,
                'slug': sim_prod.slug,
                'mrp': sim_prod.mrp_price,
                'thumb': sim_prod.mainimage.thumb_data.th_mini.image.url
            }
            #print(temp)
            similar_prod.append(temp)
        if len(similar_prod) > 0:
            has_similar_prod = True
    except:
        print(traceback.format_exc())
    return has_similar_prod, similar_prod


def get_related_prod(prod_id):
    has_related_prod = False
    related_prod = []
    try:
        prod = Product.objects.get(id=prod_id)
        related_prods = RelatedProducts.objects.filter(prod_id=prod).order_by('rank')
        for entry in related_prods:
            rel_prod = entry.sim_id
            temp = {
                'id': rel_prod.id,
                'name': rel_prod.name,
                'cardtitle': rel_prod.cardtitle,
                'price': rel_prod.price,
                'slug': rel_prod.slug,
                'mrp': rel_prod.mrp_price,
                'thumb': rel_prod.mainimage.thumb_data.th_mini.image.url
            }
            related_prod.append(temp)
            #print(temp)
        if len(related_prod) > 0:
            has_related_prod = True
    except:
        print(traceback.format_exc())
    return has_related_prod, related_prod





def process_prod_page(request, prod_id):


    require_mobile = 0

    if request.user.is_authenticated:
        if request.user.usercode.mobile == '':
            require_mobile = 1

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

    has_related_prods, related_prod_data =  get_related_prod(prod_id)
    has_similar_prods, similar_prod_data = get_similar_prod(prod_id)


    bullets = []
    bullets_data = prod.prodbullets.all().order_by('rank')
    for b in bullets_data:
        bullets.append(b.data)

    browse_links = []
    browse_data = prod.shoplinks.all().order_by('rank')
    for b in browse_data:
        browse_links.append({
            'url': b.link_id.url,
            'name': b.link_id.tag_id.name,
        })


    breadcrumbs = []
    if prod.breadcrumb:
        breads = prod.breadcrumb.breadentries.order_by('rank')
        for bread_entry in breads:
            temp = {
                'name': bread_entry.link_id.name,
                'url': bread_entry.link_id.url,
            }
            breadcrumbs.append(temp)


    keywordtags = []
    for kt in prod.keywordtags.order_by('rank'):
        temp = {
            'name': kt.keytag_id.name,
        }
        keywordtags.append(temp)



    data = {
        'id': prod.id,
        'sku': prod.sku,
        'name': prod.name,
        'meta_title': prod.meta_title,
        'meta_keywords': prod.keywords,
        'product_head': prod.product_head,
        'pagetitle': prod.pagetitle,
        'description': prod.description,
        'price': prod.price,
        'mrp': prod.mrp_price,
        'in_stock': in_stock,
        'waitlisted': waitlisted,
        'prod_details': prod_details,
        'url': 'https://noobtronics.ltd/product/'+prod.slug,
        'free_delivery': prod.free_delivery,
        'has_related_prods': has_related_prods,
        'related_prod_data': related_prod_data,
        'has_similar_prods': has_similar_prods,
        'similar_prod_data': similar_prod_data,
        'is_amazon': prod.is_amazon,
        'amazon_link': prod.amazon_link,
        'bullets': bullets,
        'browse_links': browse_links,
        'breadcrumbs': breadcrumbs,
        'keywordtags': keywordtags
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
        'cartqty': get_cart_qty(request),
        'page_structured_data': get_product_structured_data(prod.id),
        'whatsapp_on_mobile': True,
        'require_mobile': require_mobile,
        'page_type': 'product_page',
        'hide_description': prod.hide_description
    }
    for key in image_data:
        context[key] = image_data[key]
    return render(request, 'product-page.html', context)



def process_print_prod_page(request, prod_id):
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
        'description': prod.description,
        'price': prod.price,
        'mrp': prod.mrp_price,
        'in_stock': in_stock,
        'waitlisted': waitlisted,
        'prod_details': prod_details,
        'url': 'https://noobtronics.ltd/product/'+prod.slug,
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
        'cartqty': get_cart_qty(request),
        'page_structured_data': get_product_structured_data(prod.id)
    }
    for key in image_data:
        context[key] = image_data[key]
    return render(request, 'print-product-page.html', context)



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
def admin_fetch_keywordtags(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        keytags = KeyWordTags.objects.all().order_by('name')
        key_list = []
        for t in keytags:
            key_list.append(t.name)
        output = {
            'keytags': key_list
        }
        resp['data'] = output
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


@staff_or_404
def handle_media_backup(request):
    dt = timezone.now()
    archive_name = 'media_'+dt.strftime("%d-%b-%Y_%H-%M-%S")
    fil_name = archive_name + '.tar.bz2'
    fil_path = "backup/"+fil_name
    with tarfile.open(fil_path, mode='w:bz2') as archive:
        archive.add('media')

    return HttpResponse("Media Backup done")


@staff_or_404
def admin_paytm_status(request):
    order_id = request.GET.get("order_id")
    paytm = get_object_or_404(PaytmHistory, order_id=order_id)
    data = {
        "MID": settings.PAYTM['MID'].encode("utf8"),
        "ORDERID": paytm.paytm_orderid.encode("utf8"),
    }
    checksum = PaytmChecksum.generate_checksum(data, settings.PAYTM["MERCHANT_KEY"].encode("utf8"))

    for key in data:
        data[key] = data[key].decode('utf8')
    data['CHECKSUMHASH'] = checksum
    response = requests.post(settings.PAYTM["Status_URL"],
                            headers={"content-type": "application/json"},
                             json=data
                             )
    json_resp = json.loads(response.text)
    output = pformat(json_resp)
    return HttpResponse(output, content_type="application/json")



@staff_or_404
def show_markdown_editor(request):
    context = {}
    return render(request, 'markdown_editor.html', context)


@staff_or_404
def show_blog_edit_page(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    photo_urls = []
    for p in blog.blogphotos.all():
        photo_urls.append('/media'+p.image.url)

    context = {
        'html_data': blog.html,
        'markdown_data': blog.markdown,
        'short_html_data': blog.short_html,
        'short_markdown_data': blog.short_markdown,
        'photo_urls': photo_urls,
        'slug': blog.slug,
        'name': blog.name
    }

    return render(request, 'blog_editor.html', context)



def show_blog_page(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)

    data = {
        'html_data': blog.html,
        'name': blog.name,
        'meta_title': blog.name,
        'description': blog.description,
        'meta_keywords': blog.keywords,
    }

    context = {
        'loggedin': request.user.is_authenticated,
        'data': data,

        'cartqty': get_cart_qty(request),
        #'page_structured_data': get_product_structured_data(prod.id),
        'whatsapp_on_mobile': False,
        'require_mobile': False,
        'page_type': 'blog_page',
        'page_structured_data': get_blog_structured_data(blog.id),
    }

    return render(request, 'blog-page.html', context)



@staff_or_404
def admin_show_blog_page(request, blog_slug):
    return show_blog_page(request, blog_slug)

@staff_or_404
def admin_save_blog_data(request):
    resp = {
        'success': False,
        'reason': ''
    }
    try:
        data = json.loads(request.body)

        blog = get_object_or_404(Blog, slug=data['slug'])
        blog.html = data['html']
        blog.markdown = data['markdown']
        blog.short_html = data['short_html']
        blog.short_markdown = data['short_markdown']
        blog.save()
        resp['success'] = True

    except Exception as e:
        resp['reason'] = traceback.format_exc()
    return JsonResponse(resp)
