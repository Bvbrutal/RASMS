# 导入 Service 模型
from app.models import Service

# 创建服务实例并保存到数据库
services_data = [
    {"name": "基础日常护理", "description": "提供基本的生活照料，包括用餐、洗澡、穿衣等服务。", "cost": 500.00},
    {"name": "全面健康检查", "description": "每月进行一次全面的健康检查，包括血压、血糖、心电图等检查。", "cost": 300.00},
    {"name": "康复理疗服务", "description": "为有需要的老人提供康复理疗服务，包括物理治疗和职业治疗。", "cost": 800.00},
    {"name": "心理咨询服务", "description": "提供专业的心理咨询和支持，帮助老人处理情绪问题和心理健康。", "cost": 400.00},
    {"name": "文化娱乐活动", "description": "组织各种文化和娱乐活动，如音乐会、电影放映和游戏，以丰富老人的社交生活。", "cost": 200.00}
]

for service_data in services_data:
    service = Service(**service_data)
    service.save()

# 检查是否添加成功
print(Service.objects.all())
