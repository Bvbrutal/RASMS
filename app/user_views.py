import json

from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.models import Test



USER_TYPES = {
    '0': '管理员',
    '1': '工作人员',
    '2': '老年用户',
    '3': '子女用户',
    '4': '义工用户',
    '5': '其他',
}

GENDER_CHOICES = {
    'M': '男',
    'F': '女',
    'U': '未知',}



def index(request):
    for key, value in request.session.items():
        print(f'{key}: {value}')
    info_dic=request.session.get('info')
    mobile_phone = info_dic['mobile_phone']
    if Test.objects.filter(mobile_phone=mobile_phone).first().grade == 0:
        return redirect('/manager/index/')
    return render(request, "user/index_user.html")


def profile(request):
    for key, value in request.session.items():
        print(f'{key}: {value}')
    mobile_phone = request.session["info"]["mobile_phone"]
    search_result = Test.objects.filter(mobile_phone=mobile_phone).first()
    user_id = search_result.user_id
    username = search_result.username
    phone = search_result.phone
    email = search_result.email
    bio = search_result.bio
    grade = USER_TYPES[str(search_result.grade)]
    gender = GENDER_CHOICES[search_result.gender]
    context = {
        'username': username,
        'user_id': user_id,
        'mobile_phone': mobile_phone,
        'bio': bio,
        'grade': grade,
        'phone': phone,
        'email': email,
        'gender': gender
    }
    return render(request, "user/profile.html", context=context)


def modify_profile(request):
    context = {}
    return render(request, "user/community_activity.html", context=context)


def community_activity(request):
    context = {}
    return render(request, "user/community_activity.html", context=context)


