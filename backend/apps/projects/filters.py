# -*- coding: utf-8 -*-
# @author: HRUN

import django_filters
from django_filters import rest_framework as filters
from .models import  TreeNode, newInterface
from django.db.models import Q


class newInterfaceFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='contains')
    class Meta:
        model = newInterface
        # 过滤字段
        fields = ['name', 'treenode_id', 'creator', 'status']

class treeFilter(filters.FilterSet):
    class Meta:
        model = TreeNode
        fields = ['name']

    def custom_name_filter(self,queryset,name, value):
        model_class = self.Meta.model  # 获取模型类
        return model_class.objects.filter(name__icontains=value).distinct()



