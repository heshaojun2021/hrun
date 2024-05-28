from django.db import models

from projects.models import Project
from testplans.models import TestPlan

class WxPush(models.Model):
    """企业微信推送表"""
    name = models.CharField(max_length=50, help_text='hook名称', verbose_name='名称')
    webhook = models.CharField(max_length=200, help_text='webhook地址', verbose_name='地址')
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    user_ids = models.TextField(help_text='用户', verbose_name='用户', null=True, blank=True,)
    project_id = models.SmallIntegerField(help_text='项目id', verbose_name='项目id', null=True, blank=True)
    testPlan = models.OneToOneField(TestPlan, help_text='测试计划', verbose_name='测试计划', on_delete=models.SET_NULL,null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_WxPush'
        verbose_name = "企业微信推送表"
        verbose_name_plural = verbose_name

class StatisticalRecord(models.Model):
    """统计记录表"""
    name = models.CharField(max_length=50, help_text='记录名称', verbose_name='记录名称')
    type = models.CharField(max_length=50, help_text='记录类型', verbose_name='记录类型')
    status = models.IntegerField(verbose_name='运行状态', help_text='运行状态', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text='项目id', verbose_name='项目id',
                                related_name='Statistical')
    performer = models.CharField(max_length=50, help_text='执行者', verbose_name='执行者', default='', null=True, blank=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = ' Statistical'
        verbose_name = "统计记录表"
        verbose_name_plural = verbose_name