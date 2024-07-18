# -*- coding: utf-8 -*-
# @author: HRUN


from rest_framework import serializers

from .models import Project, TestEnv, TreeNode, newInterface
from rest_framework.validators import UniqueValidator

class ProjectSerializer(serializers.ModelSerializer):

    """
    项目序列化器
    """
    class Meta:
        model = Project
        fields = ['id', 'create_time', 'name', 'leader', 'leader_id', 'desc']





class TestEnvSerializer(serializers.ModelSerializer):
    """
    测试环境序列化器
    """
    class Meta:
        model = TestEnv
        fields = '__all__'


class TreeNodeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = TreeNode
        fields = '__all__'

    def get_children(self, obj):
        children = obj.children.exclude(parent_id__isnull=True)
        serializer = self.__class__(children, many=True)
        return serializer.data


class newInterfaceSerializer(serializers.ModelSerializer):
    """
    接口序列化器
    """
    class Meta:
        model = newInterface
        fields = '__all__'