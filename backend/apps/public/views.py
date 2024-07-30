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

    def analytic_data(self, datasets: list):
        """
        mock接口数据分析层
        """
        success_count = 0
        success_data = []
        # 遍历数据集
        for data in datasets:
            compare_result = self.judge_diff(data.get('conditionForm', []))
            print(compare_result)
            if compare_result:
                # 只统计匹配成功的期望 true
                success_count += 1
                success_data.append(data)

        if success_count > 1:
            # 匹配到多个期望
            return Response({"message": 'mock接口数据集存在多个匹配结果'}, status=status.HTTP_400_BAD_REQUEST)

        elif success_count == 1:
            return success_data[0]

        else:
            # 没有设置期望表单或未匹配上
            return Response({"message": '成功'}, status=status.HTTP_200_OK)
    def judge_diff(self, expect_form: list):
        """
        mock接口数据判断比对
        """
        if len(expect_form) == 1:
            params = expect_form[0]
            source = self.data_source(params.get('location'))
            paramName = params.get('paramName')
            if paramName in source:
                for key in source:
                    source_value = source[key]
                    comparison = self.comparison(source_value,params.get('comparison'),params.get('value',''))
                    if comparison:
                        return True
                    else:
                        return False
            else:
                return False

        elif len(expect_form) > 1:
            for params in expect_form:
                source = self.data_source(params.get('location'))
                paramName = params.get('paramName')
                if paramName in source:
                    for key in source:
                        source_value = source[key]
                        comparison = self.comparison(source_value, params.get('comparison'), params.get('value', ''))
                        if comparison:
                            return True
                        else:
                            return False
                else:
                    return False

        else:
            return True

    def data_source(self,dataType):
        if dataType == 'query':
            query_params = self.request.GET
            params = {}
            # 处理所有的查询参数
            for key in query_params.keys():
                value = query_params.get(key, '')
                params[key] = value
            return params

        elif dataType == 'body':
            return self.request.data

        elif dataType == 'path':
            return self.path

        elif dataType == 'header':
            return self.request.headers

        else:
            return dict

    def comparison(self,source_value, comparison_type: str, value):
        """
        mock传参比对
            source_value: 数据源中的值
            comparison_type: 比对类型
            value: 比对值
        """
        comparison_mapping = {
            'equal': lambda x, y: x == y,
            'notEqual': lambda x, y: x != y,
            'greaterThan': lambda x, y: x > y,
            'lessThan': lambda x, y: x < y,
            'greaterThanOrEqual': lambda x, y: x >= y,
            'lessThanOrEqual': lambda x, y: x <= y,
            'contains': lambda x, y: y in x,
            'notContains': lambda x, y: y not in x,
            'empty': lambda x, y: x is None,
            'notEmpty': lambda x, y: x is not None
        }

        if comparison_type not in comparison_mapping:
            raise ValueError(f"Invalid comparison type: {comparison_type}")

        return comparison_mapping[comparison_type](source_value, value)



    def response(self, data: dict):
        """
        mock接口响应体处理
        """

    def headers(self, data: dict):
        """
        mock接口响应头处理
        """
        pass

    def config(self, data: dict):
        """
        mock接口设置
        """
        pass

    def main(self, method: str):
        """
        mock接口执行层
        """
        # 1、数据校验
        validation_result = self.verification()
        # 检查验证结果
        if isinstance(validation_result, Response):
            return validation_result
        # 2、数据分析
        mock_api_detail, mock_api = validation_result
        # 数据匹配
        analytic_data = self.analytic_data(mock_api_detail)
        if isinstance(analytic_data, Response):
            return analytic_data
        # 3、ip分发校验与结果返回
        if analytic_data.get('ipCode'):
            source_ip = self.request.META.get('REMOTE_ADDR')+':' + self.request.META.get('SERVER_PORT')
            if source_ip in analytic_data.get('ipInput'):
                # ip校验通过执行通过后的处理
                self.response()
                self.headers()
                self.config()
            elif analytic_data.get('ipInput','') is None:
                # ip校验开启了但是没有配置ip，继续获取期望的返回信息
                self.response()
                self.headers()
                self.config()


            else:
                return Response({"message": '访问主机ip校验不通过'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # 未开启ip校验，继续获取期望的返回信息
            self.response()
            self.headers()
            self.config()

        if method == 'GET':
            return self.get(mock_api_detail, mock_api)

    def get(self, mock_api_detail:list, mock_api:Mock):
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