import json
import os

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import now

from RASMS import settings
from app.management_views.configuration import GENDER_CHOICES
from app.models import User
from app.user_views import USER_TYPES


def accont_api(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    serch_result = User.objects.filter(mobile_phone=mobile_phone).first()
    user_id = serch_result.user_id
    username = serch_result.username
    bio = serch_result.bio
    grade = USER_TYPES[str(serch_result.grade)]
    context = {
        'username': username,
        'user_id': user_id,
        'phone': mobile_phone,
        'bio': bio,
        'grade': grade,
        'user_photo': serch_result.user_photo.url if serch_result.user_photo else None,
    }
    return JsonResponse(context)


def update_profile(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    search_result = User.objects.filter(mobile_phone=mobile_phone)
    datas = json.loads(request.body)
    if "bio" in datas:
        search_result.update(bio=datas['bio'])
        context = {'message': '修改成功'}
        return JsonResponse(context, status=200)  # 成功响应
    else:
        item = User.objects.filter(mobile_phone=datas['mobile_phone'])
        if item.exists() and (datas['mobile_phone'] != mobile_phone):
            context = {'re':2,'message': '该手机号已经注册'}
            return JsonResponse(context, status=200)  # 成功响应
        gender = [key for key, value in GENDER_CHOICES if value == datas['gender']]
        print(gender)
        search_result.update(username=datas['username'], phone=datas['phone'], email=datas['email'],
                             gender=gender[0], mobile_phone=datas['mobile_phone'])
        print(request.session["info"])
        request.session["info"]["mobile_phone"] = datas['mobile_phone']
        request.session.modified = True
        print(request.session["info"])
        context = {
            're':1,
            'message': '修改成功'}
        return JsonResponse(context, status=200)  # 成功响应


def logging(request):
    global fomat_time
    mobile_phone = request.session["info"]["mobile_phone"]
    operator = User.objects.get(mobile_phone=mobile_phone)
    loggings = operator.Logging.all().order_by("-operation_time")
    # json_data = serializers.serialize('json', loggings)
    # loggings_data = json.loads(json_data)
    # print(type(loggings_data[0]))
    # loggings_data[0][]
    # 准备一个列表来存储更新后的日志记录
    updated_loggings = []
    current_time = timezone.now()

    for log in loggings:
        # 计算距离现在有多久
        time_diff = current_time - log.operation_time
        total_seconds = time_diff.total_seconds()
        day, remainder = divmod(total_seconds, 24 * 3600)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        if day > 0:
            fomat_time = "{}天前".format(int(day))
        elif hours > 0:
            fomat_time = "{}小时前".format(int(hours))
        elif minutes > 0:
            fomat_time = "{}分钟前".format(int(minutes))
        elif seconds > 0:  # 如果没有更大的单位，且确实有秒差异，则显示秒
            fomat_time = "{}秒前".format(int(seconds))
        # 将更新后的记录添加到列表中
        updated_loggings.append({
            "operation_time": fomat_time,
            "operator": log.operator_id,  # 假设是外键关联到操作员的 ID
            "operation_content": log.operation_content
        })
        if len(updated_loggings) > 6:
            break
    context = {'message': '处理成功', 'loggings': updated_loggings}
    return JsonResponse(context, safe=False, status=200)


# 图片上传
def image_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        image_file = request.FILES['file']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tinymce_image'))
        _, ext = os.path.splitext(image_file.name)
        image_file.name = f"{now().strftime('%Y%m%d%H%M%S')}{ext}"
        filename = fs.save(image_file.name, image_file)
        image_url = os.path.join('\media', 'tinymce_image', filename)
        print(image_url)
        return JsonResponse({'location': image_url})
    return JsonResponse({'error': 'Failed to upload image'})
