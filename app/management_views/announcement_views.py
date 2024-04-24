import os

from django.http import JsonResponse
from django.shortcuts import render

from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page
from app.models import CommunityAnnouncement, User

from django.utils.timezone import now

def announcement_list(request):
    communityAnnouncements = CommunityAnnouncement.objects.filter(is_active=True).order_by("-published_date")
    context = {
        "items": communityAnnouncements
    }
    return render(request, "manager/announcement/announcement_list.html", context)


def announcement_info(request):
    id = request.GET.get("id")
    item = CommunityAnnouncement.objects.filter(id=id).first()
    context = {
        'item': item
    }
    return render(request, "manager/announcement/announcement_info.html", context)

import re
def announcement_add(request):
    if request.method == "GET":
        context = {

        }
        return render(request, "manager/announcement/announcement_add.html", context)
    # 从请求数据中获取字段值
    title = request.POST.get('title')
    introduction=request.POST.get('introduction') or None
    content = request.POST.get('content')
    publisher = request.POST.get('publisher') or None
    published_date = request.POST.get('published_date') or None
    expiry_date = request.POST.get('expiry_date') or None
    status = request.POST.get('status') or None
    author_id = request.session["info"]["user_id"]
    author = User.objects.filter(user_id=author_id).first()
    content_text = re.sub('<[^<]+?>', '', content.strip())
    is_active=request.POST.get('is_active') or True
    # 获取上传的文件
    uploaded_file = request.FILES.get('pic1') or None
    created_by_id=request.session["info"]["user_id"]
    updated_by_id=created_by_id
    print(updated_by_id)
    if uploaded_file:
        _, ext = os.path.splitext(uploaded_file.name)

        # 使用用户的电话号码作为文件名，保留原始文件的扩展名
        uploaded_file.name = f"{now().strftime('%Y%m%d%H%M%S')}{ext}"
    if introduction is None:
        introduction=content_text[:30]
    if is_active=='false':
        is_active=False
    CA = CommunityAnnouncement(
        title=title,
        content=content,
        published_date=published_date,
        expiry_date=expiry_date,
        author=author,
        publisher=publisher,
        status=status,
        introduction=introduction,
        announcement_photo=uploaded_file,
        is_active=is_active,
        created_by_id=created_by_id,
        updated_by_id=updated_by_id
    )
    CA.save()
    print(title, content, publisher, published_date, author)
    context = {
        'ret': 1,
        'msg': "录入成功"
    }
    return JsonResponse(context, safe=False, status=200)


def announcement_modify(request):
    communityAnnouncements = CommunityAnnouncement.objects.all().order_by("-published_date")
    page_obj = Pagination(request, communityAnnouncements, items_per_page)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "manager/announcement/announcement_modify.html", context)


def announcement_modify_basic(request):
    id = request.GET.get('id')
    communityAnnouncement = CommunityAnnouncement.objects.filter(id=id,is_active=True).first()
    context = {
        "item": communityAnnouncement,
    }
    return render(request, "manager/announcement/announcement_modify_basic.html", context)