import json

from django.http import JsonResponse

from app.configuration import  GENDER_CHOICES
from app.models import Test
from app.user_views import USER_TYPES


def accont_api(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    serch_result = Test.objects.filter(mobile_phone=mobile_phone).first()
    user_id = serch_result.user_id
    username = serch_result.username
    bio = serch_result.bio
    grade = USER_TYPES[str(serch_result.grade)]
    context = {
        'username': username,
        'user_id': user_id,
        'phone': mobile_phone,
        'bio': bio,
        'grade': grade
    }
    return JsonResponse(context)


def update_profile(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    search_result = Test.objects.filter(mobile_phone=mobile_phone)
    datas = json.loads(request.body)
    if "bio" in datas:
        search_result.update(bio=datas['bio'])
        context = {'message': '处理成功'}
        return JsonResponse(context, status=200)  # 成功响应
    else:
        gender=[key for key, value in GENDER_CHOICES if value == datas['gender']]
        search_result.update(username=datas['username'], phone=datas['phone'], email=datas['email'],
                             gender=gender[0], mobile_phone=datas['mobile_phone'])
        context = {'message': '处理成功'}
        return JsonResponse(context, status=200)  # 成功响应


from django.core import serializers
from django.utils import timezone
from django.utils.timesince import timesince

def logging(request):
    mobile_phone = request.session["info"]["mobile_phone"]
    operator = Test.objects.get(mobile_phone=mobile_phone)
    loggings=operator.Logging.all().order_by("-operation_time")
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
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        fomat_time="{}小时{}分钟前".format(int(hours), int(minutes))

        # 将更新后的记录添加到列表中
        updated_loggings.append({
            "operation_time": fomat_time,
            "operator": log.operator_id,  # 假设是外键关联到操作员的 ID
            "operation_content": log.operation_content
        })
        if len(updated_loggings) > 6:
            break
    context = {'message': '处理成功', 'loggings': updated_loggings}
    return JsonResponse(context,safe=False, status=200)