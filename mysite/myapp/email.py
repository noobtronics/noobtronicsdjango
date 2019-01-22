from django.core.mail import send_mail, EmailMultiAlternatives
from products.models import *
import pytz
from django.template import Context, Template
from django.template.loader import get_template
from django.http import HttpResponse


IST_TZ = pytz.timezone('Asia/Kolkata')


def test_mail(request):
    ordr = Orders.objects.all()[0]

    rendered_data = get_order_confirm_data(ordr)

    send_mail(
        subject='Your noobtronics.ltd order - #{0} has been received'.format(ordr.order_id),
        html_message = rendered_data,
        message = '',
        from_email = 'Noobtronics Shop <no-reply@noobtronics.ltd>',
        recipient_list = ['nikhil.raut94@gmail.com'],
        fail_silently=False,
    )


def get_order_confirm_data(ordr):
    ordr = Orders.objects.all()[0]

    products = []
    temp = ['data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAwBAMAAACh2TSJAAAALVBMVEUAAADtNTX////3n5/+9fX719f7zMz5tLTzfHzuQED//f31jY3ybGzxXV3wVFRaxp+rAAAAAXRSTlMAQObYZgAAALVJREFUOMut0rENAjEQRNHdC4kY0QBaAQUQX0QAFSAKIKQEKiAA6VqgIkriApuV1x7pQPz0aWwHljLMpZ0CRDBGoXmeghGYKFJsUo90giAImCgV5OJF+oOgKE48MlGgs2VLBIunWesw0a1ZHqF82c7GmmIfUSpgotOly29DFPFJFDEhkgIT/V5mZuvj6XofKrHU6vyI4u37IYi36aN4h5tL7PJyif1dvCgEpapzISbCTEj5R78BZq5A5Ldh2XYAAAAASUVORK5CYII',
            'Smartduino UNO SMD', 'Atmega328PB microController Board','1','550', 'link']
    products.append(temp)
    products.append(temp)
    products.append(temp)

    data = {
        'order': ordr,
        'order_time': ordr.created.astimezone(IST_TZ).strftime('%d %b %Y %I:%M%p'),
        'sub_total': ordr.total_amount - ordr.delivery_charge - ordr.extra_charge,
        'products': products
    }

    template = get_template('email_confirm.html')
    rendered_data = template.render(data)
    return rendered_data



def test_mail_web(request):
    ordr = Orders.objects.all()[0]

    rendered_data = get_order_confirm_data(ordr)

    return HttpResponse(rendered_data)