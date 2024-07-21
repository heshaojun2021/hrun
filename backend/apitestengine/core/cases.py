# -*- coding: utf-8 -*-
# @author: HRUN
import time
import json
import os
import re
import unittest
import threading
from collections import OrderedDict
from numbers import Number
import importlib
import requests
from requests_toolbelt import MultipartEncoder
from functools import wraps
from jsonpath import jsonpath
from apitestengine.core.DBClient import DBClient
from apitestengine.core.runner import TestRunner


try:
    global_func = importlib.import_module('global_func')
except ModuleNotFoundError:
    from apitestengine.core import tools as global_func




class BaseEnv(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        super().__setitem__(key, value)

    def __getattr__(self, item):
        return super().__getitem__(item)


ENV = BaseEnv()
db = DBClient()
DEBUG = True
session = requests.Session()




class GenerateCase:
    """解析数据创建测试用例"""
    def data_to_suite(self, datas):
        """
        根据用例数据生成测试套件
        :param datas:
        :return:
        """
        suite = unittest.TestSuite()
        load = unittest.TestLoader()
        for item in datas:
            cls = self.create_test_class(item)
            suite.addTest(load.loadTestsFromTestCase(cls))
        return suite

    def create_test_class(self, item):
        """创建测试类"""
        cls_name = item.get('name') or 'Demo'
        cases = item.get('Cases')
        # 创建测试类
        cls = type(cls_name, (BaseTest,), {})

        # 定义处理方法字典
        type_handlers = {
            'api': 'api_perform',
            'if': 'if_perform',
            'for': 'loop_perform',
            'script': 'script_perform',
            'time': 'time_perform',
            'sql': 'sql_perform',
        }

        # 遍历数据生成,动态添加测试方法
        for index, case_ in enumerate(cases):
            test_name = self.create_test_name(index, len(cases))
            step_type = case_.get('type')
            if step_type in type_handlers:
                handler = getattr(cls, type_handlers[step_type])
                new_test_func = self.create_test_func(handler, case_)
                new_test_func.__doc__ = f"{case_.get('title')}_{step_type}" or new_test_func.__doc__
                setattr(cls, test_name, new_test_func)
            else:
                raise Exception('不支持的用例类型')

        return cls

    def create_test_func(self, func, case_):
        """创建测试方法"""
        @wraps(func)
        def wrapper(self):
            func(self, case_)
        return wrapper

    def create_test_name(self, index, length):
        """生成测试方法名"""
        n = (len(str(length)) // len(str(index))) - 1
        test_name = 'test_{}'.format("0" * n + str(index + 1))
        return test_name


class CaseRunLog:
    def save_log(self, message, level):
        if not hasattr(self, 'log_data'):
            setattr(self, 'log_data', [])
        if level in ['EXCEPT']:
            info = message
        else:
            info = "【{}】  |   {}".format(level, message)
        getattr(self, 'log_data').append((level, info))
        print(info)

    def print(self, *args):
        args = [str(i) for i in args]
        message = ' '.join(args)
        getattr(self, 'log_data').append(('DEBUG', message))

    def debug_log(self, *args):
        if DEBUG:
            message = ''.join(args)
            self.save_log(message, 'DEBUG')

    def info_log(self, *args):
        message = ''.join(args)
        self.save_log(message, 'INFO')

    def warning_log(self, *args):
        message = ''.join(args)
        self.save_log(message, 'WARNING')

    def error_log(self, *args):
        message = ''.join(str(args))
        self.save_log(message, 'ERROR')

    def exception_log(self, *args):
        message = ''.join(args)
        self.save_log(message, 'EXCEPT')

    def critical_log(self, *args):
        message = ''.join(args)
        self.save_log(message, 'CRITICAL')


class BaseTest(unittest.TestCase, CaseRunLog):

    # 定义处理方法字典
    type_handlers = {
        'api': 'api_perform',
        'if': 'if_perform',
        'for': 'loop_perform',
        'script': 'script_perform',
        'time': 'time_perform',
        'sql': 'sql_perform',
    }
    @classmethod
    def setUpClass(cls) -> None:
        cls.env = BaseEnv()
        if DEBUG:
            cls.session = session
        else:
            cls.session = requests.Session()
    # ------------------------------- api接口步骤处理逻辑 ---------------------------------------
    def api_perform(self, data):
        """单条用例的主函数"""
        self.info_log('▶️开始单条用例执行：{}'.format(data.get('name', '')))
        self.__run_log()
        # 执行前置脚本
        self.__run_setup_script(data)
        # 发送请求
        response = self.__send_request(data)
        # 执行后置脚本
        self.__run_teardown_script(response)

    def __run_log(self):
        """输出当前环境变量数据的日志"""
        self.debug_log("临时变量：\n{}".format(self.env))
        self.debug_log("全局变量：\n{}".format(ENV))

    def __request_log(self):
        """请求信息日志输出"""
        self.debug_log("请求头：\n{}".format(self.requests_header))
        self.debug_log("请求体：\n{}".format(self.requests_body))
        self.info_log('请求响应状态码:{}'.format(self.status_cede))
        self.debug_log("响应头：\n{}".format(self.response_header))
        self.debug_log("响应体：\n{}".format(self.response_body))
    def __send_request(self, data):
        """发送请求"""
        request_info = self.__handler_request_data(data)
        self.info_log('发送 {} 请求 : 请求地址：{}'.format(request_info['method'].upper(), request_info['url']))
        try:
            response = session.request(**request_info)
        except Exception as e:
            raise ValueError('请求发送失败，错误信息如下：{}'.format(e))
        self.url = response.request.url
        self.method = response.request.method
        self.status_cede = response.status_code
        self.response_header = dict(response.headers)
        self.requests_header = dict(response.request.headers)
        try:
            response_body = response.json()
            self.response_body = json.dumps(response_body, ensure_ascii=False, indent=2)
        except:
            body = response.content
            self.response_body = body.decode('utf-8') if body else ''
        try:
            request_body = json.loads(response.request.body.decode('utf-8'))
            self.requests_body = json.dumps(request_body, ensure_ascii=False, indent=2)
        except:
            body = str(response.request.body)
            self.requests_body = body or ''
        self.__request_log()
        return response

    def __handler_request_data(self, data):
        """处理请求数据"""
        # 获取请求头
        if ENV.get('headers'):
            data['headers'] = {**ENV.get('headers'), **data.get('headers')}
        # 替换用例数据中的变量
        for k, v in list(data.items()):
            if k in ['interface', "headers", 'request', 'file']:
                # 替换变量
                v = self.__parser_variable(v)
                data[k] = v
        # files字段文件上传处理的处理
        files = data.get('file')
        if files:
            if isinstance(files, dict):
                file_data = files.items()
            else:
                file_data = files
            field = []
            for name, file_info in file_data:
                # 判断是否时文件上传(获取文件类型和文件名)
                if len(file_info) == 3 and os.path.isfile(file_info[1]):
                    field.append([name, (file_info[0], open(file_info[1], 'rb'), file_info[2])])
                else:
                    field.append([name, file_info])
            form_data = MultipartEncoder(fields=field)
            data['headers']["Content-Type"] = form_data.content_type
            data['request']['data'] = form_data
            data['files'] = None
        else:
            pass
        #     if data['headers'].get("Content-Type"):
        #         del data['headers']["Content-Type"]

        # 组织requests 发送请求所需要的参数格式
        request_params = {}
        # requests请求所需的所有字段
        params_fields = ['url', 'method', 'params', 'data', 'json', 'files', 'headers', 'cookies', 'auth', 'timeout',
                         'allow_redirects', 'proxies', 'hooks', 'stream', 'verify', 'cert']
        for k, v in data['request'].items():
            if k in params_fields:
                request_params[k] = v
        # 请求地址(判断接口地址是不是http开头的，不是则再前面加上Env中的host)
        url = data.get('interface').get('url')
        if url.startswith("http://") or url.startswith("https://"):
            request_params['url'] = url
        else:
            if data.get('interface').get('host') != {}:
                try:
                    request_params['url'] = data.get('interface').get('host',{}).get('host') + url
                except TypeError:
                    request_params['url'] = ENV.get('host') + url
            else:
                request_params['url'] = ENV.get('host') + url
        # 请求方法
        request_params['method'] = data.get('interface').get('method')
        # 请求头
        request_params['headers'] = data['headers']
        return request_params

    def __run_script(test, data):
        print = test.print
        env = test.env
        setup_script = data.get('setup_script')
        if setup_script:
            try:
                exec(setup_script)
            except Exception as e:
                test.error_log('前置脚本执行错误:\n{}'.format(e))
                delattr(test, '_hook_gen')
                raise
        response = yield
        teardown_script = data.get('teardown_script')
        if teardown_script:
            try:
                exec(teardown_script)
            except AssertionError as e:
                test.warning_log('断言失败:\n{}'.format(e))
                raise e
            except Exception as e:
                test.error_log('后置脚本执行错误:\n{}'.format(e))
                raise
        yield

    def __run_teardown_script(self, response):
        """执行后置脚本"""
        self.info_log('执行后置脚本')
        self._hook_gen.send(response)
        delattr(self, '_hook_gen')

    def __run_setup_script(self, data):
        """执行前置脚本"""
        self.info_log('执行前置脚本')
        self._hook_gen = self.__run_script(data)
        next(self._hook_gen)

    # ------------------------------- script步骤处理逻辑 ---------------------------------------
    def script_perform(self, data):
        self.__run_custom_script(data)
    def __run_custom_script(self, data):
        """执行自定义脚本"""
        if data.get('script'):
            exec(data.get('script', b''), global_func.__dict__)

    # ------------------------------- sql控制器步骤处理逻辑 ---------------------------------
    def sql_perform(self, data):
        # todo: 待完成
        pass


    # ------------------------------- time时间控制器步骤处理逻辑 ---------------------------------
    def time_perform(self, data):
        self.__time_gather(data.get('content', ''))

    def __time_gather(self, data):
        self.info_log('⏲ 等待时间为{}秒'.format(data.get('time', '1')))
        time.sleep(int(data.get('time', 1)))

    def timer_decorator(delay):
        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):
                # 创建定时器
                timer = threading.Timer(delay, func, args=args, kwargs=kwargs)
                # 启动定时器
                timer.start()
            return inner
        return wrapper

    # ------------------------------- 循环步骤处理逻辑 ---------------------------------------
    def loop_perform(self, data):
        """循环执行
        - data: 存储传入的初始化数据。
            - select: 用于存储步骤控制器选择的选项，默认为空字符串。
            - cycleIndex: 循环次数，默认为0。
            - cycleInterval: 循环间隔单位为S，默认为0。
            - variable: 要遍历的变量，默认为空字符串。
            - variableName: 要使用的变量名，默认为空字符串。
            - children: 子节点数据
        """
        if data.get('content') is None:
            return
        if data['content'].get('select') == 'count':
            self.__loop_count(data)
        elif data['content'].get('select') == 'for':
            self.__loop_for(data)

        elif data['content'].get('select') == 'while':
            # self.__loop_while(data)
            # todo: 待完成
            pass
        else:
            raise ValueError('循环类型错误')

    def __loop_count(self, data):
        """循环次数"""
        datas = data.get('content')
        for index, case_ in enumerate(data.get('children')):
            self.info_log("🔄次数循环---> 开始")
            cycle_index = datas.get('cycleIndex', None) or 0
            for i in range(min(int(cycle_index), 1000)):
                try:
                    time.sleep(int(datas.get('cycleInterval', None) or 0))
                    self.info_log(f"次数循环---> 第{i + 1}次，执行间隔时间为 {datas.get('cycleInterval',0)}S")
                    # 递归处理子节点
                    self.handle_step(case_)
                except Exception as err:
                    self.error_log(err)
                    continue
            self.info_log("🔄次数循环---> 结束")
    def __loop_for(self, data):
        """
        执行for循环操作。
        对给定的数据进行for循环遍历，如果遍历对象是可迭代的，则对每个元素执行指定的操作。
        :param data: 包含循环所需数据的字典，应包含'content', 'variable', 'children'等键。
        """
        self.info_log("🔄for循环---> 开始")
        datas = data.get('content')
        variableName = datas.get('variableName')
        variable = self.__parser_variable(datas.get('variable'))
        # 遍历子项，并对每个子项执行操作
        for index, case_ in enumerate(data.get('children')):
            loop_count = 0
            if self.__is_iterable(variable):
                # 对变量中的每个元素执行循环
                for item in variable:
                    try:
                        # 根据设定的间隔时间暂停执行
                        time.sleep(int(datas.get('cycleInterval', 0)))
                        loop_count += 1  # 记录当前循环次数
                        self.info_log(f"for循环---> 第{loop_count}次，执行间隔时间为 {datas.get('cycleInterval',0)}S")
                        # 保存当前迭代变量的值
                        self.save_env_variable(variableName, item)
                        # 执行步骤
                        self.handle_step(case_)
                    except Exception as err:
                        # 记录错误并继续下一次循环
                        self.error_log(err)
                        continue
                self.info_log("🔄for循环---> 结束")


    def __loop_while(self, data):
        """循环while"""
        pass

    def __is_iterable(obj,data):
        try:
            iter(data)
            return True
        except TypeError as i:
            raise TypeError(i, "该结果类型不可迭代")
    # ------------------------------- 判断控制器步骤处理逻辑 -----------------------------------
    def if_perform(self, data):
        """
        属性:
        - data: 存储传入的初始数据。
            - variable: 要判断的变量，默认为空字符串。
            - JudgmentMode: 用于存储判断模式，默认为空字符串。
            - value: 用于存储某个值，默认为空字符串。
            - children: 子节点数据
        """
        self.__manage_data(data)

    def __manage_data(self, data):
        self.__judgment_mode(data)

    def __judgment_mode(self, data):
        mode = data['content'].get('JudgmentMode', '')
        content = data.get('content')
        mode_map = {
            'equal': ("等于", self.__equal),
            'notEqual': ("不等于", self.__not_equal),
            'greaterThan': ("大于", self.__greater_than),
            'lessThan': ("小于", self.__less_than),
            'greaterThanOrEqual': ("大于等于", self.__greater_than_or_equal),
            'lessThanOrEqual': ("小于等于", self.__less_than_or_equal),
            'contains': ("包含", self.__contains),
            'notContains': ("不包含", self.__not_contains),
            'empty': ("为空", self.__empty),
            'notEmpty': ("不为空", self.__not_empty)
        }

        if mode in mode_map:
            log_info, handler = mode_map[mode]
            variable = str(self.__parser_variable(content.get('variable')))
            if log_info:
                self.info_log(f"🔀 判断控制器---> 【条件：{log_info}】")
            if handler:
                handler(data, variable, content.get('value', ''))
        else:
            raise AssertionError(self.warning_log('判断条件为空,执行失败'))

    def __equal(self, data, variable, value):
        log_flag = False
        for index, case_ in enumerate(data.get('children')):
            # 进行相等判断
            if variable == value:
                if not log_flag:
                    log_flag = True
                    self.debug_log('✅ 要判断的值{}，要对比的值{}，条件成立，执行相关逻辑'.format(variable, value))
                self.handle_step(case_)
            else:
                raise AssertionError(self.warning_log('❌ 要判断的值{}，要对比的值{}，条件不成立，不执行相关逻辑'.format(variable, value)))

    def __not_equal(self, data, variable, value):
        log_flag = False
        for index, case_ in enumerate(data.get('children')):
            # 进行不相等判断
            if variable != value:
                # 处理逻辑
                if not log_flag:
                    log_flag = True
                    self.debug_log('✅ 要判断的值{}，要对比的值{}，条件成立，执行相关逻辑'.format(variable, value))
                self.handle_step(case_)
            else:
                raise AssertionError(self.warning_log('❌ 要判断的值{}，要对比的值{}，条件不成立，不执行相关逻辑'.format(variable, value)))

    def __greater_than(self, data, variable, value):
        log_flag = False
        for index, case_ in enumerate(data.get('children')):
            # 进行大于判断
            if variable > value:
                # 处理逻辑
                if not log_flag:
                    log_flag = True
                    self.debug_log('✅ 要判断的值{}，要对比的值{}，条件成立，执行相关逻辑'.format(variable, value))
                self.handle_step(case_)
            else:
                raise AssertionError(self.warning_log('❌ 要判断的值{}，要对比的值{}，条件不成立，不执行相关逻辑'.format(variable, value)))

    def __less_than(self, data, variable, value):
        log_flag = False
        for index, case_ in enumerate(data.get('children')):
            # 进行小于判断
            if variable < value:
                # 处理逻辑
                if not log_flag:
                    log_flag = True
                    self.debug_log('✅ 要判断的值{}，要对比的值{}，条件成立，执行相关逻辑'.format(variable, value))
                self.handle_step(case_)
            else:
                raise AssertionError(self.warning_log('❌ 要判断的值{}，要对比的值{}，条件不成立，不执行相关逻辑'.format(variable, value)))

    def __greater_than_or_equal(self, data, variable, value):
        log_flag = False
        for index, case_ in enumerate(data.get('children')):
            # 进行大于等于判断
            if variable >= value:
                # 处理逻辑
                if not log_flag:
                    log_flag = True
                    self.debug_log('✅ 要判断的值{}，要对比的值{}，条件成立，执行相关逻辑'.format(variable, value))
                self.handle_step(case_)
            else:
                raise AssertionError(self.warning_log('❌ 要判断的值{}，要对比的值{}，条件不成立，不执行相关逻辑'.format(variable, value)))

    def __less_than_or_equal(self, data, variable, value):
        log_flag = False
        for index, case_ in enumerate(data.get('children')):
            # 进行小于等于判断
            if variable <= value:
                # 处理逻辑
                if not log_flag:
                    log_flag = True
                    self.debug_log('✅ 要判断的值{}，要对比的值{}，条件成立，执行相关逻辑'.format(variable, value))
                self.handle_step(case_)
            else:
                raise AssertionError(self.warning_log('❌ 要判断的值{}，要对比的值{}，条件不成立，不执行相关逻辑'.format(variable, value)))

    def __contains(self, data, variable, value):
        log_flag = False
        for index, case_ in enumerate(data.get('children')):
            # 进行包含判断
            if value in variable:
                # 处理逻辑
                if not log_flag:
                    log_flag = True
                    self.debug_log('✅ 要判断的值{}，要对比的值{}，条件成立，执行相关逻辑'.format(variable, value))
                self.handle_step(case_)
            else:
                raise AssertionError(self.warning_log('❌ 要判断的值{}，要对比的值{}，条件不成立，不执行相关逻辑'.format(variable, value)))

    def __not_contains(self, data, variable, value):
        log_flag = False
        for index, case_ in enumerate(data.get('children')):
            # 进行不包含判断
            if value not in variable:
                # 处理逻辑
                if not log_flag:
                    log_flag = True
                    self.debug_log('✅ 要判断的值{}，要对比的值{}，条件成立，执行相关逻辑'.format(variable, value))
                self.handle_step(case_)
            else:
                raise AssertionError(self.warning_log('❌ 要判断的值{}，要对比的值{}，条件不成立，不执行相关逻辑'.format(variable, value)))

    def __empty(self, data, variable, value):
        log_flag = False
        for index, case_ in enumerate(data.get('children')):
            # 进行为空判断
            if not variable:
                # 处理逻辑
                if not log_flag:
                    log_flag = True
                    self.debug_log('✅ 要判断的值{}，要对比的值无，条件成立，执行相关逻辑'.format(variable))
                self.handle_step(case_)
            else:
                raise AssertionError(self.warning_log('❌ 要判断的值{}，要对比的值无，条件不成立，不执行相关逻辑'.format(variable)))

    def __not_empty(self, data, variable, value):
        log_flag = False
        for index, case_ in enumerate(data.get('children')):
            # 进行不为空判断
            if variable:
                # 处理逻辑
                if not log_flag:
                    log_flag = True
                    self.debug_log('✅ 要判断的值{}，要对比的值无，条件成立，执行相关逻辑'.format(variable))
                self.handle_step(case_)
            else:
                raise AssertionError(self.warning_log('❌ 要判断的值{}，要对比的值无，条件不成立，不执行相关逻辑'.format(variable)))

    def handle_step(self, case_):
        """ 处理单个步骤。
        :param case_: 一个字典，包含步骤的类型和相关数据，可能包括子步骤。
        :return: 返回一个布尔值，表示该步骤是否已成功处理。
        """
        # 获取步骤类型
        type_ = case_.get('type')

        # 判断步骤类型是否为'if'或'for'，且没有子步骤
        if type_ in ['if', 'for']:
            if not case_.get('children'):
                self.debug_log("开始执行子节点步骤 -->【{}】".format(case_.get('title', '')))
                self.debug_log("【{}】 无子节点步骤，执行结束".format(case_.get('title', '')))
                return True

        # 尝试从type_handlers获取对应的处理方法
        handler_method = self.type_handlers.get(type_)
        if handler_method:
            self.debug_log("开始执行子节点步骤 -->【{}】".format(case_.get('title', '')))
            # 使用 getattr 来获取方法并调用
            handler = getattr(self, handler_method)
            handler(case_)
        else:
            # 如果没有找到对应的处理方法，记录错误日志
            self.error_log("【{}】 未找到对应的处理方法".format(case_.get('title', '')))

    def __parser_variable(self, data):
        """替换变量"""
        pattern = r'\{{(.+?)}}'
        old_data = data
        if isinstance(data, OrderedDict):
            data = dict(data)
        data = str(data)

        while re.search(pattern, data):
            res2 = re.search(pattern, data)
            item = res2.group()
            attr = res2.group(1)
            value = ENV.get(attr) if self.env.get(attr) is None else self.env.get(attr)
            if value is None:
                raise ValueError('变量引用错误：\n{}\n中的变量{},在当前运行环境中未找到'.format(
                    json.dumps(old_data, ensure_ascii=False, indent=2), attr)
                )
            if isinstance(value, Number):
                s = data.find(item)
                dd = data[s - 1:s + len(item) + 1]
                data = data.replace(dd, str(value))
            elif isinstance(value, str) and "'" in value:
                data = data.replace(item, value.replace("'", '"'))
            else:
                data = data.replace(item, str(value))
        return eval(data)

    def save_env_variable(self, name, value):
        self.info_log('🌛 -->设置临时变量')
        self.debug_log('🍖变量名：{}，🍗变量值：{}'.format(name, value))
        if DEBUG:
            self.warning_log('提示: 调试模式运行,设置的临时变量均保存到Debug全局变量中')
            ENV[name] = value
        else:
            self.env[name] = value

    def save_global_variable(self, name, value):
        self.info_log('🌞 -->设置全局变量')
        self.debug_log('🍖变量名：{}，🍗变量值：{}'.format(name, value))
        ENV[name] = value

    def delete_env_variable(self, name):
        """删除临时变量"""
        self.info_log('🔴删除临时变量：{}'.format(name, ))
        del self.env[name]

    def delete_global_variable(self, name):
        """删除全局变量"""
        self.info_log('🔴删除全局变量：{}'.format(name))
        del ENV[name]

    def json_extract(self, obj, ext):
        """jsonpath数据提取"""
        self.info_log('-----------jsonpath提取数据-----------')
        value = jsonpath(obj, ext)
        value = value[0] if value else ''
        self.debug_log('\n数据源：{}'.format(obj))
        self.debug_log('\n提取表达式：{}'.format(ext))
        self.debug_log('\n提取结果:{}'.format(value))
        return value

    def re_extract(self, string, ext):
        """正则表达式提取数据提取"""
        self.info_log('-----------正则提取数据------------')
        value = re.search(ext, string)
        value = value.group(1) if value else ''
        self.debug_log('\n数据源：{}'.format(string))
        self.debug_log('\n提取表达式：{}'.format(ext))
        self.debug_log('\n提取结果:{}'.format(value))
        return value

    def assertion(self, methods, expected, actual):
        """
        断言
        :param methods: 比较方式
        :param expected: 预期结果
        :param actual: 实际结果
        :return:
        """
        methods_map = {
            "相等": self.assertEqual,
            "包含": self.assertIn,
        }
        self.info_log('↪ 【开始断言】')
        self.debug_log('比较方式:{}'.format(methods))
        self.debug_log('预期结果:{}'.format(expected))
        self.debug_log('实际结果:{}'.format(actual))
        assert_method = methods_map.get(methods)
        if assert_method:
            assert_method(expected, actual)
            self.info_log('↩ 【断言通过】')
        else:
            raise TypeError('断言比较   方法{},不支持!'.format(methods))


def run(case_data, env_config, thread_count=1, debug=True):
    """
    :param case_data: 测试套件数据
    :param env_config: 用例执行的环境配置
        env_config:{
        'ENV':{"host":'http//:127.0.0.1'},
        'db':[{},{}],
        'FuncTools':'工具函数文件'
        }
    :param thread_count: 运行线程数
    :param debug: 单接口调试用debug模式
    :return:
        debug模式：会返回本次运行的结果和 本次运行设置的全局变量，
    """
    global global_func, db, DEBUG, ENV, global_func_file
    global_func_file = env_config.get('global_func', b'')

    if global_func_file:
        exec(global_func_file, global_func.__dict__)
    '''
    if global_func:
        with open('global_func.py', 'w', encoding='utf-8') as f:
            f.write(global_func_file)
    # 更新运行环境
    global_func = importlib.import_module('global_func')
    '''
    DEBUG = debug
    ENV = {**env_config.get('ENV', {})}
    db.init_connect(env_config.get('DB', []))
    # 生成测试用例
    suite = GenerateCase().data_to_suite(case_data)
    # 运行测试用例
    runner = TestRunner(suite=suite)
    result = runner.run(thread_count=thread_count)
    # if global_func:
    #     os.remove('global_func.py')
    # 断开数据库连接
    db.close_connect()
    if debug:
        return result, ENV
    else:
        return result
