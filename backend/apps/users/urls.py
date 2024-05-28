from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', views.RefreshTokenView.as_view(), name='token-refresh'),
]
urlpatterns += router.urls