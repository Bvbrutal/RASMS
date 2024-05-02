from django.db.models import Q
from django.shortcuts import render

from app.components.Dynamic_inheritance import Dynamic_inheritance
from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page, EVENT_TYPES, OPERATION_CHOICES
from app.models import User, Logging, Event, UserIP

USER_TYPES = {
    '0': '管理员',
    '1': '工作人员',
    '2': '老年用户',
    '3': '子女用户',
    '4': '义工用户',
    '5': '其他',
}

GENDER_CHOICES = {
    'M': '男',
    'F': '女',
    'U': '未知', }


# pages


def profile(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    user_id = request.session["info"]["user_id"]
    print(mobile_phone)
    print(user_id)
    search_result = User.objects.filter(mobile_phone=mobile_phone).first()
    user_id = search_result.user_id
    username = search_result.username
    phone = search_result.phone
    email = search_result.email
    bio = search_result.bio
    grade = USER_TYPES[str(search_result.grade)]
    gender = GENDER_CHOICES[search_result.gender]

    ip_addr = UserIP.objects.filter(user_by__user_id=user_id).order_by('-created_at')
    context = {
        'username': username,
        'item': search_result,
        'user_id': user_id,
        'mobile_phone': mobile_phone,
        'bio': bio,
        'grade': grade,
        'phone': phone,
        'email': email,
        'gender': gender,
        'ip_addr': ip_addr,
    }

    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/profile.html", context=context)


def select_event(request):
    key = request.GET.get('key', '')
    filter = request.GET.get('filter', '')
    column_names = [event[1] for event in EVENT_TYPES]
    if filter:
        events = Event.objects.filter(event_type=filter, is_active=True)
        page_obj = Pagination(request, events, items_per_page)
        context = {
            'column_names': column_names,
            "page_obj": page_obj,
            "filter": filter,
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/select_event.html", context=context)

    if key:
        # 搜索 address, name, 或 email 字段包含关键词的用户
        events = Event.objects.filter(
            (Q(id__icontains=key) |
             Q(event_location__icontains=key) |
             Q(event_date__icontains=key) |
             Q(oldperson_id__icontains=key) |
             Q(op_id__icontains=key) |
             Q(event_desc__icontains=key)) &
            Q(is_active=True)
        ).order_by('id')
    else:
        # 如果没有提供关键词，则返回所有用户
        events = Event.objects.filter(is_active=True).order_by('id')

    page_obj = Pagination(request, events, items_per_page)
    context = {
        'column_names': column_names,
        "page_obj": page_obj,
        "key": key,
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/select_event.html", context=context)


def library(request):
    context={

    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/library.html",context)


def logging_record(request):
    key = request.GET.get('key', '')
    filter = request.GET.get('filter', '')
    column_names = [event[1] for event in OPERATION_CHOICES]
    if filter:
        logs = Logging.objects.filter(operation_type=filter, is_active=True)
        page_obj = Pagination(request, logs, items_per_page)
        context = {
            'column_names': column_names,
            "page_obj": page_obj,
            "filter": filter,
        }
        return render(request, "manager/logging_record.html", context=context)

    if key:
        # 搜索 address, name, 或 email 字段包含关键词的用户
        logs = Logging.objects.filter(
            (Q(id__icontains=key) |
             Q(operation_content__icontains=key) |
             Q(operation_time__icontains=key)) &
            Q(is_active=True)
        ).order_by('id')
    else:
        # 如果没有提供关键词，则返回所有用户
        logs = Logging.objects.filter(is_active=True).order_by('id')

    page_obj = Pagination(request, logs, items_per_page)
    context = {
        'column_names': column_names,
        "page_obj": page_obj,
        "key": key,
    }
    return render(request, "manager/logging_record.html", context=context)
