from django.shortcuts import render
import json
from pprint import pprint
from orders_app.models import *
from django.http import JsonResponse

def add_email_subscriber_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email_s, created = EmailSubscriber.objects.get_or_create(email=data['email'])

        resp = {
            'email_token': email_s.token
        }
        return JsonResponse(resp, status=200)
    return JsonResponse(resp, status=400)
