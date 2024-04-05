import os

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page
from app.models import Staff, User

GENDER_CHOICES = {
    'M': '男',
    'F': '女',
    'U': '未知',}
# 工作人员信息管理
def add_worker(request):
    if request.method == "GET":
        return render(request, "manager/worker_management/add_worker.html")

    # 获取表单数据
    created_by_id = request.session["info"]["user_id"]
    created_by=User.objects.filter(user_id=created_by_id).first()
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
    staff_photo = request.FILES.get('pic1') or None
    if staff_photo:
        _, ext = os.path.splitext(staff_photo.name)
        # 使用用户的电话号码作为文件名，保留原始文件的扩展名
        staff_photo.name = f"{mobile_phone}_{now().strftime('%Y%m%d%H%M%S')}{ext}"

    if Staff.objects.filter(id_card=id_card).exists() or Staff.objects.filter(mobile_phone=mobile_phone).exists():
        context = {
            'ret': 2,
            'msg': "该员工信息已经录入过了"
        }
        return JsonResponse(context, safe=False)

    # 创建Elder实例并保存
    staff = Staff(
        username=username,
        gender=gender if gender in ['M', 'F'] else 'U',
        mobile_phone=mobile_phone,
        phone=phone,
        id_card=id_card,
        birthday=birthday,
        hire_date=hire_date,
        resign_date=resign_date,
        staff_photo=staff_photo,
        description=description,
        created_by=created_by,
        is_active=True
    )
    staff.save()

    context = {
        'ret': 1,
        'msg': "录入成功"
    }
    return JsonResponse(context, safe=False)


def list_worker(request):
    staff = Staff.objects.filter(is_active=True)
    page_obj = Pagination(request, staff, items_per_page)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "manager/worker_management/list_worker.html", context)


def modify_worker(request):
    if request.method == "GET":
        # 获取所有激活的Elder对象
        key = request.GET.get('key', '')
        if key:
            # 搜索 address, name, 或 email 字段包含关键词的用户
            staff = Staff.objects.filter(
                (Q(id__icontains=key) |
                 Q(username__icontains=key) |
                 Q(mobile_phone__icontains=key)) &
                Q(is_active=True)
            ).order_by('id')
        else:
            # 如果没有提供关键词，则返回所有用户
            staff = Staff.objects.filter(is_active=True).order_by('id')

        page_obj = Pagination(request, staff, items_per_page)
        context = {
            "page_obj": page_obj,
            "key": key
        }
        return render(request, "manager/worker_management/modify_worker.html", context)

    updated_by_id = request.session["info"]["user_id"]
    updated_by = User.objects.filter(user_id=updated_by_id).first()
    staff_id = request.POST.get("id")
    staff = Staff.objects.filter(id=staff_id).first()
    staff.is_active = False
    staff.updated_by=updated_by
    staff.save()
    context = {
        'ret': 1,
        'msg': "删除成功"
    }
    return JsonResponse(context, safe=False)


def analyze_worker(request):
    return render(request, "manager/worker_management/analyze_worker.html")


def modify_worker_basic(request):
    if request.method == 'GET':
        staff_id = request.GET.get('id')
        staff =get_object_or_404(Staff, id=staff_id)
        if staff.birthday:
            age = staff.calculate_age()
        else:
            age = None
        staff.gender = GENDER_CHOICES[staff.gender]
        context = {
            'item': staff,
            'age': age
        }
        return render(request, "manager/worker_management/modify_worker_basic.html",context)

    updated_by_id = request.session["info"]["user_id"]
    updated_by=User.objects.filter(user_id=updated_by_id).first()
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
    is_exists = Staff.objects.filter(id=id)
    if is_exists.exists():
        item = is_exists.first()
        if uploaded_file:
            _, ext = os.path.splitext(uploaded_file.name)

            # 使用用户的电话号码作为文件名，保留原始文件的扩展名
            uploaded_file.name = f"{mobile_phone}_{now().strftime('%Y%m%d%H%M%S')}{ext}"
            item.staff_photo.save(uploaded_file.name, uploaded_file, save=True)
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


def worker_info(request):
    old_id = request.GET.get('id')
    staff = Staff.objects.filter(id=old_id).first()
    if staff.birthday:
        age = staff.calculate_age()
    else:
        age = None
    staff.gender = GENDER_CHOICES[staff.gender]
    context = {
        'item': staff,
        'age': age
    }
    return render(request, "manager/worker_management/worker_info.html", context)


def select_worker(request):
    return render(request, "manager/worker_management/select_worker.html")

