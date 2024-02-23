from django.db import models


#测试
class Test(models.Model):
    id=models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, verbose_name="用户名")
    password = models.CharField(max_length=50, verbose_name="密码")
    email = models.EmailField(max_length=50, blank=True, default="", verbose_name="邮箱")



# 管理员
class Admin(models.Model):
    user_name = models.CharField(max_length=50, verbose_name="用户名")
    password = models.CharField(max_length=50, verbose_name="密码")
    real_name = models.CharField(max_length=50, blank=True, default="", verbose_name="用户真实姓名")
    sex = models.CharField(max_length=20, blank=True, default="", verbose_name="性别")
    email = models.EmailField(max_length=50, blank=True, default="", verbose_name="邮箱")
    phone = models.CharField(max_length=50, blank=True, default="", verbose_name="电话")
    mobile = models.CharField(max_length=50, blank=True, default="", verbose_name="移动电话")
    description = models.TextField(max_length=200, blank=True, default="", verbose_name="描述")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    created_by = models.IntegerField(blank=True, null=True, verbose_name="创建人")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    updated_by = models.IntegerField(blank=True, null=True, verbose_name="更新人")
    remove = models.BooleanField(default=False, verbose_name="删除标志")
    data_filter = models.TextField(max_length=200, blank=True, default="", verbose_name="数据过滤")
    theme = models.CharField(max_length=45, blank=True, default="", verbose_name="主题")
    default_page = models.CharField(max_length=45, blank=True, default="", verbose_name="缺省页面")
    logo_image = models.CharField(max_length=45, blank=True, default="", verbose_name="Logo")
    qq_openid = models.CharField(max_length=100, blank=True, default="", verbose_name="用于第三方登录的凭证")
    app_version = models.CharField(max_length=10, blank=True, default="1.0", verbose_name="检测app的版本号")
    json_auth = models.TextField(max_length=1000, blank=True, default="{}",
                                 verbose_name="用于app的权限控制（json串里有权限点的配置）")

    class Meta:
        verbose_name = "系统管理员"
        verbose_name_plural = "系统管理员"
        db_table = 'system_administrator'

    def __str__(self):
        return self.user_name


# 老人
class Elder(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('U', '未知'),
    )
    username = models.CharField(max_length=50, verbose_name='老人姓名')
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default='U', verbose_name='性别')
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='电话')
    id_card = models.CharField(max_length=50, unique=True, verbose_name='身份证号')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')  # 允许为空，有可能未知
    checkin_date = models.DateField(null=True, blank=True, verbose_name='入养老院日期')  # 允许为空，初始状态可能未入住
    checkout_date = models.DateField(null=True, blank=True, verbose_name='离开养老院日期')  # 允许为空，初始状态肯定为空
    imgset_dir = models.CharField(max_length=200, blank=True, null=True, verbose_name='图像目录')
    profile_photo = models.CharField(max_length=200, blank=True, null=True, verbose_name='头像路径')
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
    is_active = models.BooleanField(default=True, verbose_name='是否有效')  # 使用BooleanField，默认为True
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    created_by = models.IntegerField(blank=True, null=True, verbose_name='创建人')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    updated_by = models.IntegerField(blank=True, null=True, verbose_name='更新人')
    remove = models.BooleanField(default=False, verbose_name='删除标志')  # 使用BooleanField，默认为False

    class Meta:
        verbose_name = '老人信息'
        verbose_name_plural = '老人信息'
        db_table = 'elder_info'

    def __str__(self):
        return self.username


# 员工
class Staff(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('U', '未知'),
    )
    username = models.CharField(max_length=50, verbose_name='工作人员姓名')
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default='U', verbose_name='性别')
    phone = models.CharField(max_length=50, blank=True, default='', verbose_name='电话')
    id_card = models.CharField(max_length=50, blank=True, default='', verbose_name='身份证号')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    hire_date = models.DateField(null=True, blank=True, verbose_name='入职日期')
    resign_date = models.DateField(null=True, blank=True, verbose_name='离职日期')
    imgset_dir = models.CharField(max_length=200, blank=True, default='', verbose_name='图像目录')
    profile_photo = models.CharField(max_length=200, blank=True, default='', verbose_name='头像路径')
    description = models.TextField(max_length=200, blank=True, default='', verbose_name='描述')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    created_by = models.IntegerField(blank=True, null=True, verbose_name='创建人')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    updated_by = models.IntegerField(blank=True, null=True, verbose_name='更新人')
    remove = models.BooleanField(default=False, verbose_name='删除标志')

    class Meta:
        verbose_name = '工作人员'
        verbose_name_plural = '工作人员'
        db_table = 'staff_info'

    def __str__(self):
        return self.username


# 事件
class Event(models.Model):
    EVENT_TYPES = (
        (0, '情感检测'),
        (1, '义工交互检测'),
        (2, '陌生人检测'),
        (3, '摔倒检测'),
        (4, '禁止区域入侵检测'),
    )
    event_id = models.IntegerField(default=0, choices=EVENT_TYPES, verbose_name='事件id')
    event_date = models.DateTimeField(verbose_name='事件发生时间')
    event_location = models.CharField(max_length=200, blank=True, default='', verbose_name='事件发生地点')
    event_desc = models.TextField(max_length=200, blank=True, default='', verbose_name='事件描述')
    oldperson_id = models.IntegerField(blank=True, null=True, verbose_name='老人id')

    class Meta:
        verbose_name = '事件记录'
        verbose_name_plural = '事件记录'
        db_table = 'event_record'

    def __str__(self):
        return f"{self.get_event_id_display()} - {self.event_date.strftime('%Y-%m-%d %H:%M:%S')}"


# 义工
class Volunteer(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('U', '未知'),
    )
    name = models.CharField(max_length=50, verbose_name="义工姓名")
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default='U', verbose_name="性别")
    phone = models.CharField(max_length=50, blank=True, default="", verbose_name="电话")
    id_card = models.CharField(max_length=50, blank=True, default="", verbose_name="身份证号")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    checkin_date = models.DateField(null=True, blank=True, verbose_name="访问日期")
    checkout_date = models.DateField(null=True, blank=True, verbose_name="离开日期")
    imgset_dir = models.CharField(max_length=200, blank=True, default="", verbose_name="图像目录")
    profile_photo = models.CharField(max_length=200, blank=True, default="", verbose_name="头像路径")
    description = models.TextField(max_length=200, blank=True, default="", verbose_name="描述")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    created_by = models.IntegerField(blank=True, null=True, verbose_name="创建人")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    updated_by = models.IntegerField(blank=True, null=True, verbose_name="更新人")
    remove = models.BooleanField(default=False, verbose_name="删除标志")

    class Meta:
        verbose_name = "义工"
        verbose_name_plural = "义工"
        db_table = 'volunteer_info'

    def __str__(self):
        return self.name
