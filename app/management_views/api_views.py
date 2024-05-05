import json
import os

from django.db.models import Count
from django.http import JsonResponse
import json
import re
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import now

from RASMS import settings
from app.management_views.configuration import GENDER_CHOICES
from app.models import User, ServiceOrder, Service
from app.user_views import USER_TYPES

STATUS_CHOICES = (
    ('pending', '待处理'),
    ('accepted', '已接单'),
    ('in_progress', '进行中'),
    ('completed', '已完成'),
    ('cancelled', '已取消'),
)
SERVICE_TYPES = (
    ('daily_care', '日常护理'),
    ('medical_care', '医疗护理'),
    ('rehabilitation', '康复护理'),
    ('leisure', '休闲活动'),
    ('education', '教育活动'),
    ('mental_health', '精神健康')
)


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
    datas = json.loads(request.body)
    mobile_phone = datas.get('mobile_phone_old')
    new_phone = datas.get('phone')
    new_mobile_phone = datas.get('mobile_phone')
    email = datas.get('email')

    # 更新用户信息
    search_result = User.objects.filter(mobile_phone=mobile_phone)
    if "bio" in datas:
        search_result.update(bio=datas['bio'])
        return JsonResponse({'ret': 1, 'message': '修改成功'}, status=200)

    phone_pattern = re.compile(r'^0\d{2,3}-\d{7,8}$')
    mobile_phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    # 验证电话号码
    if new_phone and not phone_pattern.match(new_phone):
        return JsonResponse({'ret': 0, 'message': '无效的电话号码格式'}, status=200)

    # 验证移动电话号码
    if new_mobile_phone and not mobile_phone_pattern.match(new_mobile_phone):
        return JsonResponse({'ret': 0, 'message': '无效的手机号格式'}, status=200)

    # 验证电子邮箱
    if email and not email_pattern.match(email):
        return JsonResponse({'ret': 0, 'message': '无效的邮箱格式'}, status=200)

    # 检查手机号是否已被其他账户使用
    if User.objects.exclude(mobile_phone=mobile_phone).filter(mobile_phone=new_mobile_phone).exists():
        return JsonResponse({'ret': 2, 'message': '该手机号已经注册'}, status=200)

    # 更详尽的信息更新
    gender = next((key for key, value in GENDER_CHOICES if value == datas['gender']), None)
    if search_result.exists():
        search_result.update(
            username=datas['username'],
            phone=datas['phone'],
            email=email,
            gender=gender,
            mobile_phone=new_mobile_phone
        )
        if request.session.get("info", {}).get("mobile_phone") == mobile_phone:
            request.session["info"]["mobile_phone"] = new_mobile_phone
            request.session.modified = True

        return JsonResponse({'ret': 1, 'message': '修改成功'}, status=200)

    return JsonResponse({'ret': 0, 'message': '用户未找到'}, status=200)


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
            "operation_content": log.operation_content,
            "operation_type": log.get_operation_type_display()
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


def service_status(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        status = ServiceOrder.objects.filter(id=id).first().status
        return JsonResponse({'status': status}, safe=False, status=200)
    return JsonResponse({'error': '请求错误'}, safe=False, status=200)


def service_type_distribution(request):
    # Aggregate service types and count them
    data = Service.objects.values('type').annotate(total=Count('type')).order_by('type')
    service_types = dict(SERVICE_TYPES)
    response_data = {
        'categories': [service_types.get(item['type'], "未知服务") for item in data],
        'values': [item['total'] for item in data]
    }
    return JsonResponse(response_data)


def order_status_distribution(request):
    # Aggregate order statuses and count them
    data = ServiceOrder.objects.values('status').annotate(total=Count('status')).order_by('status')
    status_descriptions = dict(STATUS_CHOICES)
    response_data = {
        'categories': [status_descriptions.get(item['status'], "未知状态") for item in data],
        'values': [item['total'] for item in data]
    }
    return JsonResponse(response_data)


from django.db.models.functions import TruncDay

from django.utils import timezone
from datetime import timedelta
def daily_orders_stats(request):
    # 获取今天的日期并计算30天前的日期
    today = timezone.now().date()
    start_date = today - timedelta(days=90)

    # 过滤最近30天的订单，然后按天聚合
    data = ServiceOrder.objects.filter(
        date_scheduled__date__gte=start_date
    ).annotate(
        date=TruncDay('date_scheduled')  # 将 datetime 截断到天
    ).values('date').annotate(
        total=Count('id')  # 按天计算订单数量
    ).order_by('date')  # 按日期排序

    # 为前端准备数据
    dates = [item['date'].strftime('%Y-%m-%d') if item['date'] else '未知日期' for item in data]
    counts = [item['total'] for item in data]

    return JsonResponse({
        'dates': dates,  # 日期列表
        'counts': counts  # 每天对应的订单数量
    })
