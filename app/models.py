from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=32, verbose_name='邮箱')
    password = models.CharField(max_length=64, verbose_name='密码')
    admin = models.SmallIntegerField(default=0, verbose_name='管理员')
    name = models.CharField(max_length=32, verbose_name='姓名')
