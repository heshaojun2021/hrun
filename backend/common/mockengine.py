# -*- coding: utf-8 -*-
# @author: HRUN

import json
import time
import subprocess
import xml.etree.ElementTree as ET

from rest_framework import status
from rest_framework.response import Response

from projects.models import Mock




class MockEngine:
    def __init__(self, request, path, mock_id):
        self.request = request
        self.path = path
        self.mock_id = mock_id

    def verification(self):
        """
        mock接口数据校验层
        """
        mock_api_detail = []
        try:
            mock_api = Mock.objects.get(mockId=self.mock_id)
            for detail in mock_api.MockDetail.values():
                mock_api_detail.append(detail)

            if not mock_api.status:
                return Response({"message": 'mock接口已禁用'}, status=status.HTTP_400_BAD_REQUEST)

            if mock_api.method != self.request.method:
                return Response({"message": '请求方法错误'}, status=status.HTTP_400_BAD_REQUEST)

            return mock_api_detail, mock_api

        except Mock.DoesNotExist:
            return Response({"message": 'mock接口不存在'}, status=status.HTTP_404_NOT_FOUND)

    def analytic_data(self, datasets: list):
        """
        mock接口数据分析层
        """
        success_count = 0
        success_data = []
        # 遍历数据集
        for data in datasets:
            compare_result = self.judge_diff(data.get('conditionForm', []))
            print(compare_result)
            if compare_result:
                # 只统计匹配成功的期望 true
                success_count += 1
                success_data.append(data)

        if success_count > 1:
            # 匹配到多个期望
            return Response({"message": 'mock接口中匹配到多个结果,请确认接口配置是否正确!'}, status=status.HTTP_400_BAD_REQUEST)

        elif success_count == 1:
            return success_data[0]

        else:
            # 没有设置期望表单或未匹配上
            return Response({"message": '成功'}, status=status.HTTP_200_OK)

    def judge_diff(self, expect_form: list):
        """
        mock接口数据判断比对
        """
        if len(expect_form) == 1:
            params = expect_form[0]
            if all(value == '' or value is None for value in params.values()):
                return True
            source = self.data_source(params.get('location'))
            paramName = params.get('paramName')

            # 处理值类型转换
            value = self.value_type(params.get('value', ''), params.get('valueType','String'))
            if paramName in source:
                for key in source:
                    source_value = source[key]
                    comparison = self.comparison(source_value,params.get('comparison'),value)
                    if comparison:
                        return True
                    else:
                        return False
            else:
                return False

        elif len(expect_form) > 1:
            for params in expect_form:
                if all(value == '' or value is None for value in params.values()):
                    return True
                source = self.data_source(params.get('location'))
                paramName = params.get('paramName')
                # 处理值类型转换
                value = self.value_type(params.get('value', ''), params.get('valueType', 'String'))
                if paramName in source:
                    for key in source:
                        source_value = source[key]
                        comparison = self.comparison(source_value, params.get('comparison'), value)
                        if comparison:
                            return True
                        else:
                            return False
                else:
                    return False

        else:
            return True

    def data_source(self, dataType: str) -> dict:
        if dataType == 'query':
            query_params = self.request.GET
            params = {}
            # 处理所有的查询参数
            for key in query_params.keys():
                value = query_params.get(key, '')
                params[key] = value
            return params

        elif dataType == 'body':
            return self.request.data

        elif dataType == 'path':
            return self.path

        elif dataType == 'header':
            return self.request.headers

        else:
            return {}

    def comparison(self, source_value, comparison_type: str, value):
        """
        mock传参比对
            source_value: 数据源中的值
            comparison_type: 比对类型
            value: 比对值
        """
        comparison_mapping = {
            'equal': lambda x, y: x == y,
            'notEqual': lambda x, y: x != y,
            'greaterThan': lambda x, y: x > y,
            'lessThan': lambda x, y: x < y,
            'greaterThanOrEqual': lambda x, y: x >= y,
            'lessThanOrEqual': lambda x, y: x <= y,
            'contains': lambda x, y: y in x,
            'notContains': lambda x, y: y not in x,
            'empty': lambda x, y: x is None,
            'notEmpty': lambda x, y: x is not None
        }

        if comparison_type not in comparison_mapping:
            raise ValueError(f"Invalid comparison type: {comparison_type}")

        return comparison_mapping[comparison_type](source_value, value)

    def value_type(self, value, value_type: str):
        """
        mock传参值类型转换
        """
        try:
            if value_type == 'String':
                return str(value)
            elif value_type == 'Integer':
                return int(value)
            elif value_type == 'Float':
                return float(value)
            elif value_type == 'Boolean':
                return bool(value)
            elif value_type == 'Array':
                return list(value)
            else:
                return value
        except (TypeError, ValueError):
            return value

    def response(self, data: dict):
        """
        mock接口响应体处理
        """
        mock_js = data.get('data', '')
        response_data = self.mock_js(mock_js)
        if data.get('paramType') == 'json':
            if response_data is not None:
                return json.loads(response_data)
            else:
                return {}
        elif data.get('paramType') == 'xml':
            if response_data is not None:
                root = ET.Element('person')  # 创建根节点
                for key, value in eval(response_data).items():
                    child = ET.Element(key)  # 创建子节点
                    child.text = str(value)
                    root.append(child)
                xml_str = ET.tostring(root, encoding='utf-8', method='xml')
                return xml_str.decode('utf-8')
            else:
                return "<person></person>"

        elif data.get('paramType') == 'html':

            return str(response_data)

        else:
            return {}

    def headers(self, data):
        """
        mock接口响应头处理
        """
        headers_data = self.mock_js(data)
        return json.loads(headers_data)

    def config(self, data: dict):
        """
        mock接口设置
        """
        time.sleep(int(data.get('time', 0)))
        return int(data.get('statusCode', 200))

    def mock_js(self, data):
        data_json = json.dumps(data)
        # 构造Node.js命令
        node_command = ['node', 'mock.js', data_json]
        # 执行Node.js脚本并获取输出
        result = subprocess.run(node_command, capture_output=True, text=True)

        return json.loads(result.stdout)

    def main(self):
        """
        mock接口执行层
        """
        # 1、数据校验
        validation_result = self.verification()
        # 检查验证结果
        if isinstance(validation_result, Response):
            return validation_result
        # 2、数据分析
        mock_api_detail, mock_api = validation_result
        # 数据匹配
        analytic_data = self.analytic_data(mock_api_detail)
        if isinstance(analytic_data, Response):
            return analytic_data

        # 3、ip分发校验与结果返回
        response = self.response(analytic_data.get('response'))
        headers = self.headers(analytic_data.get('headers'))
        config = self.config(analytic_data.get('config'))
        if analytic_data.get('ipCode'):
            source_ip = self.request.META.get('REMOTE_ADDR')+':' + self.request.META.get('SERVER_PORT')
            if source_ip in analytic_data.get('ipInput'):
                return Response(response, headers=headers, status=config)
            elif analytic_data.get('ipInput', '') is None:
                # ip校验开启了但是没有配置ip，继续获取期望的返回信息
                return Response(response, headers=headers, status=config)

            else:
                return Response({"message": '访问主机ip校验不通过'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # 未开启ip校验，继续获取期望的返回信息
            return Response(response, headers=headers, status=config)