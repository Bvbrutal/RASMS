from django.utils import timezone

from ..models import UserIP, VisitNumber, DayNumber, User
from .ip_convert_addr import ip_to_addr

"""
    # 访问信息服务
    # change_info(request, '/index',user_id
    # city = UserIP.objects.all().last()
"""
# 自定义的函数，不是视图
def change_info(request, end_point,user_id):
    """
    # 修改网站访问量和访问 ip 等信息
    # 每一次访问，网站总访问次数加一
    """

    # 记录访问 ip 和每个 ip 的次数
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取 ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的 ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理 ip
    # print(client_ip)

    ip_exist = UserIP.objects.filter(ip=str(client_ip), end_point=end_point,user_by__user_id=user_id)
    if ip_exist:  # 判断是否存在该 ip
        uobj = ip_exist[0]
        uobj.count += 1
    else:
        uobj = UserIP()
        uobj.ip = client_ip
        uobj.end_point = end_point
        user_by=User.objects.filter(user_id=user_id).first()
        uobj.user_by=user_by
        try:
            uobj.ip_addr = ip_to_addr(client_ip)
        except:
            uobj.ip_addr = 'unknown'
        uobj.count = 1
    uobj.save()

    # 增加今日访问次数
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date)
    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.count = 1
    temp.save()