from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
