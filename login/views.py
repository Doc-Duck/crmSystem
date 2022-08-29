import random

from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from crm.models import Managers


def index(request):
    login_form = LoginForm(request.POST)
    if request.method == 'POST' and login_form.is_valid():
        login1 = login_form.cleaned_data['login']
        passwd = login_form.cleaned_data['passwd']
        try:
            user = User.objects.get(username__exact=login1)
        except:
            user = False
            print('Cringe')
        finally:
            if user and user.check_password(passwd):
                user = authenticate(username=login1, password=passwd)
                login(request, user)
                return redirect('/crm')
    return render(request, 'login/index.html', {'form': login_form})


def registration(request):
    register_form = RegistrationForm(request.POST)
    if request.method == 'POST' and register_form.is_valid():
        login = register_form.cleaned_data['login']
        passwd = register_form.cleaned_data['passwd']
        first_name = register_form.cleaned_data['first_name']
        last_name = register_form.cleaned_data['last_name']
        confirm_passwd = register_form.cleaned_data['passwd_repeat']
        user_list = User.objects.filter(username=login)
        print(user_list)
        if passwd == confirm_passwd and not user_list:
            messages.success(request, 'Now you can crm')
            User.objects.create_user(username=login, password=passwd, first_name=first_name, last_name=last_name)
            mng = Managers(username=login, first_name=first_name, last_name=last_name)
            mng.save()
            return redirect('/')
        else:
            messages.error(request, 'Are you tarded?')
    return render(request, 'login/registration.html', {'form': register_form})


def logout_view(request):
    logout(request)
    return redirect('/')