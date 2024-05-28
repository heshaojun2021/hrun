from rest_framework.serializers import ModelSerializer, StringRelatedField,DateTimeField

from .models import Record, Report


class RecordSerializer(ModelSerializer):
    env_name = StringRelatedField(source='test_env')
    plan_name = StringRelatedField(source='plan')

    class Meta:
        model = Record
        fields = '__all__'




class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

