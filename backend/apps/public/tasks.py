import requests

from common.YApiData import DataWorkers
from projects.serializers import newInterfaceSerializer
from projects.models import newInterface

from celery import shared_task

@shared_task
def import_run_yapi(YApi_data):
    url = YApi_data.get('url') + "/api/interface/list"
    interface_url = YApi_data.get('url') + '/api/interface/get'
    list_query = {
        "project_id": YApi_data.get('YApi_id'),
        "token": f"{YApi_data.get('token')}",
        "limit": "100"
    }

    page = 1
    has_next_page = True
    interfaces = []
    format = YApi_data.get('format')
    while has_next_page:
        list_query["page"] = str(page)
        response = requests.get(url, params=list_query)
        if response.status_code == 200 and response.json().get("data"):
            data = response.json()
            list_data = data["data"].get("list", [])

            if not list_data:
                break

            for item in list_data:
                interface_id = item.get("_id")
                interface_query = {
                    "id": interface_id,
                    "token": f"{YApi_data.get('token')}",
                }
                interface_response = requests.get(interface_url, params=interface_query)
                if interface_response.status_code == 200 and interface_response.json().get("data"):
                    if format == 'list':
                        interfaces.append(interface_response.json().get("data"))
                    elif format == 'json':
                        data = DataWorkers().main_func(format, interface_response.json().get("data"), YApi_data.get('treenode'), YApi_data.get('project'))
                    else:
                        raise Exception("请求格式错误")
                else:
                    raise Exception(response.text)

            page += 1
        else:
            raise Exception(response.text)

    if format == 'list':
        data = DataWorkers().main_func(format, interfaces, YApi_data.get('treenode'), YApi_data.get('project'))
        serializer = newInterfaceSerializer(data=data, many=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            yapi_ids = [item['YApi_id'] for item in validated_data]
            existing_yapi_ids = newInterface.objects.filter(YApi_id__in=yapi_ids).values_list('YApi_id', flat=True)
            duplicates = [yapi_id for yapi_id in yapi_ids if yapi_id in existing_yapi_ids]
            new_interfaces = []
            for data in validated_data:
                if data['YApi_id'] in duplicates:
                    # 找到重复的数据，执行批量保存
                    existing_interface = newInterface.objects.get(YApi_id=data['YApi_id'])
                    if existing_interface.YApi_status != 1:
                        for key, value in data.items():
                            setattr(existing_interface, key, value)
                        existing_interface.save()  # 保存更新后的数据
                else:
                    # 找到非重复的数据，执行批量新增
                    new_interfaces.append(newInterface(**data))

            newInterface.objects.bulk_create(new_interfaces)
        return serializer.data

