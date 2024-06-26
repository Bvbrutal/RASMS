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
    '3': '义工用户',
    '4': '其他',
}

GENDER_CHOICES = {
    'M': '男',
    'F': '女',
    'U': '未知', }


def index(request):
    info_dic = request.session.get('info')
    mobile_phone = info_dic['mobile_phone']
    item = User.objects.filter(mobile_phone=mobile_phone).first()
    if item.grade == '2':
        return redirect('/older/index/')
    template_name = Dynamic_inheritance(request)
    context = community_information()
    context['template_name'] = template_name
    return render(request, "user/index_user.html", context)


def older_index(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    print(mobile_phone)
    elder = Elder.objects.filter(mobile_phone=mobile_phone).first()
    if elder:
        if elder.birthday:
            age = elder.calculate_age()
        else:
            age = None
        elder.gender = GENDER_CHOICES[elder.gender]
        context = {
            'item': elder,
            'age': age
        }

        return render(request, "user/older_index.html", context)
    context = {}
    return render(request, "user/older_index_none.html", context)


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


def staff_information(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    staff = Staff.objects.filter(mobile_phone=mobile_phone).first()
    if staff:
        if staff.birthday:
            age = staff.calculate_age()
        else:
            age = None
        staff.gender = GENDER_CHOICES[staff.gender]
        context = {
            'item': staff,
            'age': age
        }

        return render(request, "user/staff_index.html", context)
    context = {}
    return render(request, "user/staff_index_none.html", context)

def volunteer_information(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    volunteer = Volunteer.objects.filter(mobile_phone=mobile_phone).first()
    if volunteer:
        if volunteer.birthday:
            age = volunteer.calculate_age()
        else:
            age = None
        volunteer.gender = GENDER_CHOICES[volunteer.gender]
        context = {
            'item': volunteer,
            'age': age
        }
        return render(request, "user/volunteer_index.html", context)
    context = {}
    return render(request, "user/volunteer_index_none.html", context)