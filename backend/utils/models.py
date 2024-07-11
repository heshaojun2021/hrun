# -*- coding: utf-8 -*-
# @author: HRUN

from django.db import models


class BaseModel(models.Model):
    """模型基类
    定义公共字段
    """
    is_delete = models.BooleanField('逻辑删除', help_text='逻辑删除', default=False)

    class Meta:
        # 设置为抽象类
        # 抽象类被别的类继承
        # 数据迁移时，抽象类不会创建对应的表
        abstract = True
