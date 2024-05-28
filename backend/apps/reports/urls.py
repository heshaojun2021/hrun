from rest_framework.routers import DefaultRouter

from .views import RecordViewSet
route = DefaultRouter()
route.register('records', RecordViewSet)

urlpatterns = route.urls

