from django_filters import rest_framework as filters

from .models import Record


class RecordFilterSet(filters.FilterSet):
    """测试记录过滤器"""
    project = filters.NumberFilter(field_name='plan__project')
    env = filters.NumberFilter(field_name='test_env')
    start_time = filters.DateTimeFilter(field_name='create_time', lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name='create_time', lookup_expr='lte')

    class Meta:
        model = Record
        fields = ['plan', 'project', 'env', ]
