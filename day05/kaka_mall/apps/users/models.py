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
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

# 用户地址模型类
from utils.models import BaseModel

class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='用户地址')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']