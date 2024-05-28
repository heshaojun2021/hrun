from django_filters import rest_framework as filters

from .models import TestStep, TestCase, TestPlan


class TestStepFilterSet(filters.FilterSet):
    """测试步骤过滤器"""
    scene = filters.NumberFilter(field_name='scenedata__scene')

    class Meta:
        model = TestStep
        fields = ['scene', 'interface']


class TestCaseFilter(filters.FilterSet):
    """测试用例过滤器"""
    name = filters.CharFilter(field_name="name", lookup_expr='contains')
    class Meta:
        model = TestCase
        # 过滤字段
        fields = ['name', 'testplan']


class TestPlanFilter(filters.FilterSet):
    """测试用例过滤器"""
    name = filters.CharFilter(field_name="name", lookup_expr='contains')
    class Meta:
        model = TestPlan
        # 过滤字段
        fields = ['name', 'project']