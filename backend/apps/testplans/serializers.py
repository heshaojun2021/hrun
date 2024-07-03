from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.validators import UniqueValidator

from projects.serializers import InterfaceSerializer, ProjectSerializer
from reports.serializers import RecordSerializer
from .models import TestStep, TestPlan, TestScene, SceneData, UploadFile, CrontabTask, TestCase, CaseStepData, \
    StepController
from projects.models import newInterface

class TestStepSerializer(serializers.ModelSerializer):
    """
    测试步骤序列化器
    """

    class Meta:
        model = TestStep
        fields = '__all__'


class TestStepRetrieveSerializer(serializers.ModelSerializer):
    """
    测试步骤详情序列化器
    """
    interface = InterfaceSerializer()

    class Meta:
        model = TestStep
        fields = '__all__'
        # depth = 1


class UploadFileSerializer(serializers.ModelSerializer):
    """文件上传序列化器"""

    class Meta:
        model = UploadFile
        fields = '__all__'
        extra_kwargs = {'file': {'write_only': True}, 'info': {'read_only': True}}


class TestSceneSerializer(serializers.ModelSerializer):
    """测试场景序列化器"""
    class Meta:
        model = TestScene
        fields = '__all__'


class NestTestStepSerializer(serializers.ModelSerializer):
    """嵌套测试步骤序列化器"""
    class Meta:
        model = TestStep
        fields = ['id', 'title']


class TestSceneStepSerializer(serializers.ModelSerializer):
    """测试场景步骤序列化器"""
    stepInfo = NestTestStepSerializer(read_only=True, source='step')

    class Meta:
        model = SceneData
        fields = '__all__'


class TestPlanSerializer(serializers.ModelSerializer):
    """测试计划序列化器"""
    class Meta:
        model = TestPlan
        fields = '__all__'


class TestStepRunSerializer(serializers.ModelSerializer):
    """测试步骤序运行序列化器"""
    interface = InterfaceSerializer()

    class Meta:
        model = TestStep
        fields = '__all__'


class TestSceneStepRunSerializer(serializers.ModelSerializer):
    """测试场景步骤运行序列化器"""
    step = TestStepRunSerializer()

    class Meta:
        model = SceneData
        fields = '__all__'


class TestSceneRunSerializer(serializers.ModelSerializer):
    """测试场景运行序列化器"""
    scenedata_set = TestSceneStepRunSerializer(many=True)

    class Meta:
        model = TestScene
        fields = '__all__'



class TestCaseSerializer(serializers.ModelSerializer):
    """测试用例序列化器"""
    project = ProjectSerializer(read_only=True)
    project_id = serializers.CharField(label='项目id', help_text='项目id', write_only=True)

    class Meta:
        model = TestCase
        fields = '__all__'
        extra_kwargs = {
            'name': {
                'required': True,
                'validators': [UniqueValidator(queryset=model.objects.all(), message='此用例名称已存在')]
            }
        }
class NestTestCaseSerializer(serializers.ModelSerializer):
    """嵌套测试步骤序列化器"""
    class Meta:
        model = newInterface
        fields = ['id', 'name', 'url', 'type', 'method', 'host']

class StepControllerSerializer(serializers.ModelSerializer):
    setpId = serializers.CharField(label='步骤id', help_text='步骤id', read_only=True, default=None)
    """步骤控制器序列化器"""
    class Meta:
        model = StepController
        fields = '__all__'
        # fields = ['id', 'name', 'content', 'type', 'desc', 'script', 'creator', 'dlg', 'inputDlg', 'setpId']
        read_only_fields = ['dlg', 'inputDlg']



class TestCaseStepSerializer(serializers.ModelSerializer):
    """测试用例步骤序列化器"""
    children = serializers.SerializerMethodField()
    stepInfo = serializers.SerializerMethodField(method_name='get_step_info')

    def get_step_info(self, obj):
        if obj.interfaceStep:  # 如果存在接口步骤信息
            return NestTestCaseSerializer(obj.interfaceStep, context=self.context).data
        elif obj.controllerStep:  # 如果存在控制器步骤信息
            return StepControllerSerializer(obj.controllerStep, context=self.context).data
        return None

    def get_children(self, obj):
        children_data = []
        if obj.children:
            # 修改查询集以确保子节点按照 sort 字段排序
            children_query = obj.children.order_by('sort')
            # 使用相同的序列化器对子节点进行序列化
            serializer = self.__class__(children_query, many=True, context=self.context)
            children_data = serializer.data
        return children_data

    class Meta:
        model = CaseStepData
        fields = '__all__'

class TestCaseRunSerializer(serializers.ModelSerializer):
    """接口步骤运行序列化器"""
    interface = serializers.SerializerMethodField()
    title = serializers.CharField(source='name')  # 重命名 name 字段为 title

    class Meta:
        model = newInterface
        fields = ('title', 'interface', 'headers', 'type', 'request', 'setup_script', 'teardown_script')

    def get_interface(self, obj):
        return {
            'url': obj.url,
            'name': obj.name,
            'method': obj.method
        }

class TestCaseRunControllerSerializer(serializers.ModelSerializer):
    """步骤控制器序列化器"""
    title = serializers.CharField(source='name')
    class Meta:
        model = StepController
        fields = ['title', 'content', 'type', 'script']


class TestCaseStepRunSerializer(serializers.ModelSerializer):
    """用例步骤与接口嵌套的序列化器"""

    interfaceStep = serializers.SerializerMethodField(method_name='get_interfaceStep')
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        children_data = []
        if obj.children:
            # 修改查询集以确保子节点按照 sort 字段排序
            children_query = obj.children.order_by('sort')
            # 使用相同的序列化器对子节点进行序列化
            serializer = self.__class__(children_query, many=True, context=self.context)
            children_data = serializer.data
        return children_data
    def get_interfaceStep(self, obj):
        if obj.interfaceStep:  # 如果存在接口步骤信息
            serializer = TestCaseRunSerializer(obj.interfaceStep, context=self.context)
            return serializer.data
        elif obj.controllerStep:  # 如果存在控制器步骤信息
            serializer = TestCaseRunControllerSerializer(obj.controllerStep, context=self.context)
            return serializer.data
        return None

    class Meta:
        model = CaseStepData
        fields = '__all__'


class TestCaseDataRunSerializer(serializers.ModelSerializer):
    """测试用例嵌套用例步骤运行序列化器"""
    casestepdata_set = TestCaseStepRunSerializer(many=True)

    def filter_cases_with_status(self, case_data):
        # 如果当前节点的status为False，则直接过滤掉当前节点及其所有子节点
        if not case_data['status']:
            return False

        # 如果有子节点，则递归检查子节点
        if case_data.get('children'):
            # 过滤后的子节点列表
            filtered_children = []
            # 遍历子节点
            for child_case in case_data['children']:
                # 递归检查子节点
                if self.filter_cases_with_status(child_case):
                    # 如果子节点的status为True，则将其加入过滤后的子节点列表
                    filtered_children.append(child_case)

            # 更新当前节点的子节点列表为过滤后的子节点列表
            case_data['children'] = filtered_children

        # 返回当前节点是否保留的状态
        return case_data['status'] or bool(case_data.get('children'))

    def to_representation(self, instance):
        # 调用父类的 to_representation 方法获取 TestCase 的序列化数据
        representation = super().to_representation(instance)

        # 获取用例步骤数据
        cases_data = representation['casestepdata_set']

        # 过滤掉 status 为 False 的数据及其子节点
        filtered_cases_data = [case_data for case_data in cases_data if
                               self.filter_cases_with_status(case_data) and not case_data.get('parent_id')]

        if not filtered_cases_data:
            raise ParseError("没有启用的用例步骤数据")

        representation['casestepdata_set'] = filtered_cases_data
        return representation

    class Meta:
        model = TestCase
        fields = ['id', 'name', 'project', 'casestepdata_set']



class TestPlanRunSerializer(serializers.ModelSerializer):
    scenes = TestSceneRunSerializer(many=True)
    new_scenes = TestCaseDataRunSerializer(many=True)
    class Meta:
        model = TestPlan
        fields = '__all__'


class CrontabTaskSerializer(serializers.ModelSerializer):
    plan_name = serializers.SerializerMethodField()
    env_name = serializers.StringRelatedField(source='env')
    def get_plan_name(self, obj):
        if obj.type == 10:
            return obj.plan.name
        else:
            return 'YApi自动同步'

    class Meta:
        model = CrontabTask
        fields = '__all__'