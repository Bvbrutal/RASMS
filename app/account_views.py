import time

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import User, Elder, Staff, Volunteer
import hashlib
from datetime import datetime


def login(request):
    if request.method == 'GET':
        info_dic = request.session.get('info')
        if info_dic:
            return redirect('/index/')
        return render(request, 'account/login.html')
    mobile_phone = request.POST.get('mobile_phone')
    passwd = request.POST.get('passwd')
    # code = request.POST.get('code')
    encrypted_passwd = hashlib.md5(passwd.encode()).hexdigest()
    user_object = User.objects.filter(mobile_phone=mobile_phone, password=encrypted_passwd).first()
    if user_object:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        request.session['info'] = {'user_id': user_object.user_id, 'mobile_phone': user_object.mobile_phone}
        context = {
            'ret': 1,
            'msg': "登陆成功"
        }
        return JsonResponse(context, safe=False)
    elif User.objects.filter(mobile_phone=mobile_phone).first() or User.objects.filter(password=passwd).first():
        context = {
            'ret': 2,
            'msg': "账号或密码错误!"
        }
        return JsonResponse(context, safe=False)
    else:
        context = {
            'ret': 3,
            'msg': "手机号未注册"
        }
        return JsonResponse(context, safe=False)


def logout(request):
    request.session.clear()
    return redirect('/login/')


def register(request):
    if request.method == 'GET':
        info_dic = request.session.get('info')
        if info_dic:
            return redirect('/index/')
        return render(request, 'account/register.html')
    if request.method == 'POST':
        mobile_phone=request.POST.get('mobile_phone')
        username=request.POST.get('username')
        passwd=request.POST.get('passwd')
        repasswd=request.POST.get('repasswd')
        user_object = User.objects.filter(mobile_phone=mobile_phone).first()
        if user_object:
            context = {
                'ret': 3,
                'msg': "账号已经注册"
            }
            return JsonResponse(context, safe=False)
        if passwd == repasswd:
            # 对密码进行MD5加密
            encrypted_passwd = hashlib.md5(passwd.encode()).hexdigest()
            # 自动绑定账号
            user_now=User.objects.create(mobile_phone=mobile_phone, username=username, password=encrypted_passwd)
            elder = Elder.objects.filter(mobile_phone=mobile_phone).first()
            staff = Staff.objects.filter(mobile_phone=mobile_phone).first()
            volunteer = Volunteer.objects.filter(mobile_phone=mobile_phone).first()

            if elder:
                elder.bind_user = user_now
                elder.save()

            if staff:
                staff.bind_user = user_now
                staff.save()

            if volunteer:
                volunteer.bind_user = user_now
                volunteer.save()
            # 将加密后的密码存储到数据库中
            context = {
                'ret': 1,
                'msg': "注册成功"
            }
            return JsonResponse(context, safe=False)
        else:
            context = {
                'ret': 2,
                'msg': "两次密码不匹配！"
            }
            return JsonResponse(context, safe=False)
    return render(request, 'account/register.html')


def modify_password(request):
    return render(request, 'account/modify_password.html')