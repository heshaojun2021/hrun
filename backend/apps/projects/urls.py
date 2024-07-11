# -*- coding: utf-8 -*-
# @author: HRUN

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('projects', views.ProjectViewSet)
router.register('interfaces', views.InterfaceViewSet)
router.register('test_envs', views.TestEnvViewSet)
router.register('treeNode', views.TreeNodeViewSet)
router.register('newinterfaces', views.newInterfaceViewSet)
urlpatterns = router.urls
