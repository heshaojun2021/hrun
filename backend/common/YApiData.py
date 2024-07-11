# -*- coding: utf-8 -*-
# @author: HRUN

import json

class DataWorkers:
    def main_func(self, format, data, treenode, project):
        """
        根据提供的数据格式和数据，处理并返回接口信息。
        :param format: 数据格式，可以是'list'或'json'。
        :param data: 需要处理的数据。
        :return: 根据格式不同，返回一个接口信息的列表或字典。
        """
        self.interface_data = []
        if format == 'list':
            interface_data = []
            for item in data:
                interface_json = {
                    "name": item.get('title', ''),
                    "url": item.get('path', ''),
                    "method": item.get('method', ''),
                    "YApi_id": item.get('_id', ''),
                    "treenode": treenode,
                    "project": project,
                    "creator": "YApi导入",
                    "file": self.__get_file(item),
                    "interface_tag": self.__get_tag(item),
                    "request": self.__get_request(item),
                    "headers": self.__get_headers(item)
                }
                interface_data.append(interface_json)
            return interface_data

        if format == 'json':
            interface_json = {
                "name": data.get('title', ''),
                "url": data.get('path', ''),
                "method": data.get('method', ''),
                "YApi_id": data.get('_id', ''),
                "treenode": treenode,
                "project": project,
                "creator": "YApi导入",
                "file": self.__get_file(data),
                "interface_tag": self.__get_tag(data),
                "request": f'{self.__get_request(data)}',
                "headers":  f'{self.__get_headers(data)}'
            }
            return interface_json if data else {}
        else:
            return []

    def __get_request(self, data):
        query = {}
        json_data = {}
        if data.get("req_body_type") == 'json' and data.get("req_body_other"):
            if data.get("req_query"):
                for item in data.get("req_query"):
                    query[item.get("name", '')] = item.get("example", '')
            if data.get("req_body_other"):
                req_body_other = data.get("req_body_other")
                if req_body_other:
                    req_body_other_dict = json.loads(req_body_other)
                    properties = req_body_other_dict.get("properties", {})
                    for key, value in properties.items():
                        json_data[key] = value.get("default", "") or value.get("description", "")
                    return {"json": json_data, "data": None, "params": query}
            return {"json": json_data, "data": None, "params": query}

        elif data.get("req_body_type") == 'raw' and data.get("req_body_other"):
            if data.get("req_query"):
                for item in data.get("req_query"):
                    query[item.get("name", '')] = item.get("example", '')
            if data.get("req_body_other"):
                json_data = json.loads(data.get("req_body_other", {}))
                return {"json": json_data, "data": None, "params": query}
            return {"json": json_data, "data": None, "params": query}
        return {"json": json_data, "data": None, "params": query}
    def __get_file(self, data):
        form_data = []
        if data.get("req_body_type") == 'form' and data.get('req_body_form'):
            for item in data.get('req_body_form'):
                if item.get("type") == 'text':
                    form_data.append([item.get("name"), item.get("example", '')])
                elif item.get("type") == 'file':
                    form_data.append([item.get("name"), '文件地址', '文件格式'])
            return form_data
        return []

    def __get_headers(self, data):
        headers = {}
        if data.get("req_headers"):
            for item in data.get("req_headers"):
                headers[item.get("name")] = item.get("value") or item.get("example", '')
            return headers
        return headers

    def __get_tag(self, data):
       if data.get("tag"):
           return {"tag": data.get("tag")}
       return {"tag": []}