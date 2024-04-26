import json

from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now

from app.components.Community_information import community_information
from app.components.Dynamic_inheritance import Dynamic_inheritance
from app.models import User, Elder, Staff, Volunteer

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
    template_name=Dynamic_inheritance(request)
    context=community_information()
    context['template_name']=template_name
    return render(request, "user/index_user.html",context)


def profile(request):
    for key, value in request.session.items():
        print(f'{key}: {value}')
    mobile_phone = request.session["info"]["mobile_phone"]
    search_result = User.objects.filter(mobile_phone=mobile_phone).first()
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


