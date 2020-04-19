from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .decorators import log_urlhistory
from .models import *
from products.models import *
import json
from pprint import pprint


@log_urlhistory
@ensure_csrf_cookie
def home_page(request):
    config = Page.objects.get(name='homepage')

    page_config = json.loads(config.config)
    prod_ids = []
    prod_data = {}
    for i in page_config['catalog']:
        for sku in i['products']:
            prod_ids.append(str(sku))

    pprint(prod_ids)
    prods = Product.objects.filter(sku__in = prod_ids)
    for prod in prods:
        temp = {
            'name': prod.name,
            'cardtitle': prod.cardtitle,
            'slug': prod.slug,
            'thumb': prod.mainimage.thumb_data.th_mini.image.url
        }
        prod_data[prod.sku] = temp

    pprint(prod_data)


    catalog = []
    for i in page_config['catalog']:
        prods = []
        for sku in i['products']:
            sku = str(sku)
            if sku in prod_data:
                prods.append(prod_data[sku])

        temp = {
            'name': i['name'],
            'products': prods,
        }
        catalog.append(temp)



    context = {
        'title': config.title,
        'keywords': config.keywords,
        'description': config.description,
        'h1': config.h1,

        'catalog': catalog,
    }
    return render(request, 'home-page.html', context)
