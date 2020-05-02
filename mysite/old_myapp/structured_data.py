from products.models import *
import json
from datetime import timedelta
from django.utils import timezone


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

    reviews_list = [
        {
            "@type": "Review",
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": "4",
                "bestRating": "5"
            },
            "author": {
                "@type": "Person",
                "name": "Shrikant"
            }
        },
    ]

    prod_fields = {
        "@type": "Product",
        'brand': 'noobtronics',
        'category': category,
        'manufacturer': 'noobtronics',
        'model': prod.name,
        'name': prod.product_head,
        'alternateName': prod.name,
        'description': prod.description,
        'image': 'https://noobtronics.in'+prod.mainimage.img_data.th_home.image.url,
        'url': 'https://noobtronics.in/product/'+prod.slug,
        'sku': prod.sku,
        'mpn': prod.sku,

        'review': reviews_list,
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4",
            "reviewCount": "1"
        },

        "offers": {
            "@type": "Offer",
            "availability": availability,
            "price": prod.price,
            "priceCurrency": "INR",
            "itemCondition": "http://schema.org/NewCondition",
            "priceValidUntil": (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'url': 'https://noobtronics.in/product/' + prod.slug,
        },
    }

    data.update(prod_fields)
    return json.dumps(data)



def get_blog_structured_data(blog_id):
    blog = Blog.objects.get(id=blog_id)

    data = {}
    data.update(STRUCTURED_DATA_BASE)


    image_list = []

    images = blog.blogphotos.filter(main_image=True)
    for img in images:
        image_list.append('https://noobtronics.in/media'.format(img.image))


    data_fields = {
        "@type": "BlogPosting",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": "https://noobtronics.in/blog"
          },
         "headline": blog.name,
         "description": blog.description,
         "image":image_list,
         "datePublished": blog.created.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
         "dateModified": blog.updated.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
         "author": {
            "@type": "Person",
            "name": "Nikhil"
          },

         "publisher": {
            "@type": "Organization",
            "name": "noobtronics",
            "logo": {
            "@type": "ImageObject",
            "url": "https://noobtronics.in/static/images/Logo.png"
            }
        },
    }

    data.update(data_fields)
    return json.dumps(data)
