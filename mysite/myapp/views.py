from django.shortcuts import render, redirect
from django.http import HttpResponse
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def home_page(request):
    return HttpResponse("Hello World!")


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login_page.html')
    if request.method == 'POST':
        if not ('csrfmiddlewaretoken' in request.POST and 'g-recaptcha-response' in request.POST):
            return render(request, 'login_page.html')
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login_page.html')
        except:
            return render(request, 'login_page.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponse('Logged Out')