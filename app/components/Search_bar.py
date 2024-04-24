from django.db.models import Q
from django.shortcuts import render

from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page


def Search_bar(request,object):
    key = request.GET.get('key', '')
    if key:
        # 搜索 address, name, 或 email 字段包含关键词的用户
        elders = object.objects.filter(
            (Q(id__icontains=key) |
             Q(username__icontains=key) |
             Q(room_number__icontains=key)) &
            Q(is_active=True)
        ).order_by('id')
    else:
        # 如果没有提供关键词，则返回所有用户
        elders = object.objects.filter(is_active=True).order_by('id')

    page_obj = Pagination(request, elders, items_per_page)
    context = {
        "page_obj": page_obj,
        "key": key
    }
    return render(request, "manager/elder_management/modify_old.html", context=context)