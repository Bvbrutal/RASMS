import os
import django
import os
import django
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RASMS.settings')
django.setup()

from app.models import CommunityAnnouncement, User, ShiftAssignment
from app.models import Service


def services_data():
    additional_services = [
        Service(
            name="基础日常护理",
            description="提供基本的生活照料，包括用餐、洗澡、穿衣等服务。",
            type="daily_care",
            target_group="所有老年人",
            service_hours="每天全天",
            service_area="全国各大城市",
            qualifications="护理人员都经过专业培训和认证",
            customer_reviews="服务非常细致入微，家人非常满意。",
            additional_costs="无",
            cost=Decimal('500.00'),
            service_photo='service_photo/基础日常护理.jpeg',
            is_active=True
        ),
        Service(
            name="全面健康检查",
            description="每月进行一次全面的健康检查，包括血压、血糖、心电图等检查。",
            type="medical_care",
            target_group="所有老年人",
            service_hours="每月一次",
            service_area="全国各大城市",
            qualifications="由认证医生和护士团队执行",
            customer_reviews="非常专业，详细的健康报告帮助我们了解健康状况。",
            additional_costs="无",
            cost=Decimal('300.00'),
            is_active=True
        ),
        Service(
            name="康复理疗服务",
            description="为有需要的老人提供康复理疗服务，包括物理治疗和职业治疗。",
            type="rehabilitation",
            target_group="需要康复的老年人",
            service_hours="每周三次，每次两小时",
            service_area="全国各大城市",
            qualifications="理疗师均持有国家认证",
            customer_reviews="服务很到位，帮助家人恢复了很多。",
            additional_costs="无",
            cost=Decimal('800.00'),
            is_active=True
        ),
        Service(
            name="心理咨询服务",
            description="提供专业的心理咨询和支持，帮助老人处理情绪问题和心理健康。",
            type="mental_health",
            target_group="需要心理支持的老年人",
            service_hours="每周一次，每次一小时",
            service_area="全国各大城市",
            qualifications="所有心理咨询师均具有心理学背景和专业资格",
            customer_reviews="非常理解老年人的需求，非常有帮助。",
            additional_costs="无",
            cost=Decimal('400.00'),
            is_active=True
        ),
        Service(
            name="文化娱乐活动",
            description="组织各种文化和娱乐活动，如音乐会、电影放映和游戏，以丰富老人的社交生活。",
            type="leisure",
            target_group="所有老年人",
            service_hours="每月两次",
            service_area="全国各大城市",
            qualifications="活动组织者有丰富的活动策划经验",
            customer_reviews="活动多样，很有趣，非常期待每次的活动。",
            additional_costs="无",
            cost=Decimal('200.00'),
            is_active=True
        ),
        Service(
            name="个性化健身计划",
            description="根据每位老人的健康状况制定个性化的健身计划，包括轻度运动和适度的体育活动。",
            type="leisure",
            target_group="需要体育锻炼的老年人",
            service_hours="根据个人计划定制",
            service_area="覆盖所有服务区域",
            qualifications="所有教练均持有专业健身教练资格",
            customer_reviews="参与者反馈非常好，感觉更健康",
            additional_costs="无",
            cost=Decimal('350.00'),
            is_active=True
        ),
        Service(
            name="家庭式餐饮服务",
            description="提供定制化的餐饮服务，包括营养配餐和特殊饮食需求的满足。",
            type="daily_care",
            target_group="有特殊饮食需求的老年人",
            service_hours="全天",
            service_area="覆盖所有服务区域",
            qualifications="营养师及厨师团队",
            customer_reviews="餐食美味，满足特殊饮食需求",
            additional_costs="无",
            cost=Decimal('450.00'),
            is_active=True
        ),
        Service(
            name="专业护理服务",
            description="为有特殊医疗需求的老人提供专业护理和监护，包括病情管理和药物管理。",
            type="medical_care",
            target_group="有特殊医疗需求的老年人",
            service_hours="24小时",
            service_area="覆盖所有服务区域",
            qualifications="所有护理人员均具有医疗资格",
            customer_reviews="专业护理服务非常到位",
            additional_costs="无",
            cost=Decimal('1000.00'),
            is_active=True
        ),
        Service(
            name="出行辅助服务",
            description="提供定制的出行辅助，包括陪同外出、交通工具安排和外出活动策划。",
            type="leisure",
            target_group="需要辅助出行的老年人",
            service_hours="根据需求定制",
            service_area="覆盖所有服务区域",
            qualifications="所有员工均经过出行辅助培训",
            customer_reviews="非常贴心，出行无忧",
            additional_costs="根据具体活动可能有额外费用",
            cost=Decimal('300.00'),
            is_active=True
        ),
        Service(
            name="教育与技能培训",
            description="提供电脑使用、外语学习和其他技能培训课程，帮助老人学习新技能。",
            type="education",
            target_group="有学习新技能兴趣的老年人",
            service_hours="每周两次课，每次2小时",
            service_area="覆盖所有服务区域",
            qualifications="所有教师均具有相关教育背景",
            customer_reviews="课程有趣，学到了很多",
            additional_costs="无",
            cost=Decimal('150.00'),
            is_active=True
        )
    ]

    for service in additional_services:
        service.save()

    print("Services created successfully.")


def announcements_data():
    announcements_data = [
        {
            "title": "社区清洁日",
            "introduction": "参与我们的社区清洁，让我们的环境更美好。",
            "content": "本周六社区组织清洁活动，欢迎大家积极参与。",
            "published_date": timezone.now() - timedelta(days=1),
            "expiry_date": timezone.now() + timedelta(days=30),
            "author": "张三",
            "publisher": "社区管理委员会",
            "status": "active",
            "is_active": True
        },
        {
            "title": "老年人健康讲座",
            "introduction": "关注老年健康，关爱您的生活。",
            "content": "本月底将有一场针对老年人健康的讲座，内容涵盖饮食和运动。",
            "published_date": timezone.now() - timedelta(days=2),
            "expiry_date": timezone.now() + timedelta(days=20),
            "author": "李四",
            "publisher": "社区健康中心",
            "status": "active",
            "is_active": True
        },
        {
            "title": "健康饮食讲座",
            "introduction": "学习如何维持健康饮食，提升生活质量。",
            "content": "本周日，我们将邀请营养专家为社区居民举办健康饮食讲座，内容包括如何选择食材和制定饮食计划。",
            "published_date": timezone.now() - timedelta(days=3),
            "expiry_date": timezone.now() + timedelta(days=27),
            "author": "李四",
            "publisher": "社区健康促进会",
            "status": "active",
            "is_active": True
        },
        {
            "title": "春季花卉种植活动",
            "introduction": "一起动手种植花卉，美化我们的社区环境。",
            "content": "本月底社区将组织花卉种植活动，居民们将有机会学习种植技巧并实际操作，活动将在社区公园举行。",
            "published_date": timezone.now() - timedelta(days=7),
            "expiry_date": timezone.now() + timedelta(days=23),
            "author": "王五",
            "publisher": "社区环境保护协会",
            "status": "active",
            "is_active": True
        },
        {
            "title": "社区安全防范讲座",
            "introduction": "提升安全意识，共建安全社区。",
            "content": "面对日增的安全挑战，我们将于本周五晚上在社区中心举行安全防范讲座，警方代表将分享防范技巧。",
            "published_date": timezone.now() - timedelta(days=2),
            "expiry_date": timezone.now() + timedelta(days=28),
            "author": "赵六",
            "publisher": "社区公安局",
            "status": "active",
            "is_active": True
        },
        {
            "title": "老年人电脑基础课程",
            "introduction": "帮助老年人掌握电脑基础，享受数字生活。",
            "content": "为帮助社区中的老年人了解和掌握电脑使用，我们将在下周一至周三开设电脑基础课程。",
            "published_date": timezone.now() - timedelta(days=4),
            "expiry_date": timezone.now() + timedelta(days=26),
            "author": "孙七",
            "publisher": "社区教育中心",
            "status": "active",
            "is_active": True
        }

    ]

    # 获取或创建用户，假设为公告的创建者和更新者
    user_for = User.objects.filter(user_id=1668238).first()

    # 生成公告
    for data in announcements_data:
        announcement = CommunityAnnouncement(
            title=data["title"],
            introduction=data["introduction"],
            content=data["content"],
            published_date=data["published_date"],
            expiry_date=data["expiry_date"],
            author=data["author"],
            publisher=data["publisher"],
            is_active=data["is_active"],
            created_by=user_for,
            updated_by=user_for,
            status=data["status"]
        )
        announcement.save()

    print("Community announcements created successfully.")


def shift_assignments_data():
    shift_assignments = [
        ShiftAssignment(
            staff_name="王明",
            staff_phone="13598765432",
            volunteer_name="张丽",
            volunteer_phone="13612348765",
            area="接待区",
            weekday=1,
            shift=1
        ),
        ShiftAssignment(
            staff_name="李强",
            staff_phone="13765432198",
            volunteer_name="王芳",
            volunteer_phone="13876543210",
            area="医务室",
            weekday=3,
            shift=2
        ),
        ShiftAssignment(
            staff_name="刘涛",
            staff_phone="13345678901",
            volunteer_name="陈红",
            volunteer_phone="13567890123",
            area="餐厅",
            weekday=5,
            shift=3
        ),
        ShiftAssignment(
            staff_name="赵敏",
            staff_phone="13098765432",
            volunteer_name="周宇",
            volunteer_phone="13512348765",
            area="康复室",
            weekday=2,
            shift=2
        ),
        ShiftAssignment(
            staff_name="吴艳",
            staff_phone="13765432987",
            volunteer_name="王勇",
            volunteer_phone="13876543211",
            area="娱乐室",
            weekday=4,
            shift=1
        ),
        ShiftAssignment(
            staff_name="陈刚",
            staff_phone="13234567890",
            volunteer_name="李莉",
            volunteer_phone="13456789012",
            area="办公室",
            weekday=6,
            shift=3
        ),
        ShiftAssignment(
            staff_name="王磊",
            staff_phone="13456789012",
            volunteer_name="刘娜",
            volunteer_phone="13678901234",
            area="接待区",
            weekday=1,
            shift=2
        ),
        ShiftAssignment(
            staff_name="张明",
            staff_phone="13678901234",
            volunteer_name="王鹏",
            volunteer_phone="13890123456",
            area="康复室",
            weekday=3,
            shift=1
        ),
        ShiftAssignment(
            staff_name="李莉",
            staff_phone="13890123456",
            volunteer_name="陈刚",
            volunteer_phone="13234567890",
            area="餐厅",
            weekday=5,
            shift=2
        ),
        ShiftAssignment(
            staff_name="周宇",
            staff_phone="13512348765",
            volunteer_name="赵敏",
            volunteer_phone="13098765432",
            area="医务室",
            weekday=2,
            shift=3
        ),
        ShiftAssignment(
            staff_name="王芳",
            staff_phone="13876543210",
            volunteer_name="李强",
            volunteer_phone="13765432198",
            area="办公室",
            weekday=6,
            shift=1
        ),
        ShiftAssignment(
            staff_name="刘娜",
            staff_phone="13678901234",
            volunteer_name="王磊",
            volunteer_phone="13456789012",
            area="娱乐室",
            weekday=4,
            shift=2
        ),
        ShiftAssignment(
            staff_name="王勇",
            staff_phone="13876543211",
            volunteer_name="吴艳",
            volunteer_phone="13765432987",
            area="接待区",
            weekday=1,
            shift=3
        ),
        ShiftAssignment(
            staff_name="陈红",
            staff_phone="13567890123",
            volunteer_name="刘涛",
            volunteer_phone="13345678901",
            area="餐厅",
            weekday=5,
            shift=1
        ),
        ShiftAssignment(
            staff_name="张丽",
            staff_phone="13612348765",
            volunteer_name="王明",
            volunteer_phone="13598765432",
            area="医务室",
            weekday=2,
            shift=1
        ),
        ShiftAssignment(
            staff_name="王鹏",
            staff_phone="13890123456",
            volunteer_name="张明",
            volunteer_phone="13678901234",
            area="娱乐室",
            weekday=4,
            shift=3
        ),
        ShiftAssignment(
            staff_name="李莉",
            staff_phone="13456789012",
            volunteer_name="陈刚",
            volunteer_phone="13234567890",
            area="康复室",
            weekday=3,
            shift=2
        ),
        ShiftAssignment(
            staff_name="吴艳",
            staff_phone="13765432987",
            volunteer_name="王勇",
            volunteer_phone="13876543211",
            area="接待区",
            weekday=6,
            shift=1
        ),
        ShiftAssignment(
            staff_name="王明",
            staff_phone="13598765432",
            volunteer_name="张丽",
            volunteer_phone="13612348765",
            area="餐厅",
            weekday=5,
            shift=3
        ),
    ]

    for shift in shift_assignments:
        shift.save()

    print("shift_assignments created successfully.")


if __name__ == '__main__':
    shift_assignments_data()
