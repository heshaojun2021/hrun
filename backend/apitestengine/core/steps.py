# -*- coding: utf-8 -*-
# @author: HRUN


class LoopController:
    """
    循环控制器。

    参数:
    - data: 初始化实例时传入的数据，赋值给self.data。

    属性:
    - data: 存储传入的初始化数据。
    - select: 用于存储步骤控制器选择的选项，默认为空字符串。
    - cycleIndex: 循环次数，默认为0。
    - cycleInterval: 循环间隔单位为S，默认为0。
    - variable: 要遍历的变量，默认为空字符串。
    - variableName: 要使用的变量名，默认为空字符串。
    """

    def __init__(self, data):
        self.data = data
        self.select = ''
        self.cycleIndex = 0
        self.cycleInterval = 0
        self.variable = ''
        self.variableName = ''




class JudgeController:
    """
    判断控制器。

    参数:
    - data: 传入的数据，将被存储在实例的data属性中。

    属性:
    - data: 存储传入的初始数据。
    - variable: 要判断的变量，默认为空字符串。
    - JudgmentMode: 用于存储判断模式，默认为空字符串。
    - value: 用于存储某个值，默认为空字符串。
    """
    def __init__(self,data):
        self.data = data
        self.variable = ''
        self.JudgmentMode = ''
        self.value = ''


class ScriptController:
    """
    自定义脚本。

    :param data: 一个包含数据的字典，该字典应至少包含'script'键。
    :type data: dict
    """
    def __init__(self, data):
        self.data = data
        self.script = data.get('script')

    @classmethod
    def print(cls, case_):

        print(case_.get('script'))


class TimerController:
    """
    定时控制器。

    :param data: 传入的数据，将存储在实例的data属性中。
    :time: 定时时间。
    """
    def __init__(self,data):
        self.data = data
        self.time = ''
