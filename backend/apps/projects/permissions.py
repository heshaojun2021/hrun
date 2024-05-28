from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        """
        要么登录要么只读
        :param request:
        :param view:
        :return:
        """
        # 1. 对于get，head，option这种请求，直接允许
        if request.method in ['GET', 'HEAD', 'OPTION']:
            return True
        # 2. 是否登录
        if request.user and request.user.is_authenticated:
            return True
        return False


class ProjectPermission(BasePermission):
    """只有项目的leader才可以编辑删除项目，其他用户只读"""

    def has_object_permission(self, request, view, obj):
        # 允许所有GET、HEAD和OPTIONS请求
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        if str(request.user) == 'admin':
            return True
        # 仅允许项目领导人编辑和删除项目
        return obj.leader == str(request.user) and request.method in ["DELETE", "PATCH"]