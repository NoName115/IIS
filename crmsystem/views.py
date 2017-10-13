from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


#@login_required(login_url='accounts/login/')
def default_web(request):
    return render(request, 'crmsystem/main.html', {})

def login_form(request):
    state = "Please log in below..."
    username = password = ''

    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if (user is not None):
            if (user.is_active):
                login(request, user)
                state = "You're successfully logged in!"
                return redirect('default_web')
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username or password were incorrect."

    return render(request, 'account/login.html', {
        'state': state
    })

def logout_form(request):
    logout(request)
    return render(request, 'account/logout.html', {})

def registration_form(request):
    return render(request, 'account/registration.html', {})
