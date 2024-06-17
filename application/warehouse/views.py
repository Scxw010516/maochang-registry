# 功能库
from typing import Dict, List
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, HttpRequest
import cv2
import random
import json
from PIL import Image, ImageDraw, ImageFont, ImageColor
from django.db.models import Q
from django.views import View
from io import BytesIO
import base64

# 资源库
from application.warehouse.models import *
from application.warehouse import services

"""
查询所有镜架仓库
"""
class GetAllWarehousesView(View):
	def get(self, request: HttpRequest):
		# 调用查询镜架仓库方法
		result = services.GetAllWarehouses(request)
		# 返回结果
		return result

###################################################################################################################
"""
添加镜架仓库
"""
def AddWarehouse(request: HttpRequest):
	if request.method == 'POST':
		warehouse = request.POST.get('warehouse', "")
		address = request.POST.get('address', "")
		if warehouse and address:
			warehouses = Warehouse.objects.filter(warehouse=warehouse)
			if len(warehouses) == 0:
				Warehouse_instance = Warehouse(warehouse=warehouse, address=address)
				Warehouse_instance.save()
				return JsonResponse(data={"result": "添加镜架仓库成功"})
			else:
				return JsonResponse(data={"result": "镜架仓库已存在"})
		else:
			return JsonResponse(data={"result": "镜架仓库不能为空"})
	else:
		return JsonResponse(data={"result": "请求方式错误"})
















