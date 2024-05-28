from celery import shared_task

from apitestengine.core.cases import run
from common.mailPush import wxPush

from projects.models import TestEnv, Project
from public.tasks import import_run_yapi
from reports.models import Record, Report
from public.models import WxPush, StatisticalRecord
from .models import TestPlan, TestCase
from .serializers import TestPlanRunSerializer, TestCaseDataRunSerializer


def __get_env_config(env_id, debug=True):
    """获取测试环境的配置"""
    env = TestEnv.objects.get(pk=env_id)
    var = {**env.global_variable, **env.debug_global_variable} if debug else env.global_variable
    # 环境变量
    ENV = {
        **var,  # 因为debug模式下var中有临时的调试变量，解包时不能写到下面，否则会覆盖真正的host和headers
        'host': env.host,
        'headers': env.headers,
    }
    config = {
        'ENV': ENV,
        'DB': env.db,
        'global_func': env.global_func
    }
    return config


def run_case(cases, env_id):
    """运行单条用例"""
    # 环境
    config = __get_env_config(env_id)
    # 执行用例
    res, debug_var = run(case_data=[{"Cases": [cases]}], env_config=config, debug=True)
    # 获取执行的结果
    result = res['results'][0]['cases'][0]
    # 保存一下调试模式下的环境变量
    env = TestEnv.objects.get(pk=env_id)
    env.debug_global_variable = debug_var
    env.save()
    # 返回结果
    return result


def run_scene(pk, env_id):
    """执行测试场景(套件)"""
    # 1. 获取测试环境
    config = __get_env_config(env_id, debug=True)
    # 2. 获取测试用例
    scene = TestCase.objects.get(pk=pk)
    # 3. 根据测试场景对象，组织测试场景的测试数据
    cases = TestCaseDataRunSerializer(scene).data['casestepdata_set']
    # 4. 套件内的用例排序
    cases.sort(key=lambda x: x['sort'])
    # 5. 组装用例数据
    def process_item(item):
        processed_item = {**item['interfaceStep'], **{'children': []}}
        if 'children' in item:
            processed_item['children'] = [process_item(child) for child in item['children']]
        return processed_item

    test_data = {'Cases': [process_item(item) for item in cases], 'name': scene.name}

    # 6. 运行测试用例
    res, debug_var = run(case_data=[test_data], env_config=config, debug=True, thread_count=3)
    # 7. 保存debug模式的环境变量
    env = TestEnv.objects.get(pk=env_id)
    env.debug_global_variable = debug_var
    env.save()
    return res['results'][0]


@shared_task
def run_plan(plan_id, env_id, record_id):
    """执行测试计划"""
    # 获取测试环境,注意现在是正式运行，所以debug要关掉
    config = __get_env_config(env_id, debug=True)
    # 获取执行计划的数据
    plan = TestPlan.objects.get(pk=plan_id)
    task_data = TestPlanRunSerializer(plan).data
    scene_list = []
    for scene in task_data['new_scenes']:
            cases = scene['casestepdata_set']
            # 排序
            cases.sort(key=lambda x: x['sort'])

            def process_item(item):
                processed_item = {**item['interfaceStep'], **{'children': []}}
                if 'children' in item:
                    processed_item['children'] = [process_item(child) for child in item['children']]
                return processed_item
            scene_list.append({'Cases': [process_item(item) for item in cases], 'name': scene['name']})

    # 执行测试任务
    res, env = run(case_data=scene_list, env_config=config, debug=True, thread_count=5)

    # 保存运行结果
    record = Record.objects.get(pk=record_id)
    # 往执行结果中加一些字段
    res['plan'] = plan_id
    res['test_env'] = env_id
    res['tester'] = record.tester
    # 创建报告
    Report.objects.create(info=res, record=record)

    # 更新record中的数据
    record.all = res.get('all', 0)
    record.success = res.get('success', 0)
    record.fail = res.get('fail', 0)
    record.error = res.get('error', 0)
    record.pass_rate = '{:.2f}'.format(100 * res.get('success', 0) / res.get('all', 0)) if res.get('all', 0) else '0'
    record.status = '执行完毕'
    record.save()

    # 获取用例执行总耗时用于报告展示
    all_time = []
    for results in res["results"]:
        for cases in results['cases']:
            run_time_str = cases['run_time']  # 获取时间字符串，如"0.519s"
            run_time_float = float(run_time_str[:-1])  # 将时间字符串转换为浮点数，去掉末尾的"s"
            all_time.append(run_time_float)
            total_run_time = round(sum(all_time), 3)

    # 发送测试报告
    try:
        wx_data = WxPush.objects.get(testPlan=plan_id)
        wx = wxPush(wx_data.webhook, wx_data.user_ids)
        wx.text()
        wx.markdown(project=record.project,
                    url=f'http://139.9.38.166:5002/#/PushEport/{record.id}',
                    env=record.test_env,
                    plan=plan,
                    pass_rate=record.pass_rate,
                    all=res.get('all', 0),
                    success=res.get('success', 0),
                    fail=res.get('fail', 0),
                    error=res.get('error', 0),
                    all_time=total_run_time)

    except WxPush.DoesNotExist:
        return True

    wx_data = WxPush.objects.get(testPlan=plan_id)
    if wx_data is None:
        return True





@shared_task
def run_crontab_plan(plan_id, env_id, tester, project):
    """
    定时执行测试计划
    :param plan_id:
    :param env_id:
    :param tester:
    :return:
    """
    # 1. 创建测试记录
    record = Record.objects.create(**{
        'plan_id': plan_id,
        'test_env_id': env_id,
        'status': '执行中',
        'tester': tester,
        'project_id': project,
        'execute_type': '定时执行'
    })
    project = Project.objects.get(id=project)
    plan = TestPlan.objects.get(pk=plan_id)
    statistical = StatisticalRecord.objects.create(
        name=plan.name,
        type='job',
        status=2,
        project=project,
        performer='job定时执行')
    # 2. 执行测试计划
    run_plan(plan_id, env_id, record.pk)
    StatisticalRecord.objects.filter(pk=statistical.pk).update(status=1)


@shared_task
def run_crontab_yapi(**kwargs):
    project = Project.objects.get(id=int(kwargs['project']))
    statistical = StatisticalRecord.objects.create(
        name='YApi自动同步',
        type='job',
        status=2,
        project=project,
        performer='job定时执行')

    data = {
        'project': int(kwargs['project']),
        'YApiId': int(kwargs['YApiId']),
        'treenode': int(kwargs['treenode']),
        'token': kwargs['token'],
        'url': kwargs['url'],
        'format': "list"
    }
    import_run_yapi(data)
    StatisticalRecord.objects.filter(pk=statistical.pk).update(status=1)
