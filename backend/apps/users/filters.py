from django_filters import rest_framework as filters
from .models import User


class UserFilter(filters.FilterSet):
    project_name = filters.CharFilter(field_name='project__name')

    class Meta:
        model = User
        # 过滤字段
        fields = ['email', 'mobile', 'username', 'project_name']

