# Generated by Django 4.1.13 on 2024-05-27 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("projects", "0001_initial"),
        ("testplans", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WxPush",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="hook名称", max_length=50, verbose_name="名称"
                    ),
                ),
                (
                    "webhook",
                    models.CharField(
                        help_text="webhook地址", max_length=200, verbose_name="地址"
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="创建时间",
                        null=True,
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "user_ids",
                    models.TextField(
                        blank=True, help_text="用户", null=True, verbose_name="用户"
                    ),
                ),
                (
                    "project_id",
                    models.SmallIntegerField(
                        blank=True, help_text="项目id", null=True, verbose_name="项目id"
                    ),
                ),
                (
                    "testPlan",
                    models.OneToOneField(
                        blank=True,
                        help_text="测试计划",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="testplans.testplan",
                        verbose_name="测试计划",
                    ),
                ),
            ],
            options={
                "verbose_name": "企业微信推送表",
                "verbose_name_plural": "企业微信推送表",
                "db_table": "tb_WxPush",
            },
        ),
        migrations.CreateModel(
            name="StatisticalRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="记录名称", max_length=50, verbose_name="记录名称"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        help_text="记录类型", max_length=50, verbose_name="记录类型"
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        blank=True, help_text="运行状态", null=True, verbose_name="运行状态"
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="创建时间",
                        null=True,
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "performer",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="执行者",
                        max_length=50,
                        null=True,
                        verbose_name="执行者",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="项目id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Statistical",
                        to="projects.project",
                        verbose_name="项目id",
                    ),
                ),
            ],
            options={
                "verbose_name": "统计记录表",
                "verbose_name_plural": "统计记录表",
                "db_table": " Statistical",
            },
        ),
    ]
