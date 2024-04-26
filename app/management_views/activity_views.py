import os
import re

from django.shortcuts import render
from django.utils.timezone import now

from app.components.Dynamic_inheritance import Dynamic_inheritance
from app.models import CommunityEvent, User

from django.http import JsonResponse
def activity_list(request):
    communityEvent=CommunityEvent.objects.all().order_by("-created")
    print(communityEvent)
    context={
        'communityEvent':communityEvent
    }

    return render(request,"manager/activity/activity_list.html",context)


def activity_info(request):
    activity_id=request.GET.get('activity_id')
    activity=CommunityEvent.objects.filter(id=activity_id).first()
    context = {
        'event': activity
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request,"manager/activity/activity_info.html",context)


def activity_add(request):
    if request.method == "GET":
        context = {

        }
        return render(request, "manager/activity/activity_add.html", context)
    # 从请求数据中获取字段值
    title = request.POST.get('title')
    introduction = request.POST.get('introduction') or None
    content = request.POST.get('content')
    editorContent = request.POST.get('editorContent')
    publisher = request.POST.get('publisher') or None
    published_date = request.POST.get('published_date') or None
    expiry_date = request.POST.get('expiry_date') or None
    status = request.POST.get('status') or None
    author_id = request.session["info"]["user_id"]
    author = User.objects.filter(user_id=author_id).first()
    content_text = re.sub('<[^<]+?>', '', content.strip())
    is_save = request.POST.get('is_active') or True
    # 获取上传的文件
    uploaded_file = request.FILES.get('pic1') or None
    created_by_id = request.session["info"]["user_id"]
    updated_by_id = created_by_id
    print(updated_by_id, editorContent)
    if uploaded_file:
        _, ext = os.path.splitext(uploaded_file.name)

        # 使用用户的电话号码作为文件名，保留原始文件的扩展名
        uploaded_file.name = f"{now().strftime('%Y%m%d%H%M%S')}{ext}"
    if introduction is None:
        introduction = content_text[:20]
    if is_save == 'False':
        is_save = False
    CE = CommunityEvent(
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
    CE.save()
    context = {
        'ret': 1,
        'msg': "活动编辑成功"
    }
    return JsonResponse(context, safe=False, status=200)


def activity_modify(request):
    return None