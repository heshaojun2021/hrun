# -*- coding: utf-8 -*-
# @author: HRUN

from django.db.models import ProtectedError
from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from common.Error_customization import CustomException
from common.pagination import TenPerPageNumberPagination
from public.models import StatisticalRecord
from users.models import User
from .models import Project, Interface, TestEnv, TreeNode, newInterface
from .permissions import IsAuthenticatedOrReadOnly,ProjectPermission
from .serializers import ProjectSerializer, InterfaceSerializer, TestEnvSerializer, TreeNodeSerializer, \
    newInterfaceSerializer
from .filters import InterfaceFilter, treeFilter, newInterfaceFilter

from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from testplans.tasks import run_case, run_scene, run_plan

class ProjectViewSet(ModelViewSet):
    """项目视图集"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission, IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        project = serializer.save(leader=self.request.user, leader_id=self.request.user.id)

        # 获取当前用户对象
        user = self.request.user
        # 将项目与当前用户关联起来
        user.project.add(project)

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.user.id
        try:

            user = User.objects.get(id=user_id)
            project_ids = user.project.values_list('id', flat=True)
        except User.DoesNotExist:
            return []
        if self.request.user.username == 'admin':
            return queryset
        # 过滤
        if project_ids:
            queryset = queryset.filter(id__in=project_ids)
        else:
            queryset = queryset.none()
        return queryset



class InterfaceViewSet(ModelViewSet):
    """接口视图集"""
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = InterfaceFilter
    pagination_class = TenPerPageNumberPagination
    # filterset_fields = ['project', 'type']

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as e:
            raise CustomException()




class TestEnvViewSet(ModelViewSet):
    queryset = TestEnv.objects.all()
    serializer_class = TestEnvSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        # 获取参数
        project = self.request.query_params.get('project')
        # 过滤
        if project:
            queryset = queryset.filter(project=project)

        return queryset


class TreeNodeViewSet(ModelViewSet):
    queryset = TreeNode.objects.filter(parent_id=None).order_by('create_time')
    serializer_class = TreeNodeSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = treeFilter


    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        return Response({'result': data, 'message': '成功', 'code': 200})

    def destroy(self, request, *args, **kwargs):
        re = self.kwargs['pk']
        instance = TreeNode.objects.filter(id=re)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def get_queryset(self):
        queryset = super().get_queryset()
        # 获取参数
        project = self.request.query_params.get('project_id')
        # 过滤
        if project:
            queryset = queryset.filter(project_id=project)

        return queryset


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = TreeNode.objects.get(pk=request.data.get('id'))
        serializer = TreeNodeSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

class newInterfaceViewSet(ModelViewSet):
    """接口视图集"""
    queryset = newInterface.objects.all().order_by('-create_time')
    serializer_class = newInterfaceSerializer
    # permission_classes = [IsAuthenticated]
    filterset_class = newInterfaceFilter

    @action(methods=['post'], detail=False)
    def delete_batch(self, request, *args, **kwargs):
        item_ids = request.data.get('item_ids', [])  # 获取传递的item_ids列表
        if item_ids:
            items = newInterface.objects.filter(id__in=item_ids)  # 根据item_ids查询要删除的对象
            items.delete()  # 执行批量删除操作
            return Response({'message': '删除成功'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '列表不可为空'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def run(self, request, *args, **kwargs):
        # 1. 获取测试数据
        cases = request.data.get('data')
        env_id = request.data.get('env')
        if not env_id:
            raise ValidationError('请求参数env必填')
        try:
            TestEnv.objects.get(id=env_id)
        except:
            raise ValidationError('参数env传入的值无效')

        res = run_case(cases=cases, env_id=env_id)
        project = Project.objects.get(id=cases.get('project'))
        StatisticalRecord.objects.create(
            name=cases.get('name'),
            type='api',
            status=1,
            project=project,
            performer=request.user)

        return Response(res)

