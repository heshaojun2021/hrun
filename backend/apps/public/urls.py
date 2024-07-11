# -*- coding: utf-8 -*-
# @author: HRUN

from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

router = DefaultRouter()
router.register('wxPush', views.WxPushViewSet)

# 手动注册 YApiViewSet
urlpatterns = [
    path('yapi/', views.YApiViewSet.as_view(), name='yapi'),
    path('ProjectBoard/', views.ProjectBoardView.as_view(), name='ProjectBoard'),
]

# 将自定义路由器中的 URLs 与手动注册的 URL 集成
urlpatterns += router.urls
