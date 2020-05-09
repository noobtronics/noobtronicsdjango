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

    page_config = json.loads(config.config)
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
    # for i in page_config['catalog']:
    #     prods = []
    #     for sku in i['products']:
    #         sku = str(sku)
    #         if sku in prod_data:
    #             prods.append(prod_data[sku])
    #
    #     temp = {
    #         'name': i['name'],
    #         'products': prods,
    #     }
    #     catalog.append(temp)



    context = {
        'title': config.title,
        'keywords': config.keywords,
        'description': config.description,
        'h1': config.h1,

        'catalog': catalog,
    }
    return render(request, 'home-page.html', context)


@log_urlhistory
@ensure_csrf_cookie
def product_page(request, category_slug, prod_slug):
    prod = get_object_or_404(Product, slug='{0}/{1}'.format(category_slug, prod_slug))

    variants = []
    prices = []
    for v in prod.variants.all().order_by('rank'):

        temp = {
            'name': v.name,
            'count': json.loads(v.image)['count'],
            'is_disabled': 'disabled' if not v.in_stock else '',
            'price': v.price,
            'stock': 'out of stock' if not v.in_stock else 'in stock',
        }
        prices.append(v.price)
        variants.append(temp)

    context = {
        'title': prod.title,
        'keywords': prod.keywords,
        'meta_description': prod.meta_description,
        'name': prod.name,
        'description': prod.description,
        'h1': '',
        'images': json.loads(prod.images),
        'variants': variants,
        'pricerange': '{0} - {1}'.format(min(prices), max(prices)),
        'html': prod.html,


    }
    return render(request, 'product-page.html', context)
