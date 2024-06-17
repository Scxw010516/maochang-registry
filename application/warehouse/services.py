import json
import decimal
from utils import R, regular
from utils import utils
from django.db import transaction
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, HttpRequest

from application.warehouse import models
from application.warehouse import forms

def GetAllWarehouses(request:HttpRequest):
    """
    获取所有仓库

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """

    # 查询所有仓库
    warehouses = models.Warehouse.objects.all()

    # 判断查询结果是否为空
    if not warehouses:
        return R.failed(msg="仓库为空")

    # 构建查询结果
    search_result = [{
        'id': warehouse.id,
        'warehouse': warehouse.warehouse,
        'address': warehouse.address,
    }for warehouse in warehouses]

    # 返回查询结果
    return R.ok(data=search_result)






