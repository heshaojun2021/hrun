# Generated by Django 4.1.13 on 2024-05-27 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StepController",
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
                        help_text="步骤控制器名称", max_length=50, verbose_name="步骤控制器名称"
                    ),
                ),
                (
                    "dlg",
                    models.BooleanField(
                        default=False, help_text="是否展开", verbose_name="是否展开"
                    ),
                ),
                (
                    "inputDlg",
                    models.BooleanField(
                        default=False, help_text="是否展开", verbose_name="是否展开"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        help_text="步骤控制器类型", max_length=50, verbose_name="步骤控制器类型"
                    ),
                ),
                (
                    "content",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="步骤控制器内容",
                        verbose_name="步骤控制器内容",
                    ),
                ),
                (
                    "script",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="步骤控制器脚本",
                        null=True,
                        verbose_name="步骤控制器脚本",
                    ),
                ),
                (
                    "desc",
                    models.CharField(
                        blank=True,
                        help_text="步骤控制器描述",
                        max_length=200,
                        null=True,
                        verbose_name="步骤控制器描述",
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
            ],
            options={
                "verbose_name": "步骤控制器表",
                "verbose_name_plural": "步骤控制器表",
                "db_table": "tb_StepController",
            },
        ),
        migrations.CreateModel(
            name="TestCase",
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
                        help_text="用例名称", max_length=50, verbose_name="用例名称"
                    ),
                ),
                (
                    "stepCount",
                    models.IntegerField(
                        blank=True, help_text="步骤数", null=True, verbose_name="步骤数"
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
                    "desc",
                    models.CharField(
                        blank=True,
                        help_text="用例描述",
                        max_length=200,
                        null=True,
                        verbose_name="用例描述",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="所属项目",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="testcase",
                        to="projects.project",
                        verbose_name="项目名称",
                    ),
                ),
            ],
            options={
                "verbose_name": "用例表",
                "verbose_name_plural": "用例表",
                "db_table": "tb_testCase",
            },
        ),
        migrations.CreateModel(
            name="UploadFile",
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
                    "file",
                    models.FileField(help_text="文件", upload_to="", verbose_name="文件"),
                ),
                (
                    "info",
                    models.JSONField(
                        default=list, help_text="文件信息", verbose_name="文件信息"
                    ),
                ),
            ],
            options={
                "verbose_name": "上传文件",
                "verbose_name_plural": "上传文件",
                "db_table": "tb_upload_file",
            },
        ),
        migrations.CreateModel(
            name="TestStep",
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
                    "title",
                    models.CharField(
                        help_text="用例名称", max_length=50, verbose_name="用例名"
                    ),
                ),
                (
                    "headers",
                    models.JSONField(
                        blank=True, default=dict, help_text="请求头", verbose_name="请求头"
                    ),
                ),
                (
                    "request",
                    models.JSONField(
                        blank=True, default=dict, help_text="请求信息", verbose_name="请求信息"
                    ),
                ),
                (
                    "file",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="上传的文件参数",
                        verbose_name="上传的文件",
                    ),
                ),
                (
                    "setup_script",
                    models.TextField(
                        blank=True,
                        default="# 前置脚本(python):\n# global_tools:全局工具函数\n# data:用例数据 \n# env: 局部环境\n# ENV: 全局环境\n# db: 数据库操作对象\n",
                        help_text="前置脚本",
                        verbose_name="前置脚本",
                    ),
                ),
                (
                    "teardown_script",
                    models.TextField(
                        blank=True,
                        default="# 后置脚本(python):\n# global_tools:全局工具函数\n# data:用例数据 \n# response:响应对象response \n# env: 局部环境\n# ENV: 全局环境\n# db: 数据库操作对象\n",
                        help_text="后置脚本",
                        verbose_name="用例后置脚本",
                    ),
                ),
                (
                    "interface",
                    models.ForeignKey(
                        help_text="接口",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.interface",
                        verbose_name="接口",
                    ),
                ),
            ],
            options={
                "verbose_name": "测试步骤表",
                "verbose_name_plural": "测试步骤表",
                "db_table": "tb_test_step",
            },
        ),
        migrations.CreateModel(
            name="TestScene",
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
                        help_text="测试场景名", max_length=50, verbose_name="测试场景名"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="所属项目",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="test_scenes",
                        to="projects.project",
                        verbose_name="项目名称",
                    ),
                ),
            ],
            options={
                "verbose_name": "测试场景",
                "verbose_name_plural": "测试场景",
                "db_table": "tb_test_scene",
            },
        ),
        migrations.CreateModel(
            name="TestPlan",
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
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True, help_text="创建时间", verbose_name="创建时间"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="计划名", max_length=150, verbose_name="计划名"
                    ),
                ),
                (
                    "new_scenes",
                    models.ManyToManyField(
                        blank=True,
                        help_text="包含的测试场景",
                        to="testplans.testcase",
                        verbose_name="包含的测试场景",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="项目id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="test_plans",
                        to="projects.project",
                        verbose_name="项目id",
                    ),
                ),
                (
                    "scenes",
                    models.ManyToManyField(
                        blank=True,
                        help_text="包含的测试场景",
                        to="testplans.testscene",
                        verbose_name="包含的测试场景",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "测试计划表",
                "db_table": "tb_test_plan",
            },
        ),
        migrations.CreateModel(
            name="SceneData",
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
                    "sort",
                    models.IntegerField(
                        blank=True, help_text="执行顺序", verbose_name="执行顺序"
                    ),
                ),
                (
                    "scene",
                    models.ForeignKey(
                        help_text="场景",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="testplans.testscene",
                        verbose_name="场景",
                    ),
                ),
                (
                    "step",
                    models.ForeignKey(
                        help_text="步骤",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="testplans.teststep",
                        verbose_name="步骤",
                    ),
                ),
            ],
            options={
                "verbose_name": "场景步骤",
                "verbose_name_plural": "场景步骤",
                "db_table": "tb_scene_data",
            },
        ),
        migrations.CreateModel(
            name="CrontabTask",
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
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True, help_text="创建时间", verbose_name="创建时间"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="名称", max_length=150, unique=True, verbose_name="名称"
                    ),
                ),
                (
                    "type",
                    models.IntegerField(
                        blank=True,
                        help_text="任务类型10-测试计划 20-yapi导入",
                        null=True,
                        verbose_name="任务类型",
                    ),
                ),
                (
                    "rule",
                    models.CharField(
                        default="* * * * *",
                        help_text="定时执行规则",
                        max_length=80,
                        verbose_name="定时任务",
                    ),
                ),
                ("status", models.BooleanField(default=False, verbose_name="状态")),
                (
                    "yapi",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="YAPI导入参数",
                        null=True,
                        verbose_name="YAPI导入参数",
                    ),
                ),
                (
                    "tester",
                    models.CharField(
                        blank=True, help_text="创建人", max_length=20, verbose_name="创建人"
                    ),
                ),
                (
                    "env",
                    models.ForeignKey(
                        blank=True,
                        help_text="执行环境",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="projects.testenv",
                        verbose_name="执行环境",
                    ),
                ),
                (
                    "plan",
                    models.ForeignKey(
                        blank=True,
                        help_text="执行任务",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="testplans.testplan",
                        verbose_name="执行任务",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="项目id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crontab_jobs",
                        to="projects.project",
                        verbose_name="项目id",
                    ),
                ),
            ],
            options={
                "verbose_name": "定时任务表",
                "verbose_name_plural": "定时任务表",
                "db_table": "tb_crontab_job",
            },
        ),
        migrations.CreateModel(
            name="CaseStepData",
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
                    "sort",
                    models.IntegerField(
                        blank=True, help_text="执行顺序", verbose_name="执行顺序"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=True, help_text="是否启用", verbose_name="是否启用"
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        help_text="用例",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="testplans.testcase",
                        verbose_name="用例",
                    ),
                ),
                (
                    "controllerStep",
                    models.ForeignKey(
                        blank=True,
                        help_text="步骤(控制器表)",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="testplans.stepcontroller",
                        verbose_name="步骤(控制器表)",
                    ),
                ),
                (
                    "interfaceStep",
                    models.ForeignKey(
                        blank=True,
                        help_text="步骤(接口表)",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="projects.newinterface",
                        verbose_name="步骤(接口表)",
                    ),
                ),
                (
                    "parent_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="testplans.casestepdata",
                    ),
                ),
            ],
            options={
                "verbose_name": "用例步骤表",
                "verbose_name_plural": "用例步骤表",
                "db_table": "tb_CaseStepData",
            },
        ),
    ]