from django.shortcuts import render, redirect
from django.http import HttpResponse
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.http import HttpResponseForbidden
from django.http import JsonResponse


@ensure_csrf_cookie
def home_page(request):
    context = {
        'loggedin': request.user.is_authenticated
    }
    return render(request, 'home-page.html', context)



def login_view(request):
    signed_in = False
    data = json.loads(request.body.decode('utf-8'))
    idinfo = id_token.verify_oauth2_token(data['id_token'], requests.Request(), settings.GOOGLE_API_CLIENT_ID)

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        return HttpResponseForbidden()
    user = User.objects.filter(email=idinfo['email'])
    if not user.exists():
        user = User(email=idinfo['email'], username=idinfo['email'],
                    first_name=idinfo['given_name'],
                    last_name=idinfo['family_name'])
        user.save()
    else:
        user = user[0]
    login(request, user)
    resp = {
        'success': True
    }
    print('login')
    return JsonResponse(resp)


@login_required
def logout_view(request):
    logout(request)
    resp = {
        'success': True
    }
    print('logout')
    return JsonResponse(resp)