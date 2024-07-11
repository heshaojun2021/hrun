# -*- coding: utf-8 -*-
# @author: HRUN

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Bug, BugHandle
from .serializers import BugSerializer, BugHandleSerializer


class BugViewSet(ModelViewSet):
    queryset = Bug.objects.all().order_by('-create_time')
    serializer_class = BugSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'interface']
    # 复写perform_create perform_update，在创建bug和更新bug的时候
    # 添加操作记录
    def perform_create(self, serializer):
        #获取当前登录人的name保存到数据库
        user = self.request.user.username
        bug = serializer.save(user=user)
        # 创建处理记录
        status = f'由{user}创建,状态为【{bug.status}】'
        BugHandle.objects.create(
            bug=bug,
            handle=status,
            update_user=self.request.user.username,
        )

    # 更新操作
    def perform_update(self, serializer):
        super().perform_update(serializer)
        bug = serializer.save()
        user = self.request.user.username
        # 创建处理记录
        status = f'由{user}更新,状态为【{bug.status}】'
        BugHandle.objects.create(
            bug=bug,
            handle=status,
            update_user=user,
            remark=bug.remark
        )


class BugHandleViewSet(ReadOnlyModelViewSet):
    """
    retrieve:
    bug日志详情（这里描述retrieve接口）
    list:
    bug日志列表
    """
    queryset = BugHandle.objects.all().order_by('-create_time')
    serializer_class = BugHandleSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ('bug',)
