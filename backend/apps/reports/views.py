from datetime import timedelta

from django.utils import timezone

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.cache import cache

from .models import Record
from .serializers import RecordSerializer, ReportSerializer
from .filters import RecordFilterSet


class RecordViewSet(ReadOnlyModelViewSet):
    """测试记录视图集"""
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    # permission_classes = [IsAuthenticated]
    filterset_class = RecordFilterSet

    def get_queryset(self):
        now = timezone.now().date()  # 获取当前日期
        three_days_ago = now - timedelta(days=2)

        if self.request.query_params.get('start_time'):
            queryset = super().get_queryset().order_by('-create_time')
        else:
            queryset = super().get_queryset().filter(create_time__gte=three_days_ago).order_by('-create_time')  # 只获取最近三天的记录

        project = self.request.query_params.get('project')

        # 过滤
        if project:
            queryset = queryset.filter(project=project)

            return queryset

    @action(methods=['get'], detail=True)
    def report(self, request, pk):
        cache_key = f"report_data_{pk}"

        # 尝试从缓存中获取数据
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        try:
            obj = self.get_object()
            serializer = ReportSerializer(instance=obj.report)
            cache.set(cache_key, serializer.data, 3 * 24 * 60 * 60)
            return Response(serializer.data)
        except Exception as e:
            print(f"Error setting cache: {e}")
