# 老年人信息管理
import hashlib
import os
from datetime import datetime

from django.db.models import Q, Count
from django.db.models.functions import TruncYear, TruncMonth
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.timezone import now

from app.components.Dynamic_inheritance import Dynamic_inheritance
from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page
from app.models import Elder, User

GENDER_CHOICES = {
    'M': '男',
    'F': '女',
    'U': '未知', }


def add_old(request):
    if request.method == "GET":
        context={

        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/elder_management/add_old.html",context)

    # 获取表单数据
    created_by_id = request.session["info"]["user_id"]
    created_by = User.objects.filter(user_id=created_by_id).first()
    username = request.POST.get('input1')
    gender = 'M' if request.POST.get('gridRadios') == 'option1' else 'F'
    mobile_phone = request.POST.get('input2')
    id_card = request.POST.get('input3')
    birthday = request.POST.get('input4') or None
    checkin_date = request.POST.get('input5') or None
    checkout_date = request.POST.get('input6') or None
    phone = request.POST.get('input7') or None
    room_number = request.POST.get('input8') or None
    firstguardian_name = request.POST.get('input9') or None
    firstguardian_relationship = request.POST.get('input10') or None
    firstguardian_phone = request.POST.get('input11') or None
    firstguardian_wechat = request.POST.get('input12') or None
    secondguardian_name = request.POST.get('input13') or None
    secondguardian_relationship = request.POST.get('input14') or None
    secondguardian_phone = request.POST.get('input15') or None
    secondguardian_wechat = request.POST.get('input16') or None
    health_state = request.POST.get('input17') or None
    description = request.POST.get('input18') or None

    # 获取上传的文件
    uploaded_file = request.FILES.get('pic1') or None
    if uploaded_file:
        _, ext = os.path.splitext(uploaded_file.name)

        # 使用用户的电话号码作为文件名，保留原始文件的扩展名
        uploaded_file.name = f"{mobile_phone}_{now().strftime('%Y%m%d%H%M%S')}{ext}"
    if Elder.objects.filter(id_card=id_card).exists() or Elder.objects.filter(mobile_phone=mobile_phone).exists():
        context = {
            'ret': 2,
            'msg': "该老人信息已经录入过了"
        }
        return JsonResponse(context, safe=False)
    # 创建Elder实例并保存
    elder = Elder(
        username=username,
        gender=gender if gender in ['M', 'F'] else 'U',
        mobile_phone=mobile_phone,
        phone=phone,
        id_card=id_card,
        birthday=birthday,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        elder_photo=uploaded_file,
        room_number=room_number,
        firstguardian_name=firstguardian_name,
        firstguardian_relationship=firstguardian_relationship,
        firstguardian_phone=firstguardian_phone,
        firstguardian_wechat=firstguardian_wechat,
        secondguardian_name=secondguardian_name,
        secondguardian_relationship=secondguardian_relationship,
        secondguardian_phone=secondguardian_phone,
        secondguardian_wechat=secondguardian_wechat,
        health_state=health_state,
        description=description,
        created_by=created_by,
    )
    elder.save()
    context = {
        'ret': 1,
        'msg': "录入成功"
    }
    return JsonResponse(context, safe=False)


def select_old(request):
    key = request.GET.get('key', '')
    if key:
        # 搜索 address, name, 或 email 字段包含关键词的用户
        elders = Elder.objects.filter(
            (Q(id__icontains=key) |
             Q(username__icontains=key) |
             Q(room_number__icontains=key)) &
            Q(is_active=True)
        ).order_by('id')
    else:
        # 如果没有提供关键词，则返回所有用户
        elders = Elder.objects.filter(is_active=True).order_by('id')

    page_obj = Pagination(request, elders, items_per_page)
    context = {
        "page_obj": page_obj,
        "key": key
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/elder_management/select_old.html", context=context)


def modify_old(request):
    if request.method == "GET":
        key = request.GET.get('key', '')
        if key:
            # 搜索 address, name, 或 email 字段包含关键词的用户
            elders = Elder.objects.filter(
                (Q(id__icontains=key) |
                 Q(username__icontains=key) |
                 Q(room_number__icontains=key)) &
                Q(is_active=True)
            ).order_by('id')
        else:
            # 如果没有提供关键词，则返回所有用户
            elders = Elder.objects.filter(is_active=True).order_by('id')

        page_obj = Pagination(request, elders, items_per_page)
        context = {
            "page_obj": page_obj,
            "key": key
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/elder_management/modify_old.html", context=context)

    updated_by_id = request.session["info"]["user_id"]
    updated_by = User.objects.filter(user_id=updated_by_id).first()
    old_id = request.POST.get("id")
    op = request.POST.get("op")
    elder = Elder.objects.filter(id=old_id).first()
    try:
        if op == 'delete_elder':
            elder.is_active = False
            elder.updated_by = updated_by
            elder.save()
            context = {
                'ret': 1,
                'msg': "删除成功"
            }

            return JsonResponse(context, safe=False)
        # if op == 'reset_password':
        #     if elder.bind_user:
        #         elder.updated_by = updated_by
        #         elder.bind_user.password = hashlib.md5('123456'.encode()).hexdigest()
        #         elder.save()
        #         context = {
        #             'ret': 1,
        #             'msg': "重置成功"
        #         }
        #         return JsonResponse(context, safe=False)
        #     context = {
        #         'ret': 2,
        #         'msg': "该用户未注册"
        #     }
        #     return JsonResponse(context, safe=False)
    except:
        context = {
            'ret': 3,
            'msg': "删除失败"
        }
        return JsonResponse(context, safe=False)


def analyze_old(request):
    # 年龄分布
    age_distribution = [0, 0, 0, 0, 0]
    for elder in Elder.objects.filter(is_active=True):
        if elder.birthday:
            age = elder.calculate_age()
            if age <= 20:
                age_distribution[0] += 1
            elif 21 <= age <= 40:
                age_distribution[1] += 1
            elif 41 <= age <= 60:
                age_distribution[2] += 1
            elif 61 <= age <= 80:
                age_distribution[3] += 1
            else:
                age_distribution[4] += 1

    # 近八年的流入流出统计
    # 获取当前年份
    current_year = datetime.now().year
    year_range = range(current_year - 7, current_year + 1)
    checkin_counts = Elder.objects.filter(
        checkin_date__year__gte=current_year - 7,
        checkin_date__year__lte=current_year
    ).annotate(
        year=TruncYear('checkin_date')
    ).values('year').annotate(
        count=Count('id')
    ).order_by('year')
    checkout_counts = Elder.objects.filter(
        checkout_date__year__gte=current_year - 7,
        checkout_date__year__lte=current_year,
        checkout_date__isnull=False  # 排除空值
    ).annotate(
        year=TruncYear('checkout_date')
    ).values('year').annotate(
        count=Count('id')
    ).order_by('year')
    checkin_data = {entry['year'].year: entry['count'] for entry in checkin_counts}
    checkout_data = {entry['year'].year: entry['count'] for entry in checkout_counts}
    final_checkin_data = [checkin_data.get(year, 0) for year in year_range]
    final_checkout_data = [checkout_data.get(year, 0) for year in year_range]
    year_range_list = [year for year in year_range]

    # 去年一整年不同月份老人流入流出
    last_year = datetime.now().year - 1
    checkin_counts = Elder.objects.filter(
        checkin_date__year=last_year
    ).annotate(
        month=TruncMonth('checkin_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    # 计算去年的离院人数
    checkout_counts = Elder.objects.filter(
        checkout_date__year=last_year
    ).annotate(
        month=TruncMonth('checkout_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    # 转换查询结果为字典，键为月份
    checkin_counts_dict = {c['month'].month: c['count'] for c in checkin_counts}
    checkout_counts_dict = {c['month'].month: c['count'] for c in checkout_counts}
    # 初始化一个包含所有月份的计数字典
    all_months_counts1 = {month: 0 for month in range(1, 13)}
    all_months_counts2 = {month: 0 for month in range(1, 13)}
    # 更新字典，使用查询结果覆盖默认的零计数
    all_months_counts1.update(checkin_counts_dict)
    all_months_counts2.update(checkout_counts_dict)
    # 将查询结果转换为更易于处理的格式，例如字典列表
    checkin_data = [count for month, count in all_months_counts1.items()]
    checkout_data = [count for month, count in all_months_counts2.items()]
    context = {
        'age_distribution': age_distribution,
        'final_checkin_data': final_checkin_data,
        'final_checkout_data': final_checkout_data,
        'year_range_list': year_range_list,
        'checkin_data': checkin_data,
        'checkout_data': checkout_data,
        'check_year': last_year
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/elder_management/analyze_old.html", context)


def old_info(request):
    id = request.GET.get('id')
    elder1 = Elder.objects.filter(mobile_phone=id).first()
    elder2 = Elder.objects.filter(id=id).first()
    elder=elder1 if elder1 else elder2
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
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/elder_management/old_info.html", context=context)
    context={}
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/elder_management/elder_info_none.html",context)


def list_old(request):
    # 获取所有激活的Elder对象
    elders = Elder.objects.filter(is_active=True)
    page_obj = Pagination(request, elders, items_per_page)
    context = {
        "page_obj": page_obj,
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/elder_management/list_old.html", context=context)


def modify_old_basic(request):
    if request.method == "GET":
        old_id = request.GET.get('id')
        elder = get_object_or_404(Elder, id=old_id)
        if elder.birthday:
            age = elder.calculate_age()
        else:
            age = None
        elder.gender = GENDER_CHOICES[elder.gender]
        context = {
            'item': elder,
            'age': age
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/elder_management/modify_old_basic.html", context)
        # 获取表单数据
    updated_by_id = request.session["info"]["user_id"]
    updated_by = User.objects.filter(user_id=updated_by_id).first()
    id = request.POST.get('id')
    username = request.POST.get('input1')
    gender = 'M' if request.POST.get('gridRadios') == 'option1' else 'F'
    mobile_phone = request.POST.get('input2')
    id_card = request.POST.get('input3')
    birthday = request.POST.get('input4') or None
    checkin_date = request.POST.get('input5') or None
    checkout_date = request.POST.get('input6') or None
    phone = request.POST.get('input7') or None
    room_number = request.POST.get('input8') or None
    health_state = request.POST.get('input17') or None
    description = request.POST.get('input18') or None

    # 获取上传的文件
    uploaded_file = request.FILES.get('pic1') or None
    is_exists = Elder.objects.filter(id=id)
    if is_exists.exists():
        item = is_exists.first()
        if uploaded_file:
            _, ext = os.path.splitext(uploaded_file.name)

            # 使用用户的电话号码作为文件名，保留原始文件的扩展名
            uploaded_file.name = f"{mobile_phone}_{now().strftime('%Y%m%d%H%M%S')}{ext}"
            item.elder_photo.save(uploaded_file.name, uploaded_file, save=True)
        # 更新模型实例的字段
        item.username = username
        item.gender = gender if gender in ['M', 'F'] else 'U'
        item.mobile_phone = mobile_phone
        item.phone = phone
        item.id_card = id_card
        item.birthday = birthday
        item.checkin_date = checkin_date
        item.checkout_date = checkout_date
        item.room_number = room_number
        item.health_state = health_state
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


def modify_old_guardian(request):
    if request.method == 'GET':
        old_id = request.GET.get('id')
        elder = get_object_or_404(Elder, id=old_id)
        if elder.birthday:
            age = elder.calculate_age()
        else:
            age = None
        elder.gender = GENDER_CHOICES[elder.gender]
        context = {
            'item': elder,
            'age': age
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/elder_management/modify_old_guardian.html", context)
    id = request.POST.get('id')
    firstguardian_name = request.POST.get('input9') or None
    firstguardian_relationship = request.POST.get('input10') or None
    firstguardian_phone = request.POST.get('input11') or None
    firstguardian_wechat = request.POST.get('input12') or None
    secondguardian_name = request.POST.get('input13') or None
    secondguardian_relationship = request.POST.get('input14') or None
    secondguardian_phone = request.POST.get('input15') or None
    secondguardian_wechat = request.POST.get('input16') or None
    is_exists = Elder.objects.filter(id=id)
    if is_exists.exists():
        item = is_exists.first()
        item.firstguardian_name = firstguardian_name
        item.firstguardian_relationship = firstguardian_relationship
        item.firstguardian_phone = firstguardian_phone
        item.firstguardian_wechat = firstguardian_wechat
        item.secondguardian_name = secondguardian_name
        item.secondguardian_relationship = secondguardian_relationship
        item.secondguardian_phone = secondguardian_phone
        item.secondguardian_wechat = secondguardian_wechat
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
