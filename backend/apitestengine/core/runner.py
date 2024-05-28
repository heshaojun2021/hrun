
import copy
import time
import traceback
import unittest
from concurrent.futures.thread import ThreadPoolExecutor


class TestResult(unittest.TestResult):
    """ 测试结果记录"""

    def __init__(self):
        super().__init__()

        self.result = {
            "all": 0,
            "success": 0,
            "fail": 0,
            "error": 0,
            "cases": [],
            "state": "",
            "name": "",
        }

    def startTest(self, test):
        """
        当测试用例测试即将运行时调用
        :return:
        """
        super().startTest(test)
        self.start_time = time.time()
        data = getattr(test, '_testMethodDoc')
        test.name, _, test.type = data.partition('_')
        if test.name !='None':
            getattr(test, 'info_log')("▶️开始执行步骤——>【{}】\n".format(test.name))

    def stopTest(self, test):
        """
        当测试用列执行完成后进行调用
        :return:
        """
        test.run_time = '{:.3}s'.format((time.time() - self.start_time))
        self.result['cases'].append(test)
        self.result['all'] += 1
        self.result['name'] = test.__class__.__name__

    def stopTestRun(self, title=None):
        """
        测试用例执行完手动调用统计测试结果的相关数据
        :param title:
        :return:
        """
        if len(self.errors) > 0:
            self.result['state'] = 'error'
        elif len(self.failures) > 0:
            self.result['state'] = 'fail'
        else:
            self.result['state'] = 'success'

    def addSuccess(self, test):
        """用例执行通过，成功数量+1"""
        self.result["success"] += 1
        test.state = '成功'
        data = getattr(test, '_testMethodDoc')
        test.name, _, test.type = data.partition('_')
        if test.name !='None':
            getattr(test, 'info_log')("🎉 {}执行——>【通过】\n".format(test.name))
        getattr(test, 'info_log')('⏹️步骤运行结束')
    def addFailure(self, test, err):
        """
        :param test: 测试用例
        :param err:  错误信息
        :return:
        """

        self.result["fail"] += 1
        test.state = '失败'
        data = getattr(test, '_testMethodDoc')
        test.name, _, test.type = data.partition('_')
        if test.name =='None':
            getattr(test, 'warning_log')("😅 {}执行——>【失败】\n".format('用例执行失败'))
        else:
            getattr(test, 'warning_log')("😅 {}执行——>【失败】\n".format(test.name))
        super().addFailure(test, err)

    def addError(self, test, err):
        """
        修改错误用例的状态
        :param test: 测试用例
        :param err:错误信息
        :return:
        """
        super().addError(test, err)
        self.result["error"] += 1
        test.state = '错误'
        getattr(test, 'exception_log')(''.join(traceback.format_exception(*err)))
        data = getattr(test, '_testMethodDoc')
        test.name, _, test.type = data.partition('_')
        if test.name == 'None':
            getattr(test, 'error_log')("💣 {}执行——>【错误】\n".format('用例执行错误'))
        else:
            getattr(test, 'error_log')("💣 {}执行——>【错误】\n".format(test.name))




class TestRunner:
    """测试运行器"""

    def __init__(self, suite):
        """套件"""
        self.suite = suite
        self.result_list = []

    def __classification_suite(self):
        """
        将测试套件中的用例，根据用例类位单位，拆分成多个测试套件，打包成列表类型
        :return: list-->[suite,suite,suite.....]
        """
        suites_list = []
        def wrapper(suite):
            for item in suite:
                if isinstance(item, unittest.TestCase):
                    suites_list.append(suite)
                    break
                else:
                    wrapper(item)

        wrapper(copy.deepcopy(self.suite))
        return suites_list

    def __parser_results(self):
        """解析汇总测试结果"""
        result = {
            "results": [],
            "all": 0,
            "success": 0,
            "error": 0,
            "fail": 0,
        }
        for cls in self.result_list:
            cases_info = cls.result['cases']
            result['all'] += cls.result['all']
            result['success'] += cls.result['success']
            result['error'] += cls.result['error']
            result['fail'] += cls.result['fail']

            cls.result['cases'] = [{k: v for k, v in res.__dict__.items() if not k.startswith('_')} for res in
                                   cases_info]
            result['results'].append(cls.result)

        return result

    def run(self, thread_count=1):
        """
        支持多线程执行
        注意点：如果多个测试类共用某一个全局变量，由于资源竞争可能会出现错误
        :param thread_count:线程数量，默认位1
        :return:测试运行结果
        """
        # 将测试套件按照用例类进行拆分
        suites = self.__classification_suite()
        with ThreadPoolExecutor(max_workers=thread_count) as ts:
            for i in suites:
                res = TestResult()
                self.result_list.append(res)
                ts.submit(i.run, result=res).add_done_callback(res.stopTestRun)
        result = self.__parser_results()
        return result
