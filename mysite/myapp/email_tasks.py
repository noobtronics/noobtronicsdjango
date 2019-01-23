from django.core.mail import send_mail, EmailMultiAlternatives
from products.models import *
import pytz
from django.template import Context, Template
from django.template.loader import get_template
from django.http import HttpResponse
from email.mime.image import MIMEImage
import queue
import time
from datetime import datetime
from background_task import background




IST_TZ = pytz.timezone('Asia/Kolkata')



EMAIL_QUEUE = queue.Queue()


@background(schedule=10)
def send_confirm_mail(ordr_id):
    ordr = Orders.objects.get(id=ordr_id)

    if ordr.email_sent_confirm:
        return

    rendered_data, images_data = get_order_confirm_data(ordr)

    message = EmailMultiAlternatives(
        subject='Your noobtronics.ltd order - #{0} has been received'.format(ordr.order_id),
        body='',
        from_email='Noobtronics Shop <no-reply@noobtronics.ltd>',
        to=[ordr.user_id.email],
        bcc=['noobtronics12@gmail.com'],
    )

    message.content_subtype = "html"
    message.attach_alternative(rendered_data, "text/html")
    message.attach(logo_data())
    for img in images_data:
        message.attach(get_img_data(img['path'], img['id']))

    message.send(fail_silently=False)
    ordr.email_sent_confirm = True
    ordr.save()



def logo_data():
    with open('static/images/logo_email.png', 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    return logo


def get_img_data(path, cid):
    with open('media/..'+path, 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<{0}>'.format(cid))
    return logo



def get_order_confirm_data(ordr):
    order_prods = OrderProducts.objects.filter(order_id=ordr)

    products = []
    images_data = []

    for op in order_prods:
        temp = ['cid:{0}'.format(op.prod_id.id),
                op.prod_id.name, op.prod_id.pagetitle,op.quantity,op.subtotal, 'https://noobtronics.ltd/product/'+op.prod_id.slug]
        products.append(temp)

        temp_i = {
            'id': op.prod_id.id,
            'path': op.prod_id.mainimage.img_data.th_micro.image.url
        }
        images_data.append(temp_i)

    data = {
        'order': ordr,
        'order_time': ordr.created.astimezone(IST_TZ).strftime('%d %b %Y %I:%M%p'),
        'sub_total': ordr.total_amount - ordr.delivery_charge - ordr.extra_charge,
        'products': products,
        'images_data': images_data,
    }

    template = get_template('email_confirm.html')
    rendered_data = template.render(data)
    return rendered_data, images_data



def test_mail_web(request):
    ordr = Orders.objects.all()[0]

    rendered_data, images_data = get_order_confirm_data(ordr)

    return HttpResponse(rendered_data)