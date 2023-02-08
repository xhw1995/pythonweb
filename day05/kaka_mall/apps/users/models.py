from django.db import models

# Create your models here.
"""
1 自定义模型
密码需要加密
需要实现登录时的密码验证
"""
# class User(models.Model):
#    username = models.CharField(max_length=20, unique=True)
#    password = models.CharField(max_length=20)
#    mobile = models.CharField(max_length=11, unique=True)

"""
2 django 自带用户模型
自带模型有 密码加密和密码验证功能
"""
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)
    email_active = models.BooleanField(default=False, verbose_name="邮箱验证状态")

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name