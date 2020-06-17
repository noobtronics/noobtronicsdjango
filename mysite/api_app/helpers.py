from siteconfig.models import *
from ecommerce.models import *

def get_page_meta(name):
    config = Page.objects.get(name=name)
    meta = {
        'title': config.title,
        'keywords': config.keywords,
        'description': config.meta_description,
        'h1': config.h1,
    }
    return meta
