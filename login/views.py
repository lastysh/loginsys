from django.shortcuts import render, redirect
from login import models
from login.forms import UserForm, RegisterForm
# Create your views here.

def index(request):
    if request.method == "GET":
        symbol = request.session.get('is_login', None)
        return render(request, "login/index.html", {'symbol':symbol})

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "所有字段都必须填写！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_maker(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = '密码不正确！'
            except models.User.DoesNotExist:
                message = '用户名不存在！'
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request, "login/login.html", locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = "请检查填写内容"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已存在，请重新注册！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已被注册，请选择其他邮箱注册！'
                    return render(request, 'login/register.html', locals())
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_maker(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')

### 密码加密
import hashlib

def hash_maker(str, salt="login"):
    h = hashlib.sha256()
    str += salt
    h.update(str.encode())
    return h.hexdigest()
