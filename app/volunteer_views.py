import json
import os

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from app.components.Pagination import Pagination
from app.models import User, Elder, Staff, Volunteer



from django.db.models import Count
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta



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

# pages


def profile(request):
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
    return render(request, "manager/profile.html", context=context)


def select_event(request):

    return render(request, "manager/select_event.html")


def library(request):

    return render(request, "manager/library.html")

