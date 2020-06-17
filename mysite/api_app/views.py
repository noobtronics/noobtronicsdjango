from django.shortcuts import render

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from siteconfig.models import *
from ecommerce.models import *
from api_app.helpers import *



class homepage_api(APIView):

    def get_product_category_wise(self):
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
        return catalog



    @swagger_auto_schema(
                         responses={
                             200: openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description="200 status means OK",
                                ),
                             500: openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description="Internal Error",
                            )

                         }
    )
    def get(self, request, format=None):
        context = {
            'meta': get_page_meta('homepage'),
            'catalog': self.get_product_category_wise(),
        }
        return Response(context)
