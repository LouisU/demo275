# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):

    name = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'用户名')
    mobile = models.CharField(max_length=11, verbose_name=u'电话', blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name=u'邮箱')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __unicode__(self):
        return self.name if self.name else self.username
    # return self.name 会报错，说__str__方法返回了一个non-string字段，那是因为self.name字段null=True, blank=True.
    # 所以这里设置成self.username， 因为self.username是不能为空的字段。


class VerifyCode(models.Model):

    mobile = models.CharField(max_length=11, verbose_name=u'电话')
    code = models.CharField(max_length=10, verbose_name=u'验证码')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __unicode__(self):
        return self.code
