import os
import re

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now

from app.components.Dynamic_inheritance import Dynamic_inheritance
from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page
from app.models import CommunityEvent, User


def activity_list(request):
    communityEvent = CommunityEvent.objects.filter(is_active=True,is_save=False).order_by("-created")
    print(communityEvent)
    context = {
        'communityEvent': communityEvent
    }

    return render(request, "manager/activity/activity_list.html", context)


def activity_info(request):
    id = request.GET.get('id')
    activity = CommunityEvent.objects.filter(id=id).first()
    context = {
        'event': activity
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/activity/activity_info.html", context)


def activity_add(request):
    if request.method == "GET":
        context = {

        }
        return render(request, "manager/activity/activity_add.html", context)
    # 从请求数据中获取字段值
    name = request.POST.get('name')
    editorContent = request.POST.get('editorContent') or None
    introduction = request.POST.get('introduction') or None
    content = request.POST.get('content')
    location = request.POST.get('location') or None
    start_time = request.POST.get('start_time') or None
    end_time = request.POST.get('end_time') or None
    organizer = request.POST.get('organizer') or None
    participant_limit = request.POST.get('participant_limit') or None
    status = request.POST.get('status') or None
    contact_info = request.POST.get('contact_info') or None
    cost = request.POST.get('cost') or None
    registration_link = request.POST.get('registration_link') or None
    is_save = request.POST.get('is_active') or False
    author = request.POST.get('author') or None
    content_text = re.sub('<[^<]+?>', '', content.strip())
    # 获取上传的文件
    uploaded_file = request.FILES.get('pic1') or None
    created_by_id = request.session["info"]["user_id"]
    updated_by_id = created_by_id
    if uploaded_file:
        _, ext = os.path.splitext(uploaded_file.name)

        # 使用用户的电话号码作为文件名，保留原始文件的扩展名
        uploaded_file.name = f"{now().strftime('%Y%m%d%H%M%S')}{ext}"
    print(start_time,end_time,type(start_time),type(end_time))
    if introduction is None:
        introduction = content_text[:20]
    if is_save == 'True':
        is_save = True
    CE = CommunityEvent(
        name=name,
        description=content,
        contact_info=contact_info,
        cost=cost,
        participant_limit=participant_limit,
        author=author,
        organizer=organizer,
        status=status,
        introduction=introduction,
        image=uploaded_file,
        is_save=is_save,
        location=location,
        registration_link=registration_link,
        created_by_id=created_by_id,
        updated_by_id=updated_by_id,
        start_time=start_time,
        end_time=end_time,
    )
    CE.save()
    context = {
        'ret': 1,
        'msg': "活动编辑成功"
    }
    return JsonResponse(context, safe=False, status=200)


def activity_modify(request):
    if request.method == "GET":
        key = request.GET.get('key', '')
        if key:
            status_mapping = {v: k for k, v in CommunityEvent.STATUS_CHOICES}
            status_key = status_mapping.get(key.capitalize(), key)  # 假设用户输入的是“有效”
            # 搜索 address, name, 或 email 字段包含关键词的用户
            communityEvent = CommunityEvent.objects.filter(
                (Q(name__icontains=key) |
                 Q(introduction__icontains=key) |
                 Q(start_time__icontains=key) |
                 Q(status=status_key) |
                 Q(id__icontains=key)) &
                Q(is_active=True)
            ).order_by("-created")
        else:
            # 如果没有提供关键词，则返回所有用户
            communityEvent = CommunityEvent.objects.filter(is_active=True).order_by("-created")

        page_obj = Pagination(request, communityEvent, items_per_page)
        context = {
            "page_obj": page_obj,
            "key": key
        }
        return render(request, "manager/activity/activity_modify.html", context)
    updated_by_id = request.session["info"]["user_id"]
    updated_by = User.objects.filter(user_id=updated_by_id).first()
    id = request.POST.get("id")
    op = request.POST.get("op")
    CA = CommunityEvent.objects.filter(id=id).first()
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


def activity_modify_basic(request):
    if request.method == "POST":
        updated_by_id = request.session["info"]["user_id"]
        id = request.POST.get('id')
        name = request.POST.get('name')
        introduction = request.POST.get('introduction') or None
        content = request.POST.get('content')
        location = request.POST.get('location') or None
        start_time = request.POST.get('start_time') or None
        end_time = request.POST.get('end_time') or None
        organizer = request.POST.get('organizer') or None
        participant_limit = request.POST.get('participant_limit') or None
        status = request.POST.get('status') or None
        contact_info = request.POST.get('contact_info') or None
        cost = request.POST.get('cost') or None
        registration_link = request.POST.get('registration_link') or None
        is_save = request.POST.get('is_active') or False
        author = request.POST.get('author') or None
        content_text = re.sub('<[^<]+?>', '', content.strip())
        # 获取上传的文件
        uploaded_file = request.FILES.get('pic1') or None
        print(start_time, end_time, type(start_time), type(end_time))
        is_exists = CommunityEvent.objects.filter(id=id)
        if is_save == 'True':
            is_save = True
        if is_exists.exists():
            item = is_exists.first()
            if uploaded_file:
                _, ext = os.path.splitext(uploaded_file.name)

                # 使用用户的电话号码作为文件名，保留原始文件的扩展名
                uploaded_file.name = f"{now().strftime('%Y%m%d%H%M%S')}{ext}"
                item.image.save(uploaded_file.name, uploaded_file, save=True)
            if introduction is None:
                introduction = content_text[:20]
            # 更新模型实例的字段
            item.name = name
            item.introduction = introduction
            item.description = content
            item.location = location
            item.start_time = start_time
            item.end_time = end_time
            item.status = status
            item.organizer = organizer
            item.participant_limit = participant_limit
            item.contact_info = contact_info
            item.cost = cost
            item.registration_link = registration_link
            item.author = author
            item.cost = cost
            item.is_save = is_save
            item.updated_by_id=updated_by_id
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
    communityAnnouncement = CommunityEvent.objects.filter(id=id).first()
    print(communityAnnouncement.is_save)
    context = {
        "event": communityAnnouncement,
    }
    return render(request, "manager/activity/activity_modify_basic.html", context)
