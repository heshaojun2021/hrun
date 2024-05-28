from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('test_steps', views.TestStepViewSet)
router.register('upload', views.UploadFileViewSet)
router.register('test_scenes', views.TestSceneViewSet)
router.register('test_scene_steps', views.TestSceneStepViewSet)
router.register('test_plans', views.TestPlanViewSet)
router.register('crontab_tasks', views.CrontabTaskViewSet)
router.register('TestCase', views.TestCaseViewSet)
router.register('TestCase_Setp', views.TestCaseStepViewSet)
router.register('StepControll', views.StepControllerViewSet)
urlpatterns = router.urls
