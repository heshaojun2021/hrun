# -*- coding: utf-8 -*-
# @author: HRUN

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('projects', views.ProjectViewSet)
router.register('test_envs', views.TestEnvViewSet)
router.register('treeNode', views.TreeNodeViewSet)
router.register('newinterfaces', views.newInterfaceViewSet)
router.register('mock', views.mockViewSet)
router.register('mock_detail', views.mockDetailViewSet)
router.register('mock_log', views.mockLogViewSet)
urlpatterns = router.urls
