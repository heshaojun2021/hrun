# -*- coding: utf-8 -*-
# @author: HRUN

from django_filters import rest_framework as filters

from .models import TestCase, TestPlan





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