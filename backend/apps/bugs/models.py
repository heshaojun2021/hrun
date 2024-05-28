from django.db import models


class Bug(models.Model):
    CHOICES = [
        ('待处理', '待处理'),
        ('处理中', '处理中'),
        ('已关闭', '已关闭'),
        ('处理完成', '处理完成'),
        ('无需处理', '无需处理')
    ]
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, help_text='项目id', verbose_name='项目id')
    interface = models.ForeignKey('projects.newInterface', on_delete=models.CASCADE, help_text='接口', verbose_name='接口')
    desc = models.TextField(help_text='bug描述', verbose_name='bug描述', max_length=3000, blank=True)
    info = models.JSONField(help_text='测试报告', verbose_name='测试报告', default=dict, blank=True)
    status = models.CharField(verbose_name='状态', help_text='bug状态', max_length=40, choices=CHOICES, default='1')
    user = models.CharField(verbose_name='提交者', help_text='提交者', max_length=40, default='', blank=True)
    remark = models.TextField(help_text='备注', verbose_name='备注', max_length=3000, blank=True)

    class Meta:
        db_table = 'tb_bug'
        verbose_name = 'bug表'
        verbose_name_plural = verbose_name


class BugHandle(models.Model):
    """bug处理记录表"""
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    bug = models.ForeignKey('Bug', on_delete=models.CASCADE, help_text='bug ID', verbose_name='bug ID')
    handle = models.TextField(help_text='处理操作', verbose_name='处理操作', blank=True)
    update_user = models.CharField(max_length=32, verbose_name='更新用户', help_text='处理操作', blank=True)
    remark = models.TextField(help_text='备注', verbose_name='备注', max_length=3000, blank=True)

    class Meta:
        db_table = 'tb_bug_handle'
        verbose_name = "bug操作记录表"
        verbose_name_plural = verbose_name
