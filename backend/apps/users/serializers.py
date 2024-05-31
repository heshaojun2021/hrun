from django.contrib.auth.hashers import make_password
from requests import Response
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from projects.models import Project
from projects.serializers import ProjectSerializer
from .models import User


# 自定义token序列化器
class MyTokenSerializer(TokenObtainPairSerializer):

    # 重写  validate 修改access为token
    # 加一些字段
    def validate(self, attrs):
        data = super().validate(attrs)
        # 修改access 为token
        data['token'] = data.pop('access')
        # 增加一些字段
        data['username'] = self.user.username
        data['id'] = self.user.id
        data['msg'] = '登录成功'
        return data


# 自定义token刷新序列化器
class MyRefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # 修改access 为token
        data['token'] = data.pop('access')
        return data


# 注册用户序列化器
class UserRegisterSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(many=True, read_only=True)
    project_id =serializers.CharField(label='项目id', help_text='项目id', write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password',  'email', 'mobile', 'date_joined', 'project', 'project_id', 'weChat_name']
        # 修改模型字段的参数
        extra_kwargs = {
            'username': {
                'min_length': 3,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许3-20个字符的用户名',
                    'max_length': '仅允许3-20个字符的用户名',
                }
            },
            'password': {
                'min_length': 6,
                'max_length': 20,
                'write_only': True,
                'error_messages': {
                    'min_length': '仅允许6-20个字符的密码',
                    'max_length': '仅允许6-20个字符的密码',
                }
            },
            "date_joined": {
                'read_only': True,
            },
        }

    def create(self, validated_data):
        project_id = validated_data['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': '项目不存在'}, status=status.HTTP_400_BAD_REQUEST)
        validated_data.pop('project_id')
        user = User.objects.create_user(**validated_data)
        # 将项目与用户关联起来
        user.project.add(project)

        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data['password']
            # 在这里对密码进行特殊处理加密
            validated_data['password'] = make_password(password)

        return super().update(instance, validated_data)


