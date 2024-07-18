# -*- coding: utf-8 -*-
# @author: HRUN

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('upload', views.UploadFileViewSet)
router.register('test_plans', views.TestPlanViewSet)
router.register('crontab_tasks', views.CrontabTaskViewSet)
router.register('TestCase', views.TestCaseViewSet)
router.register('TestCase_Setp', views.TestCaseStepViewSet)
router.register('StepControll', views.StepControllerViewSet)
urlpatterns = router.urls
