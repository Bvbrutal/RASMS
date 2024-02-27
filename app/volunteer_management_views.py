# 义工信息管理
import os

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

from app.components.Pagination import Pagination
from app.configuration import items_per_page
from app.models import Volunteer, Test

from django.db.models import Q

GENDER_CHOICES = {
    'M': '男',
    'F': '女',
    'U': '未知',}
def add_volunteer(request):
    if request.method == "GET":
        return render(request, "manager/volunteer_management/add_volunteer.html")

    # 获取表单数据
    username = request.POST.get('input1')
    gender = 'M' if request.POST.get('gridRadios') == 'option1' else 'F'
    mobile_phone = request.POST.get('input2')
    id_card = request.POST.get('input3')
    phone = request.POST.get('input4')
    birthday = request.POST.get('input5') or None
    hire_date = request.POST.get('input6') or None
    resign_date = request.POST.get('input7') or None
    description = request.POST.get('input8') or None

    # 获取上传的文件
    volunteer_photo = request.FILES.get('pic1') or None
    if volunteer_photo:
        _, ext = os.path.splitext(volunteer_photo.name)
        # 使用用户的电话号码作为文件名，保留原始文件的扩展名
        volunteer_photo.name = f"{mobile_phone}_{now().strftime('%Y%m%d%H%M%S')}{ext}"

    if Volunteer.objects.filter(id_card=id_card).exists() or Volunteer.objects.filter(
            mobile_phone=mobile_phone).exists():
        context = {
            'ret': 2,
            'msg': "该义工信息已经录入过了"
        }
        return JsonResponse(context, safe=False)

    # 创建Elder实例并保存
    volunteer = Volunteer(
        username=username,
        gender=gender if gender in ['M', 'F'] else 'U',
        mobile_phone=mobile_phone,
        phone=phone,
        id_card=id_card,
        birthday=birthday,
        hire_date=hire_date,
        resign_date=resign_date,
        volunteer_photo=volunteer_photo,
        description=description,
        is_active=True
    )
    volunteer.save()

    context = {
        'ret': 1,
        'msg': "录入成功"
    }
    return JsonResponse(context, safe=False)


def list_volunteer(request):
    volunteer = Volunteer.objects.filter(is_active=True)
    page_obj = Pagination(request, volunteer, items_per_page)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "manager/volunteer_management/list_volunteer.html", context)


def select_volunteer(request):
    return render(request, "manager/volunteer_management/select_volunteer.html")


def modify_volunteer(request):
    if request.method == "GET":
        # 获取所有激活的Elder对象
        key = request.GET.get('key', '')
        if key:
            # 搜索 address, name, 或 email 字段包含关键词的用户
            volunteer = Volunteer.objects.filter(
                (Q(id__icontains=key) |
                 Q(username__icontains=key) |
                 Q(mobile_phone__icontains=key)) &
                Q(is_active=True)
            ).order_by('id')
        else:
            # 如果没有提供关键词，则返回所有用户
            volunteer = Volunteer.objects.filter(is_active=True).order_by('id')

        page_obj = Pagination(request, volunteer, items_per_page)
        context = {
            "page_obj": page_obj,
            "key": key
        }
        return render(request, "manager/volunteer_management/modify_volunteer.html",context)

    volunteer_id = request.POST.get("id")
    volunteer = Volunteer.objects.filter(id=volunteer_id).first()
    volunteer.is_active = False
    volunteer.save()
    context = {
        'ret': 1,
        'msg': "删除成功"
    }
    return JsonResponse(context, safe=False)


def analyze_volunteer(request):
    return render(request, "manager/volunteer_management/analyze_volunteer.html")


def volunteer_info(request):
    volunteer_id = request.GET.get('id')
    volunteer = Volunteer.objects.filter(id=volunteer_id).first()
    if volunteer.birthday:
        age = volunteer.calculate_age()
    else:
        age = None
    volunteer.gender = GENDER_CHOICES[volunteer.gender]
    context = {
        'item': volunteer,
        'age': age
    }
    return render(request, "manager/volunteer_management/volunteer_info.html", context)


def modify_volunteer_basic(request):
    if request.method == 'GET':
        volunteer_id = request.GET.get('id')
        volunteer =get_object_or_404(Volunteer, id=volunteer_id)
        if volunteer.birthday:
            age = volunteer.calculate_age()
        else:
            age = None
        volunteer.gender = GENDER_CHOICES[volunteer.gender]
        context = {
            'item': volunteer,
            'age': age
        }
        return render(request, "manager/volunteer_management/modify_volunteer_basic.html",context)
    updated_by_mobile_phone = request.session["info"]["mobile_phone"]
    updated_by=Test.objects.filter(mobile_phone=updated_by_mobile_phone).first().username
    id = request.POST.get('id')
    username = request.POST.get('input1')
    gender = 'M' if request.POST.get('gridRadios') == 'option1' else 'F'
    mobile_phone = request.POST.get('input2')
    id_card = request.POST.get('input3')
    birthday = request.POST.get('input4') or None
    hire_date = request.POST.get('input5') or None
    resign_date = request.POST.get('input6') or None
    phone = request.POST.get('input7') or None
    description = request.POST.get('input18') or None
    # 获取上传的文件
    uploaded_file = request.FILES.get('pic1') or None
    is_exists = Volunteer.objects.filter(id=id)
    if is_exists.exists():
        item = is_exists.first()
        if uploaded_file:
            _, ext = os.path.splitext(uploaded_file.name)

            # 使用用户的电话号码作为文件名，保留原始文件的扩展名
            uploaded_file.name = f"{mobile_phone}_{now().strftime('%Y%m%d%H%M%S')}{ext}"
            item.volunteer_photo.save(uploaded_file.name, uploaded_file, save=True)
        item.username = username
        item.gender = gender if gender in ['M', 'F'] else 'U'
        item.mobile_phone = mobile_phone
        item.phone = phone
        item.id_card = id_card
        item.birthday = birthday
        item.hire_date = hire_date
        item.resign_date = resign_date
        item.description = description
        item.updated_by = updated_by
        item.save()
        context = {
            'ret': 1,
            'msg': "修改成功"
        }
        return JsonResponse(context, safe=False)
    context = {
        'ret': 2,
        'msg': "修改失败"
    }
    return JsonResponse(context, safe=False)

