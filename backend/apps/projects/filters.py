import django_filters
from django_filters import rest_framework as filters
from .models import Interface, TreeNode, newInterface
from django.db.models import Q

class InterfaceFilter(filters.FilterSet):
    # 字段名是查询参数名
    # field_name参数就是实际查询的字段
    project_name_contains = filters.CharFilter(field_name="project__name", lookup_expr='contains')
    # Interface.objects.filter(project__name__contains='前')

    class Meta:
        model = Interface
        # 过滤字段
        fields = ['project', 'type','name','url','method']

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



