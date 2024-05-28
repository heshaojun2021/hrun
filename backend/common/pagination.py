from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class TenPerPageNumberPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'size'   # 自定义页面数量的参数名
    page_query_param = 'page'  # 修改表示页面的参数名
    max_page_size = 1000  # 一页最大的数据条数

    def get_paginated_response(self, data):
        return Response({
            'current': int(self.request.GET.get(self.page_query_param, 1)),
            'pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'size': int(self.request.GET.get(self.page_size_query_param, self.page_size)),
            'result': data,
            'message': '成功'
        })