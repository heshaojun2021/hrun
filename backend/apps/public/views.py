# -*- coding: utf-8 -*-
# @author: HRUN

from django.core.cache import cache
from django.http import HttpRequest, HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from public.models import WxPush
from public.serializers import WxPushSerializer
from projects.models import Project, Mock, MockDetail


from common.pagination import TenPerPageNumberPagination
from .tasks import import_run_yapi
from common.ProjectBoard import ProjectBoard



class WxPushViewSet(ModelViewSet):
    """项目视图集"""
    queryset = WxPush.objects.all().order_by('-create_time')
    serializer_class = WxPushSerializer
    pagination_class = TenPerPageNumberPagination
    filterset_fields = ['project_id']

    def get_queryset(self):
        queryset = super().get_queryset()
        # 获取参数
        project = self.request.query_params.get('project')
        # 过滤
        if project:
            queryset = queryset.filter(project_id=project)

        return queryset


class YApiViewSet(APIView):
    """
    YApi数据导入
    """
    def post(self, request, *args):
        try:
            import_run_yapi(request.data)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProjectBoardView(APIView):
    def post(self, request, *args, **kwargs):
        project_id = request.data.get('project')
        starttime = request.data.get('starttime', None)
        endtime = request.data.get('endtime', None)

        # 构建用于缓存的键
        cache_key = f"project_data_{project_id}_{starttime}_{endtime}"

        # 尝试从缓存中获取数据
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        try:
            project = Project.objects.get(id=project_id)
            if project:
                main = ProjectBoard(project)
                data = main.get_project_data_summary(starttime, endtime)
                # 将数据存入 Redis 缓存
                cache.set(cache_key, data, timeout=120)  # 设置缓存有效期为1小时
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "项目不存在"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class MockEngine:
    def __init__(self, request, path, mock_id):
        self.request = request
        self.path = path
        self.mock_id = mock_id

    def verification(self):
        """
        mock接口数据校验层
        """
        mock_api_detail = []
        try:
            mock_api = Mock.objects.get(mockId=self.mock_id)
            for detail in mock_api.MockDetail.values():
                mock_api_detail.append(detail)

            if not mock_api.status:
                return Response({"message": 'mock接口已禁用'}, status=status.HTTP_400_BAD_REQUEST)

            return mock_api_detail, mock_api

        except Mock.DoesNotExist:
            return Response({"message": 'mock接口不存在'}, status=status.HTTP_404_NOT_FOUND)

    def analytic_data(self, datasets):
        """
        mock接口数据分析层
        """
        # 遍历数据集
        for data in datasets:
            pass


    def main(self, method):
        """
        mock接口执行层
        """
        # 数据校验
        validation_result = self.verification()
        # 检查验证结果
        if isinstance(validation_result, Response):
            return validation_result

        mock_api_detail, mock_api = validation_result
        # 数据分析拆解
        self.analytic_data(mock_api_detail)

        if method == 'GET':
            return self.get(mock_api_detail, mock_api)

    def get(self, mock_api_detail, mock_api):
        query_params = self.request.GET
        params = {}
        # 处理所有的查询参数
        for key in query_params.keys():
            value = query_params.get(key, '')
            params[key] = value

        return Response({"path": self.path, "mock_id": self.mock_id, **params}, status=status.HTTP_200_OK)






class MockAPIView(APIView):
    """
    MockAPIView
    """

    def get(self, request: HttpRequest, path: str, mock_id: str) -> Response:
        return MockEngine(request, path, mock_id).main(request.method)



    def post(self, request: HttpRequest, path: str, mock_id: str) -> Response:
        return Response({"message": '我是post'}, status=status.HTTP_200_OK)

    def put(self, request: HttpRequest, path: str, mock_id: str) -> Response:
        return Response({"message": '我是put'}, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, path: str, mock_id: str) -> Response:
        pass