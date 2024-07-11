# -*- coding: utf-8 -*-
# @author: HRUN

"""primaryApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAuthenticated

from drf_yasg.views import get_schema_view as yasg_get_schema_view
from drf_yasg import openapi

schema_view = yasg_get_schema_view(
    openapi.Info(
        title='你的项目名称',
        default_version="1.0.0",
        description='项目描述',
        terms_of_service='http://127.0.0.1:8000/',
        contact=openapi.Contact(email='xinlan@qq.com'),
        license=openapi.License(name='MIT')
    ),
    public=True,
    permission_classes=(IsAuthenticated, ), #权限
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('projects.urls')),
    path('', include('testplans.urls')),
    path('', include('reports.urls')),
    path('', include('bugs.urls')),
    path('', include('public.urls')),
    # 给drf的可视化api增加登录功能
    path('restframework/', include('rest_framework.urls')),
    path('openapi/', get_schema_view(
        title='你的项目的名字',
        description='项目的描述',
        version="1.0.0"
    ), name='openapi-schema'),
    path('openapi-swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html', extra_context={'schema_url': 'openapi-schema'}

    ), name='openapi-swagger-ui'),
    path('docs/', include_docs_urls(title="你的项目名称", public=False, description='aaa')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(), name='swagger-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger'), name='swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc'), name='redoc-ui')

]
