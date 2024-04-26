import hashlib
import os

from django.shortcuts import render
from django.utils.timezone import now

from app.models import User
from django.db.models import Q, Count
from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page
from django.http import JsonResponse
from django.db.models.functions import TruncYear, TruncMonth
from datetime import datetime


def account_modify(request):
    if request.method == "GET":
        key = request.GET.get('key', '')
        if key:
            # 搜索 address, name, 或 email 字段包含关键词的用户
            items = User.objects.filter(
                (Q(user_id__icontains=key) |
                 Q(username__icontains=key) |
                 Q(mobile_phone__icontains=key)) &
                Q(is_active=True)
            ).order_by('id')
        else:
            # 如果没有提供关键词，则返回所有用户
            items = User.objects.filter(is_active=True).order_by('user_id')

        page_obj = Pagination(request, items, items_per_page)
        context = {
            "page_obj": page_obj,
            "key": key
        }
        return render(request, "manager/account_management/account_modify.html", context=context)

    updated_by_id = request.session["info"]["user_id"]
    updated_by = User.objects.filter(user_id=updated_by_id).first()
    id = request.POST.get("id")
    op = request.POST.get("op")
    item = User.objects.filter(user_id=id).first()
    if op == 'delete_account':
        item.is_active = False
        item.updated_by = updated_by
        item.save()
        context = {
            'ret': 1,
            'msg': "删除成功"
        }

        return JsonResponse(context, safe=False)
    if op == 'reset_password':
        item.password = hashlib.md5('123456'.encode()).hexdigest()
        item.save()
        context = {
            'ret': 1,
            'msg': "重置成功"
        }
        return JsonResponse(context, safe=False)
    return render(request, "manager/account_management/account_modify.html")


def account_analyze(request):
    # 近八年的流入流出统计
    # 获取当前年份
    current_year = datetime.now().year
    year_range = range(current_year - 7, current_year + 1)
    checkin_counts = User.objects.filter(
        creation_time__year__gte=current_year - 7,
        creation_time__year__lte=current_year
    ).annotate(
        year=TruncYear('creation_time')
    ).values('year').annotate(
        count=Count('user_id')
    ).order_by('year')

    checkin_data = {entry['year'].year: entry['count'] for entry in checkin_counts}
    final_checkin_data = [checkin_data.get(year, 0) for year in year_range]
    year_range_list = [year for year in year_range]

    # 去年一整年不同月份老人流入流出
    last_year = datetime.now().year - 1
    checkin_counts = User.objects.filter(
        creation_time__year=last_year
    ).annotate(
        month=TruncMonth('creation_time')
    ).values('month').annotate(
        count=Count('user_id')
    ).order_by('month')

    # 转换查询结果为字典，键为月份
    checkin_counts_dict = {c['month'].month: c['count'] for c in checkin_counts}

    # 初始化一个包含所有月份的计数字典
    all_months_counts1 = {month: 0 for month in range(1, 13)}
    # 更新字典，使用查询结果覆盖默认的零计数
    all_months_counts1.update(checkin_counts_dict)

    print(all_months_counts1)
    # 将查询结果转换为更易于处理的格式，例如字典列表
    checkin_data = [count for month, count in all_months_counts1.items()]
    context = {
        'final_checkin_data': final_checkin_data,
        'year_range_list': year_range_list,
        'checkin_data': checkin_data,
        'check_year': last_year
    }
    print(context)
    return render(request, "manager/account_management/account_analyze.html",context)


def account_info(request):
    id = request.GET.get('id')
    if id:
        item = User.objects.filter(user_id=id).first()
        print(item.get_grade_display())
        print(item.get_gender_display())
        if item:
            context = {
                'item': item,
            }
            return render(request, "manager/account_management/account_info.html", context=context)
    return render(request, "manager/account_management/account_info_none.html")


def account_add(request):
    if request.method == 'POST':
        username = request.POST.get('input1')
        grade = request.POST.get('userType')
        gender = 'M' if request.POST.get('gridRadios') == 'option1' else 'F'
        mobile_phone = request.POST.get('input2')
        email = request.POST.get('input3') or None
        phone = request.POST.get('input4') or None
        uploaded_file = request.FILES.get('pic1') or None
        if uploaded_file:
            _, ext = os.path.splitext(uploaded_file.name)

            # 使用用户的电话号码作为文件名，保留原始文件的扩展名
            uploaded_file.name = f"{mobile_phone}_{now().strftime('%Y%m%d%H%M%S')}{ext}"
        if User.objects.filter(mobile_phone=mobile_phone).exists():
            context = {
                'ret': 2,
                'msg': "该老人信息已经录入过了"
            }
            return JsonResponse(context, safe=False)
        # 创建用户记录
        user = User(
            username=username,
            grade=grade,
            gender=gender if gender in ['M', 'F'] else 'U',
            mobile_phone=mobile_phone,
            email=email,
            phone=phone,
            user_photo=uploaded_file
        )
        user.save()
        context = {
            'ret': 1,
            'msg': "用户注册成功"
        }
        return JsonResponse(context, safe=False)

    return render(request, "manager/account_management/account_add.html")

