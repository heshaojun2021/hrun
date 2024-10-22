# Generated by Django 4.1.13 on 2024-07-18 22:36

from django.db import migrations, models
import django.db.models.deletion
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0005_delete_interface"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mock",
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
                    "creator",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="创建人",
                        max_length=50,
                        null=True,
                        verbose_name="创建人",
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
                    "modifier",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="修改人",
                        max_length=50,
                        null=True,
                        verbose_name="修改人",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        blank=True, help_text="修改时间", null=True, verbose_name="修改时间"
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        blank=True,
                        default=0,
                        help_text="状态",
                        null=True,
                        verbose_name="状态",
                    ),
                ),
                (
                    "mockId",
                    models.CharField(
                        default=projects.models.generate_uuid,
                        max_length=32,
                        unique=True,
                    ),
                ),
                (
                    "newInterface",
                    models.OneToOneField(
                        help_text="接口id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.newinterface",
                        verbose_name="接口id",
                    ),
                ),
            ],
            options={
                "verbose_name": "mock接口表",
                "verbose_name_plural": "mock接口表",
                "db_table": "mock",
            },
        ),
        migrations.CreateModel(
            name="MockDetail",
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
                    "creator",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="创建人",
                        max_length=50,
                        null=True,
                        verbose_name="创建人",
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
                    "modifier",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="修改人",
                        max_length=50,
                        null=True,
                        verbose_name="修改人",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        blank=True, help_text="修改时间", null=True, verbose_name="修改时间"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="期望名称", max_length=50, verbose_name="期望名称"
                    ),
                ),
                (
                    "ipCode",
                    models.IntegerField(
                        blank=True,
                        default=0,
                        help_text="指定生效ip",
                        null=True,
                        verbose_name="指定生效ip",
                    ),
                ),
                (
                    "headers",
                    models.JSONField(
                        blank=True, default=dict, help_text="响应头", verbose_name="响应头"
                    ),
                ),
                (
                    "response",
                    models.JSONField(
                        default={"paramType": "json", "responseData": dict},
                        help_text="响应体",
                        verbose_name="响应体",
                    ),
                ),
                (
                    "config",
                    models.JSONField(
                        default={"statusCode": "200", "time": 0},
                        help_text="配置",
                        verbose_name="配置",
                    ),
                ),
                (
                    "mock",
                    models.ForeignKey(
                        help_text="mock",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.mock",
                        verbose_name="mock",
                    ),
                ),
            ],
            options={
                "verbose_name": "mock接口详情表",
                "verbose_name_plural": "mock接口详情表",
                "db_table": "mockDetail",
            },
        ),
        migrations.CreateModel(
            name="MockLog",
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
                    "interface",
                    models.CharField(
                        help_text="接口路径", max_length=200, verbose_name="接口路径"
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        help_text="请求方法", max_length=50, verbose_name="请求方法"
                    ),
                ),
                (
                    "status_code",
                    models.IntegerField(
                        blank=True, help_text="状态码", null=True, verbose_name="状态码"
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
                    "callIp",
                    models.CharField(
                        help_text="调用ip", max_length=50, verbose_name="调用ip"
                    ),
                ),
            ],
            options={
                "verbose_name": "mock接口日志表",
                "verbose_name_plural": "mock接口日志表",
                "db_table": "mockLog",
            },
        ),
        migrations.CreateModel(
            name="MockDetailForm",
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
                    "location",
                    models.CharField(
                        help_text="参数位置", max_length=50, verbose_name="参数位置"
                    ),
                ),
                (
                    "paramName",
                    models.CharField(
                        help_text="参数名称", max_length=50, verbose_name="参数名称"
                    ),
                ),
                (
                    "comparison",
                    models.CharField(
                        help_text="比较方式", max_length=50, verbose_name="比较方式"
                    ),
                ),
                (
                    "paramValue",
                    models.CharField(
                        help_text="参数值", max_length=50, verbose_name="参数值"
                    ),
                ),
                (
                    "mockDetail",
                    models.ForeignKey(
                        help_text="mock详情",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.mockdetail",
                        verbose_name="mock详情",
                    ),
                ),
            ],
            options={
                "verbose_name": "mock详情数据表",
                "verbose_name_plural": "mock详情数据表",
                "db_table": "mockDetailForm",
            },
        ),
    ]
