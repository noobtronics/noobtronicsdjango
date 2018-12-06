from products.models import *
import json


STRUCTURED_DATA_BASE = {
    "@context": "http://schema.org",
}







def get_product_structured_data(prod_id):
    prod = Product.objects.get(id=prod_id)

    data = {}
    data.update(STRUCTURED_DATA_BASE)

    category = ''
    try:
        tags = ProductTags.objects.filter(tag_id__parent__isnull=True, prod_id=prod)
        main_tag = tags[0]
        category = main_tag.tag_id.name
    except:
        pass


    availability = 'http://schema.org/InStock'
    if not prod.in_stock:
        availability = 'http://schema.org/OutOfStock'

    prod_fields = {
        "@type": "Product",
        'brand': 'noobtronics',
        'category': category,
        'manufacturer': 'noobtronics',
        'model': prod.name,
        'name': prod.name + ' | '+ prod.pagetitle,
        'alternateName': prod.name,
        'description': prod.description,
        'image': 'https://noobtronics.ltd'+prod.mainimage.img_data.th_home.image.url,

        "offers": {
            "@type": "Offer",
            "availability": availability,
            "price": prod.price,
            "priceCurrency": "INR",
            "itemCondition": "http://schema.org/NewCondition"
        },
    }

    data.update(prod_fields)
    return json.dumps(data)