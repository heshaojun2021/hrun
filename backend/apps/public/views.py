from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from public.models import WxPush
from public.serializers import WxPushSerializer
from projects.models import Project

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