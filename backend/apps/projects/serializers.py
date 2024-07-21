# -*- coding: utf-8 -*-
# @author: HRUN


from rest_framework import serializers

from .models import Project, TestEnv, TreeNode, newInterface, \
    Mock, MockDetail, MockLog



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





class MockDetailSerializer(serializers.ModelSerializer):
    """
    mock接口详情序列化器
    """
    def to_representation(self, instance):
        # 获取序列化后的原始数据
        data = super().to_representation(instance)

        # 创建一个映射表，用于将比较类型转换为中文
        comparison_mapping = {
            'equal': "等于",
            'notEqual': "不等于",
            'greaterThan': "大于",
            'lessThan': "小于",
            'greaterThanOrEqual': "大于等于",
            'lessThanOrEqual': "小于等于",
            'contains': "包含",
            'notContains': "不包含",
            'empty': "为空",
            'notEmpty': "不为空",
        }
        remark =''
        # 遍历每个条件表单条目，添加 remark 字段
        for condition in data.get('conditionForm', []):
            try:
                location = condition["location"]
                paramName = condition["paramName"]
                comparison = condition["comparison"]
                value = condition["value"]

                chinese_comparison = comparison_mapping[comparison]

                # 构建 remark
                remark_value = f"{location} 参数 {paramName} {chinese_comparison} {value}"

                # 将 remark 添加到当前 condition 中
                condition['remark'] = remark_value
                remark += remark_value + "<br>"
            except KeyError as e:
                print(f"缺少键错误: {e}")
        data['remark'] = remark

        return data
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