import os

from django.http import JsonResponse
from django.shortcuts import render

from app.components.Dynamic_inheritance import Dynamic_inheritance
from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page
from app.models import CommunityAnnouncement, User
from django.db.models import Q, Count
from django.utils.timezone import now
import re


def announcement_list(request):
    communityAnnouncements = CommunityAnnouncement.objects.filter(is_active=True).order_by("-published_date")
    page_obj = Pagination(request, communityAnnouncements,4)
    context = {
        "page_obj": page_obj
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/announcement/announcement_list.html", context)


def announcement_info(request):
    id = request.GET.get("id")
    item = CommunityAnnouncement.objects.filter(id=id).first()
    context = {
        'item': item
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/announcement/announcement_info.html", context)


def announcement_add(request):
    if request.method == "GET":
        context = {

        }
        return render(request, "manager/announcement/announcement_add.html", context)
    # 从请求数据中获取字段值
    title = request.POST.get('title')
    introduction=request.POST.get('introduction') or None
    content = request.POST.get('content')
    editorContent = request.POST.get('editorContent')
    publisher = request.POST.get('publisher') or None
    published_date = request.POST.get('published_date') or None
    expiry_date = request.POST.get('expiry_date') or None
    status = request.POST.get('status') or None
    author = request.POST.get('author') or None
    content_text = re.sub('<[^<]+?>', '', content.strip())
    is_save=request.POST.get('is_active') or False
    # 获取上传的文件
    uploaded_file = request.FILES.get('pic1') or None
    created_by_id=request.session["info"]["user_id"]
    updated_by_id=created_by_id
    print(updated_by_id,editorContent)
    if uploaded_file:
        _, ext = os.path.splitext(uploaded_file.name)

        # 使用用户的电话号码作为文件名，保留原始文件的扩展名
        uploaded_file.name = f"{now().strftime('%Y%m%d%H%M%S')}{ext}"
    if introduction is None:
        introduction=content_text[:20]
    if is_save=='True':
        is_save=True
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
        is_save=is_save,
        created_by_id=created_by_id,
        updated_by_id=updated_by_id
    )
    CA.save()
    context = {
        'ret': 1,
        'msg': "公告编辑成功"
    }
    return JsonResponse(context, safe=False, status=200)


def announcement_modify(request):
    if request.method == "GET":
        key = request.GET.get('key', '')
        if key:
            status_mapping = {v: k for k, v in CommunityAnnouncement.STATUS_CHOICES}
            status_key = status_mapping.get(key.capitalize(), key)  # 假设用户输入的是“有效”
            # 搜索 address, name, 或 email 字段包含关键词的用户
            communityAnnouncements = CommunityAnnouncement.objects.filter(
                (Q(title__icontains=key) |
                 Q(introduction__icontains=key) |
                 Q(published_date__icontains=key)|
                 Q(status=status_key) |
                 Q(id__icontains=key)) &
                Q(is_active=True)
            ).order_by("-published_date")
        else:
            # 如果没有提供关键词，则返回所有用户
            communityAnnouncements = CommunityAnnouncement.objects.filter(is_active=True).order_by("-published_date")

        page_obj = Pagination(request, communityAnnouncements, items_per_page)
        context = {
            "page_obj": page_obj,
            "key": key
        }
        return render(request, "manager/announcement/announcement_modify.html", context)

    updated_by_id = request.session["info"]["user_id"]
    updated_by = User.objects.filter(user_id=updated_by_id).first()
    id = request.POST.get("id")
    op = request.POST.get("op")
    CA = CommunityAnnouncement.objects.filter(id=id).first()
    if op == 'delete':
        CA.is_active = False
        CA.updated_by = updated_by
        CA.save()
        context = {
            'ret': 1,
            'msg': "删除成功"
        }

        return JsonResponse(context, safe=False)

    context = {
        'ret': 2,
        'msg': "删除失败"
    }
    return JsonResponse(context, safe=False)

def announcement_modify_basic(request):
    if request.method == "POST":
        updated_by_id = request.session["info"]["user_id"]
        id = request.POST.get('id')
        title = request.POST.get('title')
        introduction = request.POST.get('introduction') or None
        content = request.POST.get('content')
        publisher = request.POST.get('publisher') or None
        published_date = request.POST.get('published_date') or None
        expiry_date = request.POST.get('expiry_date') or None
        status = request.POST.get('status') or None
        content_text = re.sub('<[^<]+?>', '', content.strip())
        # 获取上传的文件
        uploaded_file = request.FILES.get('pic1') or None

        is_exists = CommunityAnnouncement.objects.filter(id=id)
        is_save = request.POST.get('is_active') or True
        if is_save == 'False':
            is_save = False
        print(is_save)
        if is_exists.exists():
            item = is_exists.first()
            if uploaded_file:
                _, ext = os.path.splitext(uploaded_file.name)

                # 使用用户的电话号码作为文件名，保留原始文件的扩展名
                uploaded_file.name = f"{now().strftime('%Y%m%d%H%M%S')}{ext}"
                item.announcement_photo.save(uploaded_file.name, uploaded_file, save=True)
            if introduction is None:
                introduction = content_text[:30]
            # 更新模型实例的字段
            item.title = title
            item.introduction = introduction
            item.content = content
            item.publisher = publisher
            item.published_date = published_date
            item.expiry_date = expiry_date
            item.status = status
            item.updated_by_id = updated_by_id
            item.is_save=is_save
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

    id = request.GET.get('id')
    communityAnnouncement = CommunityAnnouncement.objects.filter(id=id).first()
    print(communityAnnouncement.is_save)
    context = {
        "item": communityAnnouncement,
    }
    return render(request, "manager/announcement/announcement_modify_basic.html", context)