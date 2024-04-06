import hashlib

from django.shortcuts import render

from app.models import User
from django.db.models import Q, Count
from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page
from django.http import JsonResponse


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
    if op == 'delete_elder':
        item.is_active = False
        item.updated_by = updated_by
        item.save()
        context = {
            'ret': 1,
            'msg': "删除成功"
        }

        return JsonResponse(context, safe=False)
    if op == 'reset_password':
        if item.bind_user:
            item.updated_by = updated_by
            item.bind_user.password = hashlib.md5('123456'.encode()).hexdigest()
            item.save()
            context = {
                'ret': 1,
                'msg': "重置成功"
            }
            return JsonResponse(context, safe=False)
        context = {
            'ret': 2,
            'msg': "该用户未注册"
        }
        return JsonResponse(context, safe=False)
    return render(request, "manager/account_management/account_modify.html")


def account_analyze(request):
    return render(request, "manager/account_management/account_analyze.html")


def account_info(request):
    id = request.GET.get('id')
    item = User.objects.filter(user_id=id).first()
    if item:
        context = {
            'item': item,
        }
        return render(request, "manager/account_management/account_info.html", context=context)
    return render(request, "manager/account_management/account_info_none.html")


def account_add(request):
    return render(request, "manager/account_management/account_add.html")

