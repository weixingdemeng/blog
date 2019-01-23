from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from user.models import User


def register(request):
    if request.method == 'GET':
        return  render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1= request.POST.get('password1')
        password2= request.POST.get('password2')
        if username and password2 and password1:
            user = User.objects.filter(u_name=username).first()
            if user:
                msg = '您注册的用户名已经存在'
                return render(request, 'register.html', {'msg': msg})
            if password1 != password2:
                msg = '您输入的密码不一致'
                return render(request, 'register.html', {'msg': msg})
            password = make_password(password1)
            User.objects.create(u_name=username, u_password=password)
            return HttpResponseRedirect(reverse('user:login'))
        msg = '您的用户名、密码或确认密码不能为空！'
        return render(request, 'register.html', {'msg':msg})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = User.objects.filter(u_name=username).first()
            if not user:
                msg = '您输入的用户名不存在'
                return render(request, 'login.html', {'msg': msg})

            if not check_password(password, user.u_password):
                msg = '您输入的密码有误'
                return render(request, 'login.html', {'msg':msg})
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('article:article'))
        msg = '您输入的用户名或者密码不能为空'
        return render(request, 'login.html',{'msg':msg})


def index(request):
    if request.method == 'GET':
        return render(request, 'article.html')


def del_user(request,id):
    if request.method == 'POST':
        user_id = request.method.get('user_id')
        if user_id == id:
            request.session['user_id'].delete()
            User.objects.filter(pk=id).delete()
            return JsonResponse({'code':200, 'msg':'请求成功'})
