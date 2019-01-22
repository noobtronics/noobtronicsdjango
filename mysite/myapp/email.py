from django.core.mail import send_mail
from products.models import *

from django.template import Context, Template
from django.template.loader import get_template
from django.http import HttpResponse


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

    data = {
        'order': ordr,
        'sub_total': ordr.total_amount - ordr.delivery_charge - ordr.extra_charge
    }

    template = get_template('email_confirm.html')
    rendered_data = template.render(data)
    return rendered_data



def test_mail_web(request):
    ordr = Orders.objects.all()[0]

    rendered_data = get_order_confirm_data(ordr)

    return HttpResponse(rendered_data)