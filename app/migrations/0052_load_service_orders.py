from django.db import migrations

def load_service_orders(apps, schema_editor):
    Elder = apps.get_model('app', 'Elder')
    Service = apps.get_model('app', 'Service')
    ServiceOrder = apps.get_model('app', 'ServiceOrder')
    from django.utils import timezone

    # 确保有老人和服务可以用于创建订单
    elder = Elder.objects.get(id=28)
    service = Service.objects.get(id=1)

    # 创建服务订单实例
    ServiceOrder.objects.create(
        elder=elder,
        service=service,
        date_scheduled=timezone.now() + timezone.timedelta(days=10),
        status='pending'
    )
    ServiceOrder.objects.create(
        elder=elder,
        service=service,
        date_scheduled=timezone.now() + timezone.timedelta(days=24),
        status='pending'
    )

class Migration(migrations.Migration):
    dependencies = [
        # 依赖于先前的迁移文件，例如 '0003_last_migration'
        ('app', '0051_add_initial_services'),
    ]

    operations = [
        migrations.RunPython(load_service_orders),
    ]
