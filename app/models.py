from django.db import models



class SystemAdministrator(models.Model):
    # 定义模型字段
    user_name = models.CharField(max_length=50, verbose_name='用户名')
    password = models.CharField(max_length=50, verbose_name='密码')
    real_name = models.CharField(max_length=50, blank=True, verbose_name='用户真实姓名')
    sex = models.CharField(max_length=20, blank=True, verbose_name='性别')
    email = models.EmailField(max_length=50, blank=True, verbose_name='邮箱')
    phone = models.CharField(max_length=50, blank=True, verbose_name='电话')
    mobile = models.CharField(max_length=50, blank=True, verbose_name='移动电话')
    description = models.TextField(max_length=200, blank=True, verbose_name='描述')
    is_active = models.CharField(max_length=10, blank=True, verbose_name='是否有效')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    created_by = models.IntegerField(blank=True, null=True, verbose_name='创建人')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    updated_by = models.IntegerField(blank=True, null=True, verbose_name='更新人')
    remove = models.CharField(max_length=1, blank=True, verbose_name='删除标志')
    data_filter = models.TextField(max_length=200, blank=True, verbose_name='数据过滤')
    theme = models.CharField(max_length=45, blank=True, verbose_name='主题')
    default_page = models.CharField(max_length=45, blank=True, verbose_name='缺省页面')
    logo_image = models.CharField(max_length=45, blank=True, verbose_name='Logo')
    qq_openid = models.CharField(max_length=100, blank=True, verbose_name='第三方登录凭证')
    app_version = models.CharField(max_length=10, blank=True, verbose_name='APP版本号')
    json_auth = models.TextField(max_length=1000, blank=True, verbose_name='APP权限控制')

    class Meta:
        verbose_name = '系统管理员'
        verbose_name_plural = '系统管理员'
        # 指定数据库表名
        db_table = 'system_administrator'

    def __str__(self):
        return self.user_name

