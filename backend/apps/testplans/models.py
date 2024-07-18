# -*- coding: utf-8 -*-
# @author: HRUN

import json
from django.db import models
from django.db import transaction

from rest_framework.exceptions import ValidationError

from django_celery_beat.models import PeriodicTask, CrontabSchedule

from projects.models import newInterface


class TestPlan(models.Model):
    """测试计划表"""
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    name = models.CharField(max_length=150, help_text='计划名', verbose_name='计划名')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, help_text='项目id', verbose_name='项目id',
                                related_name='test_plans')
    new_scenes = models.ManyToManyField('TestCase', help_text='包含的测试场景', verbose_name='包含的测试场景', blank=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_test_plan'
        verbose_name_plural = "测试计划表"





class UploadFile(models.Model):
    """文件上传"""
    file = models.FileField(help_text='文件', verbose_name='文件')
    info = models.JSONField(help_text='文件信息', verbose_name='文件信息', default=list)

    def __str__(self):
        return self.file.name

    class Meta:
        db_table = 'tb_upload_file'
        verbose_name = '上传文件'
        verbose_name_plural = verbose_name


class CrontabTask(models.Model):
    """定时任务表"""
    CHOICES = [
        ('1', '开启'),
        ('2', '关闭')
    ]
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, help_text='项目id', verbose_name='项目id',
                                related_name='crontab_jobs')
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    name = models.CharField(max_length=150, help_text='名称', verbose_name='名称', unique=True)
    type = models.IntegerField(verbose_name='任务类型', help_text='任务类型10-测试计划 20-yapi导入', null=True, blank=True)
    plan = models.ForeignKey(TestPlan, help_text='执行任务', verbose_name='执行任务', on_delete=models.PROTECT, null=True, blank=True)
    rule = models.CharField(help_text='定时执行规则', verbose_name='定时任务', max_length=80, default='* * * * *')
    status = models.BooleanField(verbose_name='状态', default=False)
    yapi = models.JSONField(help_text='YAPI导入参数', verbose_name='YAPI导入参数', default=dict, blank=True, null=True)
    env = models.ForeignKey('projects.TestEnv', help_text='执行环境', verbose_name='执行环境', on_delete=models.PROTECT, null=True, blank=True)
    tester = models.CharField('创建人', max_length=20, help_text='创建人', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_crontab_job'
        verbose_name = "定时任务表"
        verbose_name_plural = verbose_name

    """
    当前模式是我们自己项目中的定时任务模型，为了实现定时任务，还需要
    和django-celery-beat中的定时任务模型(PeriodicTask)一对一进行关联。
    我们当前不使用OneToOne字段，直接复写save方法，delete方法实现
    和PeriodicTask的一对一关联。
    """

    def save(self, *args, **kwargs):
        """创建一个当前模型的对象，还要创建一个PeriodicTask的对象"""
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
                # 创建或保存一个PeriodicTask的对象
                self.create_or_update_period_task()
        except Exception:
            raise ValidationError('创建定时任务失败！请联系管理员')

    def delete(self,*args, **kwargs):
        """删除一个当前模型的对象，还要删除对应PeriodicTask的对象"""
        try:
            with transaction.atomic():
                self.delete_periodic_task()
                super().delete(*args, **kwargs)
        except Exception:
            raise ValidationError('删除定时任务失败！请联系管理员')

    def create_or_update_period_task(self):
        """创建或者保存一个PeriodicTask的对象"""
        # 1. 根据当前任务的名称查询一下PeriodicTask是否有数据，有数据说明就是更新，没数据说明就是创建
        queryset = PeriodicTask.objects.filter(description=self.id)
        # 2. 定时任务的参数
        if self.type == 10:
            kwargs = json.dumps({
                'plan_id': self.plan.id,
                'env_id': self.env.id,
                'tester': self.tester,
                'project': self.project_id
            })
        else:
            kwargs = json.dumps(self.yapi)

        if queryset:
            # 更新
            task = queryset.first()
            task.kwargs = kwargs
            task.crontab = self.get_crontab()
            task.enabled = self.status
            task.name = self.name
            task.save()
        else:
            # 创建
            if self.type == 10:
                PeriodicTask.objects.create(
                    name=self.name,
                    task='testplans.tasks.run_crontab_plan',
                    crontab=self.get_crontab(),  # 定时策略
                    kwargs=kwargs,  # 传递的任务参数
                    enabled=self.status,   # 是否启用
                    expire_seconds=3600,  # 任务过期时间
                    description=self.id       # 定时任务id
                )
            else:
                PeriodicTask.objects.create(
                    name=self.name,
                    task='testplans.tasks.run_crontab_yapi',
                    crontab=self.get_crontab(),  # 定时策略
                    kwargs=kwargs,  # 传递的任务参数
                    enabled=self.status,   # 是否启用
                    expire_seconds=3600,  # 任务过期时间
                    description=self.id
                )


    def delete_periodic_task(self):
        """删除对应的PeriodicTask的对象"""
        # 1. 根据当前任务的名称查询出PeriodicTask对象
        queryset = PeriodicTask.objects.filter(description=self.id)
        if queryset:
            queryset.first().delete()

    def get_crontab(self):
        """获取当前任务的crontab对象"""
        crontab_list = self.rule.split(' ')  # 30 20 * * *
        crontab_dict = {
            'minute': crontab_list[0],
            'hour': crontab_list[1],
            'day_of_week': crontab_list[2],
            'day_of_month': crontab_list[3],
            'month_of_year': crontab_list[4]
        }
        # 过滤
        queryset = CrontabSchedule.objects.filter(**crontab_dict)
        if queryset:
            crontab = queryset.first()
        else:
            crontab = CrontabSchedule.objects.create(**crontab_dict)
        return crontab


class TestCase(models.Model):
    """新用例表"""
    project = models.ForeignKey('projects.Project', help_text='所属项目', verbose_name='项目名称', on_delete=models.PROTECT, related_name='testcase')
    name = models.CharField(max_length=50, help_text='用例名称', verbose_name='用例名称')
    stepCount = models.IntegerField(verbose_name='步骤数', help_text='步骤数', null=True, blank=True)
    creator = models.CharField(max_length=50, help_text='创建人', verbose_name='创建人', default='', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    modifier = models.CharField(max_length=50, help_text='修改人', verbose_name='修改人', default='', null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='修改时间', help_text='修改时间', auto_now_add=False, null=True, blank=True)
    desc = models.CharField('用例描述', max_length=200, help_text='用例描述', null=True, blank=True)



    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_testCase'
        verbose_name = "用例表"
        verbose_name_plural = verbose_name



class StepController(models.Model):
    """步骤控制器表"""
    name = models.CharField(max_length=50, help_text='步骤控制器名称', verbose_name='步骤控制器名称')
    dlg = models.BooleanField(default=False, help_text='循环控制器是否展开', verbose_name='循环控制器是否展开')
    inputDlg = models.BooleanField(default=False, help_text='自定义脚本是否展开', verbose_name='自定义脚本是否展开')
    type = models.CharField(max_length=50, help_text='步骤控制器类型', verbose_name='步骤控制器类型')
    content = models.JSONField(help_text='步骤控制器内容', verbose_name='步骤控制器内容', default=dict, blank=True)
    script = models.TextField(help_text='步骤控制器脚本', verbose_name='步骤控制器脚本', default='', null=True, blank=True)
    desc = models.CharField('步骤控制器描述', max_length=200, help_text='步骤控制器描述', null=True, blank=True)
    creator = models.CharField(max_length=50, help_text='创建人', verbose_name='创建人', default='', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    modifier = models.CharField(max_length=50, help_text='修改人', verbose_name='修改人', default='', null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='修改时间', help_text='修改时间', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_StepController'
        verbose_name = "步骤控制器表"
        verbose_name_plural = verbose_name


class CaseStepData(models.Model):
    """用例步骤表"""
    interfaceStep = models.ForeignKey(newInterface, help_text='步骤(接口表)', verbose_name='步骤(接口表)', on_delete=models.PROTECT,null=True, blank=True)
    controllerStep = models.ForeignKey(StepController, help_text='步骤(控制器表)', verbose_name='步骤(控制器表)', on_delete=models.PROTECT,null=True, blank=True)
    case = models.ForeignKey(TestCase, help_text='用例', verbose_name='用例', on_delete=models.PROTECT)
    sort = models.IntegerField(help_text='执行顺序', verbose_name='执行顺序', blank=True)
    status = models.BooleanField(default=True, help_text='是否启用', verbose_name='是否启用')
    parent_id = models.ForeignKey('self', null=True, blank=True, related_name='children',on_delete=models.CASCADE)


    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'tb_CaseStepData'
        verbose_name = "用例步骤表"
        verbose_name_plural = verbose_name
