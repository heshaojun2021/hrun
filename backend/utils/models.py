# -*- coding: utf-8 -*-
# @author: HRUN

from django.db import models


class BaseModel(models.Model):
    """模型基类
    定义公共字段
    """
    creator = models.CharField(max_length=50, help_text='创建人', verbose_name='创建人', default='', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    modifier = models.CharField(max_length=50, help_text='修改人', verbose_name='修改人', default='', null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='修改时间', help_text='修改时间', auto_now_add=False, null=True, blank=True)

    class Meta:
        # 设置为抽象类
        # 抽象类被别的类继承
        # 数据迁移时，抽象类不会创建对应的表
        abstract = True
