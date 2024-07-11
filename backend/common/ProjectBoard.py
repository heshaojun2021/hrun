# -*- coding: utf-8 -*-
# @author: HRUN

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "primaryApp.settings.dev")
import django
django.setup()


from django.utils import timezone
from datetime import timedelta, datetime

from projects.models import newInterface
from projects.models import Project
from testplans.models import TestCase
from testplans.models import TestPlan
from reports.models import Record
from public.models import StatisticalRecord
from users.models import User
import random

class ProjectBoard:
    def __init__(self, project):
        self.project = project

    def __week_statistics(self, model, time_field):
        try:
            today = timezone.now().date()
            this_week_start = today - timedelta(days=today.weekday())
            this_week_end = this_week_start + timedelta(days=7)

            last_week_start = this_week_start - timedelta(weeks=1)
            last_week_end = last_week_start + timedelta(days=7)

            this_week_count = model.objects.filter(project=self.project, **{f"{time_field}__range": [this_week_start, this_week_end]}).count()
            last_week_count = model.objects.filter(project=self.project, **{f"{time_field}__range": [last_week_start, last_week_end]}).count()

        except Exception as e:
            raise Exception('数据库查询时有误: {}'.format(e))
        # 计算新增或减少的用例数量
        case_difference = this_week_count - last_week_count

        # 如果用例数量减少了，则计算减少的百分比；如果用例数量增加了，则计算增加的百分比
        if case_difference < 0:
            try:
                percentage_difference = (abs(case_difference) / last_week_count) * 100 * -1
                return {'changeType': 'lastDecrease', 'percentage':  "{:.2f}%".format(percentage_difference)}
            except ZeroDivisionError:
                percentage_difference = case_difference * 100 * -1
                return {'changeType': 'lastDecrease', 'percentage': "{:.2f}%".format(percentage_difference)}
        elif case_difference > 0:
            try:
                percentage_difference = (case_difference / last_week_count) * 100
                return {'changeType': 'lastIncrease', 'percentage':  "{:.2f}%".format(percentage_difference)}
            except ZeroDivisionError:
                percentage_difference = case_difference * 100
                return {'changeType': 'lastIncrease', 'percentage':  "{:.2f}%".format(percentage_difference)}
        else:
            percentage_difference = 0
            return {'changeType': 'lastIncrease', 'percentage':  "{:.2f}%".format(percentage_difference)}

    def __day_statistics(self, model, time_field, type):
        global this_day_count, yesterday_count, run_service, paused
        try:
            today = timezone.now().date()
            this_day_start = today
            this_day_end = this_day_start + timedelta(days=1)

            yesterday_start = today - timedelta(days=1)
            yesterday_end = yesterday_start + timedelta(days=1)

            if type == 'interface':
                this_day_count = model.objects.filter(project=self.project,
                                                      **{f"{time_field}__range": [this_day_start, this_day_end]}).count()
                yesterday_count = model.objects.filter(project=self.project,
                                                       **{f"{time_field}__range": [yesterday_start, yesterday_end]}).count()
            elif type == 'case':
                this_day_count = model.objects.filter(project=self.project,
                                                      type='case',
                                                      **{f"{time_field}__range": [this_day_start, this_day_end]}).count()
                yesterday_count = model.objects.filter(project=self.project,
                                                       type='case',
                                                       **{f"{time_field}__range": [yesterday_start, yesterday_end]}).count()
            elif type == 'job':
                this_day_count = model.objects.filter(project=self.project,
                                                      type='job',
                                                      **{f"{time_field}__range": [this_day_start, this_day_end]}).count()
                run_service = model.objects.filter(project=self.project,
                                                      type='job',
                                                      status=2,
                                                      **{f"{time_field}__range": [this_day_start, this_day_end]}).count() or 0
                paused = model.objects.filter(project=self.project,
                                                      type='job',
                                                      status=3,
                                                      **{f"{time_field}__range": [this_day_start, this_day_end]}).count() or 0

            else:
                raise Exception('type参数错误')
        except Exception as e:
            raise Exception('数据库查询时有误: {}'.format(e))

        if type == 'case' or type == 'interface':
            # 计算新增或减少的用例数量
            case_difference = this_day_count - yesterday_count

            # 如果用例数量减少了，则计算减少的百分比；如果用例数量增加了，则计算增加的百分比
            if case_difference < 0:
                try:
                    percentage_difference = (abs(case_difference) / yesterday_count) * 100 * -1
                    return {'count': this_day_count, 'changeType': 'yastdayDecrease', 'percentage':  "{:.2f}%".format(percentage_difference)}
                except ZeroDivisionError:
                    percentage_difference = case_difference * 100 * -1
                    return {'count': this_day_count, 'changeType': 'yastdayDecrease','percentage': "{:.2f}%".format(percentage_difference)}

            elif case_difference > 0:
                try:
                    percentage_difference = (case_difference / yesterday_count) * 100
                    return {'count': this_day_count, 'changeType': 'yastdayIncrease', 'percentage':  "{:.2f}%".format(percentage_difference)}
                except ZeroDivisionError:
                    percentage_difference = case_difference * 100
                    return {'count': this_day_count, 'changeType': 'yastdayIncrease','percentage': "{:.2f}%".format(percentage_difference)}

            else:
                percentage_difference = 0
                return {'count': this_day_count, 'changeType': 'yastdayIncrease', 'percentage': "{:.2f}%".format(percentage_difference)}


        return {'count': this_day_count, 'changeType': 'job', 'run_service': run_service, 'paused': paused}

    def __get_project_info(self):

        return [
            {'name': '接口数量', 'count': self.project.new_interface.count(), **self.__week_statistics(newInterface, 'create_time')},
            {'name': '用例数量', 'count': self.project.testcase.count(), **self.__week_statistics(TestCase, 'create_time')},
            {'name': '计划数量', 'count': self.project.test_plans.count(), **self.__week_statistics(TestPlan, 'create_time')},
            {'name': '报告数量', 'count': self.project.test_record.count(), **self.__week_statistics(Record, 'create_time')},
            {'name': '当天登录用户次数', 'count': random.randint(10, 200), 'percentage': '12.30%','changeType': 'lastIncrease'},
            {'name': '当天创建接口数量', **self.__day_statistics(newInterface, 'create_time', 'interface')},
            {'name': '当天运行用例次数', **self.__day_statistics(StatisticalRecord, 'create_time', 'case')},
            {'name': '当天Job运行次数', **self.__day_statistics(StatisticalRecord, 'create_time', 'job')},
        ]

    def __get_project_bug(self):
        return [
            {'name': '待处理', 'value': self.project.bug_set.filter(status='待处理').count()},
            {'name': '处理中', 'value': self.project.bug_set.filter(status='处理中').count()},
            {'name': '已关闭', 'value': self.project.bug_set.filter(status='已关闭').count()},
            {'name': '处理完成', 'value': self.project.bug_set.filter(status='处理完成').count()},
            {'name': '无需处理', 'value': self.project.bug_set.filter(status='无需处理').count()}
        ]

    def __get_project_case(self, starttime=None, endtime=None):
        user_stats = []
        user_identifiers = User.objects.values_list('username', flat=True).distinct()

        for user_identifier in user_identifiers:
            query_params = {
                'performer': user_identifier,
                'type': 'api',
                'project': self.project,
            }
            query_param = {
                'creator': user_identifier,
                'project': self.project,
            }
            if starttime and endtime:
                query_params['create_time__range'] = [starttime, endtime]
                query_param['create_time__range'] = [starttime, endtime]
            # 统计接口调试数量
            interface_debug_count = StatisticalRecord.objects.filter(**query_params).count()

            # 统计接口新增数量
            interface_new_count = newInterface.objects.filter(**query_param).count()

            # 统计用例新增数量
            testcase_new_count = TestCase.objects.filter(**query_param).count()

            if interface_debug_count != 0 or interface_new_count != 0 or testcase_new_count != 0:
                # 将统计结果添加到列表中
                user_stats.append({
                    'user': user_identifier,
                    'interface_debug_count': interface_debug_count,
                    'interface_new_count': interface_new_count,
                    'testcase_new_count': testcase_new_count
                })
        if user_stats:
            return user_stats
        return [{
                    'user': 'admin',
                    'interface_debug_count': 0,
                    'interface_new_count': 0,
                    'testcase_new_count': 0
                }]

    def __get_project_report(self):
        today = timezone.now().date()
        three_days_ago = today - timedelta(days=2)
        three_days_range = [three_days_ago, today + timedelta(days=1)]
        data = list(Record.objects.filter(project=self.project,
                                                 create_time__range=three_days_range).values('pass_rate', 'create_time', 'plan_id__name'))
        for st in data:
            st['create_time'] = st['create_time'].strftime('%Y-%m-%d %H:%M:%S')
        if data:
            return data
        return [{'create_time': timezone.now().date(), 'pass_rate': 0, 'plan_id__name': '无'}]
    def __get_project_click(self):
        """暂未开发，目前是假数据"""
        today = datetime.now().date()
        seven_days_range = [today - timedelta(days=i) for i in range(6, -1, -1)]

        random_numbers = [random.randint(200, 1500) for _ in range(7)]

        click_data = [{'date': day.strftime('%m-%d'), 'clicks': clicks} for day, clicks in
                      zip(seven_days_range, random_numbers)]

        return click_data


    def __get_mock_log(self):
        """暂未开发，目前是假数据"""
        return [{
                  "create_time": "2024-02-18T10:30:00",
                  "method": "GET",
                  "url": "/api/v1/user/login",
                  "ip": "192.168.1.1",
                  "status_code": "200",
                  "time_consuming": "0.1s",
    },
                {
                  "create_time": "2024-02-18T10:30:00",
                  "method": "GET",
                  "url": "/api/v1/user/login",
                  "ip": "192.168.1.1",
                  "status_code": "200",
                  "time_consuming": "0.1s",
                },
                {
                  "create_time": "2024-02-18T10:30:00",
                  "method": "POST",
                  "url": "/api/v1/user/login",
                  "ip": "192.168.1.101",
                  "status_code": "400",
                  "time_consuming": "0.1s",
                },
                {
                  "create_time": "2024-02-18T10:30:00",
                  "method": "POST",
                  "url": "/api/v1/user/login",
                  "ip": "192.168.1.1",
                  "status_code": "200",
                  "time_consuming": "0.5s",
                },
                {
                  "create_time": "2024-02-18T10:30:00",
                  "method": "POST",
                  "url": "/api/v1/user/login",
                  "ip": "192.168.1.1",
                  "status_code": "200",
                  "time_consuming": "0.5s",
                },
                {
                  "create_time": "2024-02-18T10:30:00",
                  "method": "POST",
                  "url": "/api/v1/user/login",
                  "ip": "192.168.1.1",
                  "status_code": "200",
                  "time_consuming": "0.5s",
                },
                {
                  "create_time": "2024-02-18T10:30:00",
                  "method": "POST",
                  "url": "/api/v1/user/login",
                  "ip": "192.168.1.1",
                  "status_code": "200",
                  "time_consuming": "0.5s",
                }
            ]

    def get_project_data_summary(self,starttime=None, endtime=None):
        summary_result = {}
        try:
            project_info = self.__get_project_info()
            project_bug = self.__get_project_bug()
            project_case = self.__get_project_case(starttime, endtime)
            project_report = self.__get_project_report()
            track_button_click = self.__get_project_click()
            mock_log = self.__get_mock_log()

            summaryResult = {
                "project_info": project_info,
                "project_bug": project_bug,
                "project_case": project_case,
                "project_report": project_report,
                "track_button_click": track_button_click,
                "mock_log": mock_log
            }
        except Exception as e:
            error_msg = f"获取项目数据时失败: {e}"
            summary_result["error"] = error_msg
            return summary_result

        return summaryResult



if __name__=="__main__":
    import json
    project = Project.objects.get(id=4)

    data = ProjectBoard(project).get_project_data_summary()
    print(json.dumps(data))
