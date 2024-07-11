# -*- coding: utf-8 -*-
# @author: HRUN

from rest_framework import serializers

from .models import Bug, BugHandle


class BugSerializer(serializers.ModelSerializer):
    """bug序列化器"""

    interface_url = serializers.CharField(source='interface.url', read_only=True)

    class Meta:
        model = Bug
        fields = '__all__'


class BugHandleSerializer(serializers.ModelSerializer):
    """bug跟进记录序列化器"""

    class Meta:
        model = BugHandle
        fields = '__all__'
