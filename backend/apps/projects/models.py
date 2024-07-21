# -*- coding: utf-8 -*-
# @author: HRUN

from pathlib import Path
import uuid

from django.db import models
from utils.models import BaseModel
from reports.models import Record
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def generate_uuid():
    return uuid.uuid4().hex


class Project(models.Model):
    """项目表"""
    name = models.CharField(max_length=50, help_text='项目名称', verbose_name='项目名')
    desc = models.CharField('项目描述', max_length=200, help_text='项目描述', null=True, blank=True)
    leader = models.CharField(max_length=50, help_text='负责人', verbose_name='负责人', default='', null=True, blank=True)
    leader_id = models.SmallIntegerField(help_text='负责人id', verbose_name='负责人id', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'project'
        verbose_name = "项目表"
        verbose_name_plural = verbose_name



class TestEnv(models.Model):
    """测试环境表"""
    name = models.CharField(max_length=150, help_text='环境名称', verbose_name='环境名称')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text='项目id', verbose_name='项目id', related_name='test_envs')
    global_variable = models.JSONField(help_text='全局变量', verbose_name='全局变量', default=dict, null=True, blank=True)
    debug_global_variable = models.JSONField(help_text='debug模式全局变量', verbose_name='debug模式全局变量', default=dict, null=True, blank=True)
    db = models.JSONField(help_text='数据库配置', verbose_name='数据库配置', default=list, null=True, blank=True)
    host = models.CharField(help_text='base_url地址', verbose_name='base_url地址', max_length=100, blank=True)
    headers = models.JSONField(help_text='请求头', verbose_name='请求头', default=dict, null=True, blank=True)
    global_func = models.TextField(help_text='用例工具文件', verbose_name='用例工具文件',
                                   default=open((BASE_DIR / 'utils/global_func.py'), 'r', encoding='utf-8').read(), null=True,
                                   blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_test_env'
        verbose_name = "测试环境表"
        verbose_name_plural = verbose_name



class TreeNode(models.Model):
    """树形结构表"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text='项目id', verbose_name='项目id',
                                related_name='treenodes')
    name = models.CharField(max_length=100, verbose_name='结构名称', help_text='结构名称')
    type = models.IntegerField(verbose_name='接口类型', help_text='暂时不用',null=True, blank=True)
    parent_id = models.ForeignKey('self', null=True, blank=True, related_name='children',on_delete=models.CASCADE)
    enable_flag = models.IntegerField(verbose_name='删除', help_text='是否可用 10-可用 20-删除', default=10)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'TreeNode'
        verbose_name = "树结构表"
        verbose_name_plural = verbose_name





setup_script = """# 前置脚本(python):
# global_tools:全局工具函数
# data:用例数据 
# env: 局部环境
# ENV: 全局环境
# db: 数据库操作对象
"""
teardown_script = """# 后置脚本(python):
# global_tools:全局工具函数
# data:用例数据 
# response:响应对象response 
# env: 局部环境
# ENV: 全局环境
# db: 数据库操作对象
"""

class newInterface(models.Model):
    """新接口表"""
    CHOICES = [
        ('开发中', '开发中'),
        ('测试中', '测试中'),
        ('已发布', '已发布'),
        ('已废弃', '已废弃')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text='项目id', verbose_name='项目id',
                                related_name='new_interface')
    treenode = models.ForeignKey(TreeNode, on_delete=models.CASCADE, help_text='节点id', verbose_name='节点id', related_name='newinterface')
    name = models.CharField(max_length=50, help_text='接口名称', verbose_name='接口名')
    host = models.JSONField( help_text='域名', verbose_name='域名', default=dict, blank=True)
    url = models.CharField(max_length=200, help_text='接口路径', verbose_name='接口路径')
    method = models.CharField(max_length=50, help_text='请求方法', verbose_name='请求方法')
    headers = models.JSONField(help_text='请求头', verbose_name='请求头', default=dict, blank=True)
    request = models.JSONField(help_text='请求信息', verbose_name='请求信息', default=dict, blank=True)
    file = models.JSONField(help_text='上传的文件参数', verbose_name='上传的文件', default=list, blank=True)
    setup_script = models.TextField(help_text='前置脚本', verbose_name='前置脚本', default=setup_script, blank=True)
    teardown_script = models.TextField(help_text='后置脚本', verbose_name='用例后置脚本', default=teardown_script, blank=True)
    interface_tag = models.JSONField(help_text='tag标签', verbose_name='tag标签', default=list, blank=True)
    creator = models.CharField(max_length=50, help_text='创建人', verbose_name='创建人', default='', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    modifier = models.CharField(max_length=50, help_text='修改人', verbose_name='修改人', default='', null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='修改时间', help_text='修改时间', auto_now_add=False, null=True, blank=True)
    desc = models.CharField('接口描述', max_length=200, help_text='接口描述', null=True, blank=True)
    type = models.CharField(max_length=20, help_text='类型', verbose_name='类型', default='api')
    YApi_id = models.IntegerField(verbose_name='YApi接口id', help_text='YApi接口id', null=True, blank=True)
    YApi_status = models.IntegerField(verbose_name='YApi接口状态', help_text='YApi接口状态', null=True, blank=True, default=0)
    status = models.CharField(verbose_name='状态', help_text='接口状态', max_length=40, choices=CHOICES, default='状态')
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_newInterface'
        verbose_name = "新接口表"
        verbose_name_plural = verbose_name




class Mock(BaseModel):
    """mock接口表"""
    newInterface = models.OneToOneField(newInterface, on_delete=models.CASCADE, help_text='接口id', verbose_name='mock',)
    name = models.CharField(max_length=50, help_text='接口名称', verbose_name='接口名')
    method = models.CharField(max_length=50, help_text='请求方法', verbose_name='请求方法')
    url = models.CharField(max_length=200, help_text='接口路径', verbose_name='接口路径')
    status = models.BooleanField(verbose_name='状态', default=False)
    mockId = models.CharField(max_length=32, default=generate_uuid, unique=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'mock'
        verbose_name = "mock接口表"
        verbose_name_plural = verbose_name



class MockDetail(BaseModel):
    """mock接口详情表"""
    mock = models.ForeignKey(Mock, on_delete=models.CASCADE, help_text='mock', related_name='MockDetail')
    name = models.CharField(max_length=50, help_text='期望名称', verbose_name='期望名称')
    conditionForm = models.JSONField(help_text='条件', verbose_name='条件', default=list, blank=True)
    ipCode = models.BooleanField(verbose_name='是否开启生效ip', default=False)
    ipInput = models.CharField(max_length=50, help_text='生效ip', verbose_name='生效ip', null=True, blank=True)
    headers = models.JSONField(help_text='响应头', verbose_name='响应头', default=dict, blank=True)
    response = models.JSONField(help_text='响应体', verbose_name='响应体', default=dict, blank=True)
    config = models.JSONField(help_text='配置', verbose_name='配置', default=dict, blank=True)


    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'mockDetail'
        verbose_name = "mock接口详情表"
        verbose_name_plural = verbose_name



class MockLog(models.Model):
    """mock接口日志表"""
    interface = models.CharField(max_length=200, help_text='接口路径', verbose_name='接口路径')
    method = models.CharField(max_length=50, help_text='请求方法', verbose_name='请求方法')
    status_code = models.IntegerField(verbose_name='状态码', help_text='状态码', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    callIp = models.CharField(max_length=50, help_text='调用ip', verbose_name='调用ip')


    def __str__(self):
        return self.id

    class Meta:
        db_table = 'mockLog'
        verbose_name = "mock接口日志表"
        verbose_name_plural = verbose_name