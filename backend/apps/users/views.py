from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from projects.models import Project
from .filters import UserFilter
from .models import User
from common.pagination import TenPerPageNumberPagination
from .serializers import MyTokenSerializer, MyRefreshTokenSerializer, UserRegisterSerializer


class LoginView(TokenObtainPairView):
    """登录视图"""
    serializer_class = MyTokenSerializer


class RefreshTokenView(TokenRefreshView):
    """token刷新视图"""
    serializer_class = MyRefreshTokenSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    pagination_class = TenPerPageNumberPagination
    filterset_class = UserFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get('project')
        # 过滤
        if project:
            queryset = queryset.filter(project=project)
        return queryset

    @action(detail=False, methods=['get'])
    def exclude_project(self, request):
        queryset = super().get_queryset()
        project_id = request.query_params.get('project')
        queryset = queryset.exclude(project=project_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_exclude(self, request):
        data = request.data
        project_id = data.get('project_id')
        user_ids = data.get('users', [])
        if not user_ids:
            return Response({"message": "请选择用户"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({"message": "找不到该项目"}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(pk__in=user_ids)

        # 将用户与项目关联
        project.users.add(*users)

        return Response({"message": "保存成功"}, status=status.HTTP_200_OK)