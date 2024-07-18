# -*- coding: utf-8 -*-
# @author: HRUN

import os

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from common.pagination import TenPerPageNumberPagination
from projects.models import TestEnv, newInterface, Project
from .models import  TestPlan, UploadFile, CrontabTask, TestCase, CaseStepData, StepController
from public.models import StatisticalRecord
from .serializers import (
     UploadFileSerializer,TestPlanSerializer,RecordSerializer, CrontabTaskSerializer,
     TestCaseSerializer, TestCaseStepSerializer, StepControllerSerializer
)
from .filters import TestCaseFilter, TestPlanFilter
from .tasks import run_case, run_scene, run_plan



class UploadFileViewSet(ModelViewSet):
    """文件上传"""
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer
    permission_classes = [IsAuthenticated]

    # 复写perform_create
    def perform_create(self, serializer):
        # 1. 限制文件大小
        size = self.request.data['file'].size
        name = self.request.data['file'].name
        if size > 1024 * 300:
            raise ValidationError('上传失败，文件大小不能超过300kb!')
            # return Response({'msg': '上传失败，文件大小不能超过300kb!', 'data': None}, status=400)
        if os.path.isfile(settings.MEDIA_ROOT / name):
            raise ValidationError(f'上传失败，【{name}】已存在！')
            # return Response({'msg': f'上传失败，【{name}】已存在！', 'data': None}, status=400)
        # 2. 生成info数据
        file_type = self.request.data['file'].content_type
        path = str(settings.MEDIA_ROOT / name)
        info = [name, path, file_type]

        serializer.save(info=info)

    # 复写perform_destroy实现删除文件
    def perform_destroy(self, instance):
        """文件删除"""
        # 删除本地保存的文件
        os.remove(instance.file.path)
        instance.delete()



class TestCaseStepViewSet(ModelViewSet):
    """测试用例步骤视图集"""
    queryset = CaseStepData.objects.all().filter(parent_id=None).order_by('sort')
    serializer_class = TestCaseStepSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['case']

    @action(detail=True, methods=['delete'])
    def delete_node(self, request, pk=None):
        try:
            instance = CaseStepData.objects.get(pk=pk)
            if instance.parent_id:
                if CaseStepData.objects.filter(parent_id=instance.id).exists():
                    return Response({"message": "存在未删除的子节点，请先删除子节点后再操作"}, status=status.HTTP_400_BAD_REQUEST)
                CaseStepData.objects.filter(id=instance.id).delete()
            else:
                if CaseStepData.objects.filter(parent_id=instance.id).exists():
                    return Response({"message": "存在未删除的子节点，请先删除子节点后再操作"}, status=status.HTTP_400_BAD_REQUEST)
                instance.delete()
            return Response({"message": "操作成功"},status=status.HTTP_204_NO_CONTENT)

        except CaseStepData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False)
    def batch_create(self, request, *args, **kwargs):
        """批量创建接口"""
        data = request.data  # 获取请求中的数据
        if not data:
            return Response({'message': '提交的数据不可是空列表'}, status=status.HTTP_400_BAD_REQUEST)
        objs = []
        if isinstance(data, list):
            for item in data:
                sort = item.get('sort')
                case_id = item.get('case')
                interfaceStep_id = item.get('interfaceStep')

                if sort is not None and case_id is not None and interfaceStep_id is not None:
                    interfaceStep = newInterface.objects.get(pk=interfaceStep_id)
                    case = TestCase.objects.get(pk=case_id)
                    obj = CaseStepData(sort=sort, case=case, interfaceStep=interfaceStep)
                    objs.append(obj)
                else:
                    return Response({'message': '缺失必填参数'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': '输出对象应该是一个列表'}, status=status.HTTP_400_BAD_REQUEST)

        # 一次性保存所有对象
        CaseStepData.objects.bulk_create(objs)

        return Response({'message':'创建成功'}, status=status.HTTP_201_CREATED)

    def update_step_data(self, data, parent_id=None):
        for item in data:
            obj = CaseStepData.objects.get(pk=item['id'])
            obj.sort = item['sort']
            obj.status = item['status']
            obj.parent_id = parent_id
            obj.save()
            if 'children' in item and item['children']:
                self.update_step_data(item['children'], parent_id=obj)

    @action(methods=['put'], detail=False)
    def order(self, request, *args, **kwargs):
        """排序接口"""
        for item in request.data:
            self.update_step_data([item])
        return Response(request.data)

class TestPlanViewSet(ModelViewSet):
    """测试计划视图集"""
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TestPlanFilter

    @action(methods=['post'], detail=True)
    def run(self, request, pk):
        if not self.queryset.get(id=pk).new_scenes.all():
            return Response({'message': '该计划下无测试场景，请添加后再试'}, status=status.HTTP_400_BAD_REQUEST)
        plan = self.get_object()
        # 1. 获取环境id
        env_id = request.data.get('env')
        # 2. 生成测试记录
        serializer = RecordSerializer(data={
            'test_env': env_id,
            'plan': pk,
            'status': '执行中',
            'tester': request.user.username,
            'project': plan.project_id,
            'execute_type': '手动执行'
        })
        serializer.is_valid(raise_exception=True)
        record = serializer.save()
        # 同步执行测试计划
        if os.environ.get('ENV') == 'production':
            # 异步执行
            run_plan.delay(pk, env_id, record_id=record.id)
        else:
            # 同步执行
            run_plan(pk, env_id, record_id=record.id)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_new_scenes(self, request, pk=None):
        plan = self.get_object()
        scene_ids = request.data.get('scene_ids', [])

        for scene_id in scene_ids:
            testcase = TestCase.objects.get(id=scene_id)  # 获取要添加的 TestCase 对象
            plan.new_scenes.add(testcase)  # 向中间表添加关联数据
        return Response({'message': '新增成功'})

    @action(detail=True, methods=['post'])
    def remove_new_scene(self, request, pk=None):
        plan = self.get_object()
        scene_id = request.data.get('scene_id')
        new_scene = TestCase.objects.get(id=scene_id)
        plan.new_scenes.remove(new_scene)
        return Response({'message': '删除成功'})


class CrontabTaskViewSet(ModelViewSet):
    queryset = CrontabTask.objects.all()
    serializer_class = CrontabTaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'plan']

    def perform_create(self, serializer):
        serializer.save(tester=self.request.user.username)


class TestCaseViewSet(ModelViewSet):
    """用例接口视图"""
    queryset = TestCase.objects.all().order_by('-create_time')
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TestCaseFilter
    pagination_class = TenPerPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # 获取参数
        project = self.request.query_params.get('project_id')
        # 过滤
        if project:
            queryset = queryset.filter(project_id=project)

        return queryset

    @action(methods=['post'], detail=True)
    def run(self, request, pk):
        # 1. 获取环境id
        env_id = request.data.get('env')
        # 2. 执行测试场景
        res = run_scene(pk, env_id)
        try:
            case = get_object_or_404(self.queryset, pk=pk)
            project = Project.objects.get(id=case.project_id)
            StatisticalRecord.objects.create(
                name=case.name,
                type='case',
                status=1,
                project=project,
                performer=request.user)
            return Response(res)
        except Exception as e:
            print(e)
            return Response(res)


class StepControllerViewSet(ModelViewSet):
    """步骤控制器视图集"""
    queryset = StepController.objects.all()
    serializer_class = StepControllerSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False)
    def copyStep(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        parent = CaseStepData.objects.filter(id=request.data.get('parent_id')).first()
        if parent:
            SetpCase = CaseStepData.objects.create(case_id=request.data.get('case'),
                                                   sort=request.data.get('sort'),
                                                   controllerStep_id=instance.id,
                                                   parent_id=parent)
        else:
            SetpCase = CaseStepData.objects.create(case_id=request.data.get('case'),
                                                   sort=request.data.get('sort'),
                                                   controllerStep_id=instance.id)

        serializer.instance.setpId = SetpCase.id

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['put'], detail=False)
    def batch_updateStep(self, request, *args, **kwargs):
        try:
            data = request.data
            if not isinstance(data, list):
                return Response({'message': '传入的数据不是list类型'}, status=400)

            # 定义递归函数来处理children中的数据
            def process_children(data):
                for item in data:
                    # 提取stepInfo数据
                    step_info = item.get('stepInfo', None)
                    if step_info is None:
                        return Response({'message': '数据缺少stepInfo'}, status=400)

                    # 检查stepInfo中的type是否为api，如果是，则跳过该节点
                    if step_info.get('type') == 'api':
                        continue

                    # 获取主键
                    pk = step_info.get('id', None)
                    if pk is None:
                        return Response({'message': '数据缺少标识'}, status=400)

                    # 删除不需要的键
                    item['stepInfo'].pop('id', None)
                    item['stepInfo'].pop('inputDlg', None)
                    item['stepInfo'].pop('dlg', None)
                    item['stepInfo'].pop('creator', None)

                    # 更新或创建StepController对象
                    StepController.objects.update_or_create(pk=pk, defaults=step_info)

                    # 递归处理children
                    children = item.get('children', [])
                    if children:
                        process_children(children)

            # 调用递归函数处理数据
            process_children(data)

            return Response(request.data, status=200)

        except Exception as e:
            return Response({'message': str(e)}, status=400)