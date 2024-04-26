import json
import os

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from app.components.Pagination import Pagination
from app.models import User, Elder, Staff, Volunteer, CommunityEvent, CommunityAnnouncement

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
    return render(request, "elder/profile.html", context=context)


def modify_regional(request):
    context = {

    }
    return render(request, "elder/modify_regional.html", context=context)


def activity_list(request):
    communityEvent=CommunityEvent.objects.all().order_by("-created")
    print(communityEvent)
    context={
        'communityEvent':communityEvent
    }

    return render(request,"elder/activity_list.html",context)

def announcement_list(request):
    communityAnnouncements = CommunityAnnouncement.objects.filter(is_active=True).order_by("-published_date")
    context = {
        "items": communityAnnouncements
    }
    return render(request, "elder/announcement_list.html", context)


def medication_list(request):
    context = {

    }
    return render(request, "elder/medication_list.html", context=context)

def modify_service(request):
    context = {

    }
    return render(request, "elder/modify_service.html", context=context)

