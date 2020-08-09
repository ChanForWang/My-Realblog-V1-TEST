from django.contrib import auth
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm, RegForm
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('blog:index')))
    else:
        login_form = LoginForm()
    return render(request, 'login.html', locals())

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username,email,password)
            user.save()
            #登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('blog:index')))

            # 第二种保存用户到后台的方法
            '''
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
            '''
    else:
        reg_form = RegForm()
    return render(request, 'register.html', locals())


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('blog:index')))


def user_info(request):
    return render(request, 'user_info.html',locals())