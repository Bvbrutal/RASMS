from dateutil.relativedelta import relativedelta
from django.utils.timezone import now

from app.models import Elder, Staff, Volunteer


def community_information():
    # 目前养老社区人数
    elders_count = Elder.objects.filter(is_active=True).count()
    worker_count = Staff.objects.filter(is_active=True).count()
    volunteer_count = Volunteer.objects.filter(is_active=True).count()
    item_count = [elders_count, worker_count, volunteer_count]

    # 近六个月的养老人数变化
    # 获取当前时间
    current_time = now()
    current_time_first = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # 计算六个月前的日期
    six_months_ago = current_time_first - relativedelta(months=6)
    monthly_checkin = {}
    monthly_checkout = {}

    item_change = []

    # 遍历最近六个月
    for month in range(6):
        # 计算每个月的开始和结束时间
        start_date = six_months_ago + relativedelta(months=month)
        end_date = start_date + relativedelta(months=1)

        # 查询在该月份入院的老人数量
        checkout_count = Elder.objects.filter(
            checkout_date__gte=start_date,
            checkout_date__lt=end_date,
            checkout_date__isnull=False  # 排除空白值
        ).count()
        checkin_count = Elder.objects.filter(
            checkin_date__gte=start_date,
            checkin_date__lt=end_date,
            checkin_date__isnull=False  # 排除空白值
        ).count()

        hire_date_count1 = Staff.objects.filter(
            hire_date__gte=start_date,
            hire_date__lt=end_date,
            hire_date__isnull=False  # 排除空白值
        ).count()

        resign_date_count = Staff.objects.filter(
            resign_date__gte=start_date,
            resign_date__lt=end_date,
            hire_date__isnull=False  # 排除空白值
        ).count()

        hire_date_count2 = Volunteer.objects.filter(
            hire_date__gte=start_date,
            hire_date__lt=end_date,
            hire_date__isnull=False  # 排除空白值
        ).count()

        item_change.append(
            [start_date.strftime("%m/%Y"), checkin_count, checkout_count, hire_date_count1, resign_date_count,
             hire_date_count2])
        # 将结果存储在字典中
        monthly_checkin[start_date.strftime("%Y-%m")] = checkin_count
        monthly_checkout[start_date.strftime("%Y-%m")] = checkout_count
    data_in_key = [key for key, value in monthly_checkin.items()]
    data_in_value = [value for key, value in monthly_checkin.items()]
    data_out_key = [key for key, value in monthly_checkout.items()]
    data_out_value = [value for key, value in monthly_checkout.items()]

    context = {
        'item_count': item_count,
        'data_in_key': data_in_key,
        'data_in_value': data_in_value,
        'data_out_key': data_out_key,
        'data_out_value': data_out_value,
        'item_change': reversed(item_change),
    }

    return context