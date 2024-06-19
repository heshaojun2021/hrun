from rest_framework.exceptions import APIException





class CustomException(APIException):
    status_code = 500
    default_detail = '删除失败，请检查相关引用!'
    default_code = 'invalid'




# class myModelViewSet(mixins.CreateModelMixin,
#                      mixins.RetrieveModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.DestroyModelMixin,
#                      mixins.ListModelMixin):
# raiseErrorValue方法重写