from rest_framework.routers import DefaultRouter

from .views import BugViewSet, BugHandleViewSet
route = DefaultRouter()
route.register('bugs', BugViewSet)
route.register('blogs', BugHandleViewSet)

urlpatterns = route.urls

