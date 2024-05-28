from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from public.models import WxPush
from testplans.serializers import TestPlanSerializer



class WxPushSerializer(serializers.ModelSerializer):
    """微信推送序列化器"""
    testPlan = TestPlanSerializer(read_only=True)
    testPlan_id = serializers.IntegerField(required=True, validators=[UniqueValidator(queryset=WxPush.objects.all(), message='此计划已被使用')])

    class Meta:
        model = WxPush
        fields = ['id', 'name', 'webhook', 'user_ids', 'testPlan', 'create_time', 'testPlan', 'project_id', 'testPlan_id']