from datetime import datetime

from django.contrib.auth.models import Permission
from django.db import models
from django.utils import timezone

from app.management_views.configuration import GENDER_CHOICES, GRADE_CHOICES, EVENT_TYPES, OPERATION_CHOICES


# 测试
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, verbose_name='用户名', default='匿名用户')
    password = models.CharField(max_length=50, verbose_name="密码")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U', verbose_name='性别')
    mobile_phone = models.CharField(max_length=50, verbose_name="移动电话", unique=True)
    creation_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='电话')
    email = models.EmailField(verbose_name='邮箱', null=True, blank=True)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, default='3', verbose_name='类别')
    bio = models.TextField(verbose_name='自我介绍', blank=True, null=True)
    user_photo = models.ImageField(upload_to='user_photo/', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="是否有效")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username


# 老人
class Elder(models.Model):
    username = models.CharField(max_length=50, verbose_name='老人姓名')
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default='U', verbose_name='性别')
    mobile_phone = models.CharField(max_length=50, verbose_name="移动电话", unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='座机电话')
    id_card = models.CharField(max_length=50, unique=True, verbose_name='身份证号')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')  # 允许为空，有可能未知
    checkin_date = models.DateField(null=True, blank=True, verbose_name='入养老院日期')  # 允许为空，初始状态可能未入住
    checkout_date = models.DateField(null=True, blank=True, verbose_name='离开养老院日期')  # 允许为空，初始状态肯定为空
    elder_photo = models.ImageField(upload_to='elder_photo/', null=True, blank=True)
    room_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='房间号')  # 允许为空，可能未分配房间
    firstguardian_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='第一监护人姓名')
    firstguardian_relationship = models.CharField(max_length=50, blank=True, null=True, verbose_name='与第一监护人关系')
    firstguardian_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='第一监护人电话')
    firstguardian_wechat = models.CharField(max_length=50, blank=True, null=True, verbose_name='第一监护人微信')
    secondguardian_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='第二监护人姓名')
    secondguardian_relationship = models.CharField(max_length=50, blank=True, null=True,
                                                   verbose_name='与第二监护人关系')
    secondguardian_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='第二监护人电话')
    secondguardian_wechat = models.CharField(max_length=50, blank=True, null=True, verbose_name='第二监护人微信')
    health_state = models.CharField(max_length=50, blank=True, null=True, default='良好',
                                    verbose_name='健康状况')  # 设置默认健康状况为“良好”
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name='描述')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, related_name='%(class)s_requests_created',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='创建人')
    updated_by = models.ForeignKey(User, related_name='%(class)s_requests_updated',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='更新人')
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    bind_user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='elder_data',
                                     verbose_name='绑定用户')

    def calculate_age(self):
        today = datetime.today()
        age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return age

    class Meta:
        verbose_name = '老人信息'
        verbose_name_plural = '老人信息'
        db_table = 'elder_info'

    def __str__(self):
        return self.username


# 工作人员
class Staff(models.Model):
    username = models.CharField(max_length=50, verbose_name='工作人员姓名')
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default='U', verbose_name='性别')
    mobile_phone = models.CharField(max_length=50, verbose_name="移动电话", unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='座机电话')
    id_card = models.CharField(max_length=50, unique=True, verbose_name='身份证号')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    hire_date = models.DateField(null=True, blank=True, verbose_name='入职日期')
    resign_date = models.DateField(null=True, blank=True, verbose_name='离职日期')
    staff_photo = models.ImageField(upload_to='staff_photo/', null=True, blank=True)
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name='描述')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, related_name='%(class)s_requests_created',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='创建人')
    updated_by = models.ForeignKey(User, related_name='%(class)s_requests_updated',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='更新人')
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    bind_user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='staff_data',
                                     verbose_name='绑定用户')

    def calculate_age(self):
        today = datetime.today()
        age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return age

    class Meta:
        verbose_name = '工作人员'
        verbose_name_plural = '工作人员'
        db_table = 'staff_info'

    def __str__(self):
        return self.username


# 义工
class Volunteer(models.Model):
    username = models.CharField(max_length=50, verbose_name='义工姓名')
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default='U', verbose_name='性别')
    mobile_phone = models.CharField(max_length=50, verbose_name="移动电话", unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='座机电话')
    id_card = models.CharField(max_length=50, unique=True, verbose_name='身份证号')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    hire_date = models.DateField(null=True, blank=True, verbose_name='入职日期')
    resign_date = models.DateField(null=True, blank=True, verbose_name='离职日期')
    volunteer_photo = models.ImageField(upload_to='volunteer_photo/', null=True, blank=True)
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name='描述')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, related_name='%(class)s_requests_created',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='创建人')
    updated_by = models.ForeignKey(User, related_name='%(class)s_requests_updated',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='更新人')
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    bind_user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='volunteer_data',
                                     verbose_name='绑定用户')

    def calculate_age(self):
        today = datetime.today()
        age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return age

    class Meta:
        verbose_name = "义工"
        verbose_name_plural = "义工"
        db_table = 'volunteer_info'

    def __str__(self):
        return self.username


# 事件
class Event(models.Model):
    EVENT_TYPES = (
        (0, '情感纠纷'),
        (1, '意外事件'),
        (2, '特殊事件'),
        (3, '服务求助'),
        (4, '日常协助'),
    )
    event_type = models.IntegerField(default=0, choices=EVENT_TYPES, verbose_name='事件类型')
    event_date = models.DateTimeField(verbose_name='事件发生时间')
    event_location = models.CharField(max_length=200, blank=True, default='', verbose_name='事件发生地点')
    event_desc = models.TextField(max_length=200, blank=True, default='', verbose_name='事件描述')
    oldperson_id = models.IntegerField(blank=True, null=True, verbose_name='老人id')
    op_id = models.IntegerField(blank=True, null=True, verbose_name='记录者id')
    is_active = models.BooleanField(default=True, verbose_name="是否有效")

    class Meta:
        verbose_name = '事件记录'
        verbose_name_plural = '事件记录'
        db_table = 'event_record'

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.event_date.strftime('%Y-%m-%d %H:%M:%S')}"


# 日志记录
class Logging(models.Model):
    operation_time = models.DateTimeField(default=timezone.now)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Logging', verbose_name='日志')
    operation_content = models.TextField(blank=True, null=True, verbose_name='操作信息')
    operation_type = models.CharField(max_length=20, choices=OPERATION_CHOICES, blank=True, null=True,
                                      verbose_name='操作类型')
    is_active = models.BooleanField(default=True, verbose_name="是否有效")

    def __str__(self):
        return f"{self.operation_time} - {self.operator} - {self.get_operation_type_display()}"


# 社区活动管理
class CommunityEvent(models.Model):
    STATUS_CHOICES = (
        ('not_started', '未开始'),
        ('ongoing', '进行中'),
        ('finished', '已结束'),
    )
    name = models.CharField(max_length=255, verbose_name="活动名称")
    introduction = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介")
    description = models.TextField(verbose_name="描述", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="开始时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="结束时间", null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name="地点", null=True, blank=True)
    organizer = models.CharField(max_length=255, verbose_name="主办方", null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True, verbose_name="发布者")
    participant_limit = models.IntegerField(verbose_name="参与人数限制", null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not_started', verbose_name="活动状态")
    contact_info = models.CharField(max_length=255, verbose_name="联系信息", null=True, blank=True)
    cost = models.CharField(max_length=255, verbose_name="费用", null=True, blank=True)
    image = models.ImageField(upload_to='communityevents/', verbose_name="图片/海报", null=True, blank=True)
    category = models.CharField(max_length=255, verbose_name="分类", null=True, blank=True)
    registration_link = models.URLField(verbose_name="注册/报名链接", max_length=1024, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='创键时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_save = models.BooleanField(default=True, verbose_name="是否保存为草稿")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    created_by = models.ForeignKey(User, related_name='%(class)s_requests_created',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='创建人')
    updated_by = models.ForeignKey(User, related_name='%(class)s_requests_updated',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='更新人')

    def registration_count(self):
        return self.registrations.count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "社区活动"
        verbose_name_plural = "社区活动"



# 社区公告管理
class CommunityAnnouncement(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    introduction = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介")
    content = models.TextField(verbose_name="内容")
    published_date = models.DateTimeField(null=True, blank=True, verbose_name="发布日期")
    expiry_date = models.DateTimeField(null=True, blank=True, verbose_name="过期日期")
    author = models.CharField(max_length=255, null=True, blank=True, verbose_name="发布者")
    publisher = models.CharField(max_length=255, null=True, blank=True, verbose_name="发布方")
    announcement_photo = models.ImageField(upload_to='announcement_photo/', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    is_save = models.BooleanField(default=True, verbose_name="是否保存为草稿")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创键时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, related_name='%(class)s_requests_created',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='创建人')
    updated_by = models.ForeignKey(User, related_name='%(class)s_requests_updated',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='更新人')
    STATUS_CHOICES = (
        ('active', '有效'),
        ('inactive', '暂时无效'),
        ('expired', '过期'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="状态")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 如果没有设置发布日期，则默认使用创建时间
        if not self.published_date:
            self.published_date = self.created or timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "社区公告"
        verbose_name_plural = "社区公告"


# 访问信息

# 访问网站的 ip 地址、端点和次数
class UserIP(models.Model):
    ip = models.CharField(verbose_name='IP 地址', max_length=30, blank=True, null=True)
    ip_addr = models.CharField(verbose_name='IP 地理位置', max_length=30, blank=True, null=True)
    end_point = models.CharField(verbose_name='访问端点', default='/', max_length=30, blank=True, null=True)
    count = models.IntegerField(verbose_name='访问次数', default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='登录时间', blank=True, null=True)
    user_by = models.ForeignKey(User, related_name='%(class)s_user_by', on_delete=models.SET_NULL, blank=True,
                                null=True, verbose_name='账户')

    class Meta:
        verbose_name = '访问用户信息'
        verbose_name_plural = verbose_name


# 网站总访问次数
class VisitNumber(models.Model):
    count = models.IntegerField(verbose_name='网站访问总次数', default=0)  # 网站访问总次数
    type = models.CharField(max_length=20, verbose_name="计数类型", null=True, blank=True)

    class Meta:
        verbose_name = '网站访问总次数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.count)


# 单日访问量统计
class DayNumber(models.Model):
    day = models.DateField(verbose_name='日期', default=timezone.now)
    count = models.IntegerField(verbose_name='网站访问次数', default=0)  # 网站访问总次数

    class Meta:
        verbose_name = '网站日访问量统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.day)


class Service(models.Model):
    SERVICE_TYPES = (
        ('daily_care', '日常护理'),
        ('medical_care', '医疗护理'),
        ('rehabilitation', '康复护理'),
        ('leisure', '休闲活动'),
        ('education', '教育活动'),
        ('mental_health', '精神健康')
    )

    name = models.CharField(max_length=100, verbose_name="服务名称", null=True, blank=True)
    content = models.TextField(verbose_name="服务内容", null=True, blank=True)
    description = models.TextField(verbose_name="服务描述", null=True, blank=True)
    type = models.CharField(max_length=20, choices=SERVICE_TYPES, verbose_name="服务类型", null=True, blank=True)
    target_group = models.CharField(max_length=100, verbose_name="服务对象", null=True, blank=True)
    service_hours = models.CharField(max_length=50, verbose_name="服务时间", null=True, blank=True)
    service_area = models.CharField(max_length=100, verbose_name="服务区域", null=True, blank=True)
    qualifications = models.TextField(verbose_name="服务人员资质", null=True, blank=True)
    customer_reviews = models.TextField(verbose_name="客户评价", null=True, blank=True)
    additional_costs = models.TextField(verbose_name="附加费用", null=True, blank=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="服务费用")
    service_photo = models.ImageField(upload_to='service_photo/', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, related_name='%(class)s_Service_created',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='创建人')
    updated_by = models.ForeignKey(User, related_name='%(class)s_Service_updated',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='更新人')
    count = models.IntegerField(verbose_name='下单次数', default=0, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "服务"
        verbose_name_plural = "服务"


class ServiceOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('accepted', '已接单'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )

    customerName = models.CharField(max_length=20, verbose_name="客户姓名", null=True, blank=True)
    customerContact = models.CharField(max_length=50, verbose_name="联系方式", null=True, blank=True)
    aceeptName = models.CharField(max_length=20, verbose_name="服务接受者", null=True, blank=True)
    aceeptContact = models.CharField(max_length=50, verbose_name="服务接受者联系方式", null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="服务", related_name="orders")
    date_scheduled = models.DateTimeField(verbose_name="预定日期", null=True, blank=True)
    date_accepted = models.DateTimeField(verbose_name="接受日期", null=True, blank=True)
    date_started = models.DateTimeField(verbose_name="开始日期", null=True, blank=True)
    date_completed = models.DateTimeField(verbose_name="完成日期", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="订单状态")
    rating = models.IntegerField(null=True, blank=True,
                                 choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
                                 verbose_name="评分")
    feedback = models.TextField(null=True, blank=True, verbose_name="反馈")
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, related_name='%(class)s_ServiceOrder_created',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='创建人')
    updated_by = models.ForeignKey(User, related_name='%(class)s_ServiceOrder_updated',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='更新人')

    def __str__(self):
        return f"{self.customerName} - {self.service.name} - {self.date_scheduled.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "服务订单"
        verbose_name_plural = "服务订单"


from django.utils.translation import gettext_lazy as _


class ShiftAssignment(models.Model):
    staff_name = models.CharField(max_length=25, verbose_name="工作人员", null=True, blank=True)
    staff_phone = models.CharField(max_length=20, verbose_name="工作人员联系方式", null=True, blank=True)
    volunteer_name = models.CharField(max_length=25, verbose_name="义工", null=True, blank=True)
    volunteer_phone = models.CharField(max_length=20, verbose_name="义工联系方式", null=True, blank=True)
    area = models.CharField(max_length=100, verbose_name="工作区域", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    created_by = models.ForeignKey(User, related_name='%(class)s_ShiftAssignment_created',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='创建人')
    updated_by = models.ForeignKey(User, related_name='%(class)s_ShiftAssignment_updated',
                                   on_delete=models.SET_NULL, blank=True, null=True, verbose_name='更新人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    WEEKDAYS = [
        (1, _('星期一')),
        (2, _('星期二')),
        (3, _('星期三')),
        (4, _('星期四')),
        (5, _('星期五')),
        (6, _('星期六')),
        (7, _('星期天')),
    ]
    weekday = models.IntegerField(choices=WEEKDAYS, verbose_name="星期", null=True, blank=True)

    SHIFTS = [
        (1, _('时间段 1: 08:00-10:20')),
        (2, _('时间段 2: 10:20-12:40')),
        (3, _('时间段 3: 12:40-15:00')),
        (4, _('时间段 4: 15:00-17:20')),
        (5, _('时间段 5: 17:20-19:40')),
        (6, _('时间段 6: 19:40-22:00')),
    ]
    shift = models.IntegerField(choices=SHIFTS, verbose_name="班次", null=True, blank=True)

    def __str__(self):
        weekday_str = dict(self.WEEKDAYS).get(self.weekday, '')
        shift_str = dict(self.SHIFTS).get(self.shift, '')
        return f"{self.staff_name}&{self.volunteer_name} - {self.area} - {weekday_str} - {shift_str}"
