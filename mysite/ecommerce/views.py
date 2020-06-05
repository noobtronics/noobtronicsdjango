from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .decorators import log_urlhistory
from .models import *
import json
from pprint import pprint
from siteconfig.models import Page
from django.shortcuts import get_list_or_404, get_object_or_404
import json


@log_urlhistory
@ensure_csrf_cookie
def home_page(request):
    config = Page.objects.get(name='homepage')

    prod_ids = []
    prod_data = {}
    # for i in page_config['catalog']:
    #     for sku in i['products']:
    #         prod_ids.append(str(sku))
    #
    #
    # prods = Product.objects.filter(sku__in = prod_ids)
    # for prod in prods:
    #     temp = {
    #         'name': prod.name,
    #         'cardtitle': prod.cardtitle,
    #         'slug': prod.slug,
    #         'thumb': prod.mainimage.thumb_data.th_mini.image.url
    #     }
    #     prod_data[prod.sku] = temp


    catalog = []
    cats = Category.objects.all().order_by('rank')
    for cat in cats:
        prod_array = []
        prods = cat.cat_products.all().order_by('rank')
        for prod in prods:
            vars = prod.variants.filter(is_shop=True).order_by('rank')
            for var in vars:
                image = json.loads(var.image)
                temp = {
                        'cardname': var.cardname,
                        'cardtitle': var.cardtitle,
                        'slug': prod.slug,
                        'thumb': image
                    }
                prod_array.append(temp)
        temp = {
                'name': cat.name.title(),
                'products': prod_array,
            }
        catalog.append(temp)

    # for i in page_config['catalog']:
    #     prods = []
    #     for sku in i['products']:
    #         sku = str(sku)
    #         if sku in prod_data:
    #             prods.append(prod_data[sku])
    #
    #



    context = {
        'title': config.title,
        'keywords': config.keywords,
        'description': config.meta_description,
        'h1': config.h1,

        'catalog': catalog,
    }
    return render(request, 'home-page.html', context)



@log_urlhistory
@ensure_csrf_cookie
def shop_page(request):
    config = Page.objects.get(name='shoppage')

    prod_ids = []
    prod_data = {}


    prod_array = []
    category = []
    cats = Category.objects.all().order_by('rank')
    for cat in cats:
        temp = {
            'name': cat.name,
            'slug': cat.slug,
        }
        category.append(temp)
        prods = cat.cat_products.all().order_by('rank')
        for prod in prods:
            vars = prod.variants.filter(is_shop=True).order_by('rank')
            for var in vars:
                image = json.loads(var.image)
                temp = {
                        'cardname': var.cardname,
                        'cardtitle': var.cardtitle,
                        'slug': prod.slug,
                        'price': var.price,
                        'thumb': image
                    }
                prod_array.append(temp)


    context = {
        'title': config.title,
        'keywords': config.keywords,
        'description': config.meta_description,
        'h1': config.h1,
        'categorys': category,
        'products': prod_array,
    }
    return render(request, 'shop-page.html', context)




@log_urlhistory
@ensure_csrf_cookie
def shop_category_page(request, category_slug):

    category = get_object_or_404(Category, slug=category_slug)

    sub_category = []
    subs = category.subcategorys.all()
    for sub_cat in subs:
        temp = {
            'name': sub_cat.name,
            'slug': sub_cat.slug,
        }
        sub_category.append(temp)

    prod_array = []

    prods = category.cat_products.all().order_by('rank')
    for prod in prods:
        vars = prod.variants.filter(is_shop=True).order_by('rank')
        for var in vars:
            image = json.loads(var.image)
            temp = {
                    'cardname': var.cardname,
                    'cardtitle': var.cardtitle,
                    'slug': prod.slug,
                    'price': var.price,
                    'thumb': image
                }
            prod_array.append(temp)


    context = {
        'title': category.title,
        'keywords': category.keywords,
        'description': category.meta_description,
        'h1': category.h1,
        'name': category.name,
        'content': category.html,

        'sub_category': sub_category,
        'products': prod_array,
    }
    return render(request, 'shop-category-page.html', context)



@log_urlhistory
@ensure_csrf_cookie
def shop_subcategory_page(request, subcategory_slug):

    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)


    prod_array = []

    prods = subcategory.subcat_products.all().order_by('rank')
    for prod in prods:
        vars = prod.variants.filter(is_shop=True).order_by('rank')
        for var in vars:
            image = json.loads(var.image)
            temp = {
                    'cardname': var.cardname,
                    'cardtitle': var.cardtitle,
                    'slug': prod.slug,
                    'price': var.price,
                    'thumb': image
                }
            prod_array.append(temp)


    context = {
        'title': subcategory.title,
        'keywords': subcategory.keywords,
        'description': subcategory.meta_description,
        'h1': subcategory.h1,
        'name': subcategory.name,
        'content': subcategory.html,

        'products': prod_array,
    }
    return render(request, 'shop-subcategory-page.html', context)




@log_urlhistory
@ensure_csrf_cookie
def product_page(request, category_slug, prod_slug):
    prod = get_object_or_404(Product, slug='{0}/{1}'.format(category_slug, prod_slug))

    variants = []
    variants_dic = {}
    prices = []
    for v in prod.variants.all().order_by('rank'):

        temp = {
            'name': v.name,
            'image': json.loads(v.image)['id'],
            'is_disabled': 'disabled' if not v.in_stock else '',
            'price': v.price,
            'stock': 'out of stock' if not v.in_stock else 'in stock',
            'id': str(v.id),
        }
        prices.append(v.price)
        variants.append(temp)
        variants_dic[temp['id']] = temp

    context = {
        'title': prod.title,
        'shortname': prod.shortname,
        'keywords': prod.keywords,
        'meta_description': prod.meta_description,
        'url': prod.slug,
        'name': prod.name,
        'description': prod.description,
        'h1': prod.name,
        'sub_category': {
            'name': prod.sub_category.name,
            'slug': prod.sub_category.slug,
        },
        'images': json.loads(prod.images),
        'variants': variants,
        'variants_dic': variants_dic,
        'pricerange': '{0} - {1}'.format(min(prices), max(prices)),
        'html': prod.html,

    }

    return render(request, 'product-page.html', context)
