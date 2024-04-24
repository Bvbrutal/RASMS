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
    grade = models.IntegerField(choices=GRADE_CHOICES, default='4', verbose_name='类别')
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
    description = models.TextField(verbose_name="描述", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="开始时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="结束时间", null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name="地点", null=True, blank=True)
    organizer = models.CharField(max_length=255, verbose_name="主办方", null=True, blank=True)
    participant_limit = models.IntegerField(verbose_name="参与人数限制", null=True, blank=True)
    registration_status = models.BooleanField(default=True, verbose_name="报名状态")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not_started', verbose_name="活动状态")
    contact_info = models.CharField(max_length=255, verbose_name="联系信息", null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="费用", null=True, blank=True)
    image = models.ImageField(upload_to='communityevents/', verbose_name="图片/海报", null=True, blank=True)
    category = models.CharField(max_length=255, verbose_name="分类", null=True, blank=True)
    registration_link = models.URLField(verbose_name="注册/报名链接", max_length=1024, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='创键时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
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


# 社区活动报名人数统计
class Registration(models.Model):
    user = models.ForeignKey(Elder, on_delete=models.CASCADE, related_name="registrations")
    event = models.ForeignKey(CommunityEvent, on_delete=models.CASCADE, related_name="registrations")
    timestamp = models.DateTimeField(auto_now_add=True)


# 社区公告管理
class CommunityAnnouncement(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    introduction = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介")
    content = models.TextField(verbose_name="内容")
    published_date = models.DateTimeField(null=True, blank=True, verbose_name="发布日期")
    expiry_date = models.DateTimeField(null=True, blank=True, verbose_name="过期日期")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="发布者")
    publisher = models.CharField(max_length=255, null=True, blank=True, verbose_name="发布方")
    announcement_photo = models.ImageField(upload_to='announcement_photo/', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='登录时间', blank=True, null=True)
    user_by = models.ForeignKey(User, related_name='%(class)s_user_by', on_delete=models.SET_NULL, blank=True,
                                null=True, verbose_name='账户')

    class Meta:
        verbose_name = '访问用户信息'
        verbose_name_plural = verbose_name


# 网站总访问次数
class VisitNumber(models.Model):
    count = models.IntegerField(verbose_name='网站访问总次数', default=0)  # 网站访问总次数

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
