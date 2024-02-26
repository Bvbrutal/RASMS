import json

from django.http import JsonResponse
from django.shortcuts import render

from app.models import UserIP, Test
from app.script.visit_info import change_info

USER_TYPES = {
        '0': '管理员',
        '1': '工作人员',
        '2': '老年用户',
        '3': '子女用户',
        '4': '义工用户',
        '5': '其他',
    }


def accont_api(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    serch_result = Test.objects.filter(mobile_phone=mobile_phone).first()
    user_id = serch_result.user_id
    username = serch_result.username
    bio = serch_result.bio
    grade = USER_TYPES[str(serch_result.grade)]
    context = {
        'username': username,
        'user_id': user_id,
        'phone': mobile_phone,
        'bio': bio,
        'grade': grade
    }
    print(context)
    return JsonResponse(context)

def index(request):

    return render(request, "page/index_user.html")


def profile(request):
    for key, value in request.session.items():
        print(f'{key}: {value}')
    mobile_phone=request.session["info"]["mobile_phone"]
    serch_result=Test.objects.filter(mobile_phone=mobile_phone).first()
    user_id=serch_result.user_id
    username=serch_result.username
    bio=serch_result.bio
    grade=USER_TYPES[str(serch_result.grade)]
    context={
        'username':username,
        'user_id':user_id,
        'phone':mobile_phone,
        'bio':bio,
        'grade':grade
    }
    return render(request, "user/profile.html",context=context)


def modify_profile(request):
    context={}
    return render(request, "user/community_activity.html", context=context)


def community_activity(request):
    context = {}
    return render(request, "user/community_activity.html", context=context)


def update_profile(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    serch_result = Test.objects.filter(mobile_phone=mobile_phone).first()
    data = json.loads(request.body)
    print(data["creation_time"])
    data = {'message': '处理成功'}
    return JsonResponse(data, status=200)  # 成功响应