from django.db import migrations

def add_service_order_data(apps, schema_editor):
    Elder = apps.get_model('app', 'Elder')
    Service = apps.get_model('app', 'Service')
    ServiceOrder = apps.get_model('app', 'ServiceOrder')
    from django.utils import timezone

    # 获取示例老人和服务实例
    elder = Elder.objects.first()  # 假设我们取数据库中的第一个老人
    service = Service.objects.filter(id=2).first()  # 假设我们取数据库中的第一个服务

    # 创建带有评分和反馈的服务订单实例
    orders_data = [
        {"elder": elder, "service": service, "date_scheduled": timezone.now() + timezone.timedelta(days=10), "status": 'completed', "rating": 5, "feedback": "非常满意，服务周到。"},
        {"elder": elder, "service": service, "date_scheduled": timezone.now() + timezone.timedelta(days=20), "status": 'completed', "rating": 4, "feedback": "服务很好，但希望下次能更及时。"},
        {"elder": elder, "service": service, "date_scheduled": timezone.now() + timezone.timedelta(days=30), "status": 'cancelled', "rating": None, "feedback": "取消服务，原因是时间冲突。"}
    ]

    for order_data in orders_data:
        ServiceOrder.objects.create(**order_data)

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0052_load_service_orders'),
    ]

    operations = [
        migrations.RunPython(add_service_order_data),
    ]
