# -*- coding: utf-8 -*-
# @author: HRUN


from rest_framework import serializers

from .models import Project, TestEnv, TreeNode, newInterface, \
    Mock, MockDetail, MockDetailForm, MockLog



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




class MockDetailFormSerializer(serializers.ModelSerializer):
    """
    mock接口详情表单序列化器
    """
    class Meta:
        model = MockDetailForm
        fields = '__all__'

class MockDetailSerializer(serializers.ModelSerializer):
    """
    mock接口详情序列化器
    """
    detailForm = MockDetailFormSerializer(many=True, required=False, allow_null=True)
    class Meta:
        model = MockDetail
        fields = '__all__'

class MockSerializer(serializers.ModelSerializer):
    """
    mock接口序列化器
    """
    MockDetail = MockDetailSerializer(many=True, required=False, allow_null=True)
    class Meta:
        model = Mock
        fields = '__all__'


class MockLogSerializer(serializers.ModelSerializer):
    """
    mock接口日志序列化器
    """
    class Meta:
        model = MockLog
        fields = '__all__'