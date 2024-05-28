import re

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from projects.models import Project


def validate_mobile(value):
    if not re.match(r'1[3-9]\d{9}', value):
        raise ValidationError('手机号码格式不正确')


class User(AbstractUser):
    """
    自定义用户类
    """
    # 添加一个mobile字段
    mobile = models.CharField('手机号码', max_length=11, unique=True, help_text='手机号码', null=True, blank=True,
                              error_messages={'unique': '手机号码已注册'}, validators=[validate_mobile])
    project = models.ManyToManyField(Project, help_text='项目', related_name='users')
    weChat_name = models.CharField(max_length=50, help_text='企业微信名称', verbose_name='企业微信名称', null=True, blank=True)
    # 如果希望用email作为用户名
    # USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    # createsuperuser时，希望提示填mobile字段
    REQUIRED_FIELDS = ['mobile']
