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
from application.glass_management.models import *
# from application.glass_management.recommend import recommend
from application.glass_management import services

"""
查询镜架SKU
"""
class SearchModeltypeOrSKUView(View):
	def post(self, request: HttpRequest):
		# 调用查询镜架方法
		result = services.SearchModeltypeOrSKU(request)
		# 返回结果
		return result
class SearchSKUView(View):
	def get(self, request: HttpRequest):
		# 调用查询镜架方法
		result = services.SearchSKU(request)
		# 返回结果
		return result

"""
删除镜架SKU
"""
class DeleteEyeglassFrameEntrysView(View):
	def post(self, request: HttpRequest):
		# 调用删除镜架方法
		result = services.DeleteEyeglassFrameEntrys(request)
		# 返回结果
		return result

"""
保存新镜架所有信息
"""
class SaveNewEyeglassFrameView(View):
	def post(self, request: HttpRequest):
		# 调用保存新镜架所有信息的服务方法
		result = services.SaveNewEyeglassFrame(request)
		# 返回结果
		return result
	
"""
编辑镜架信息
"""
class SaveEditEyeglassFrameView(View):
	def post(self, request: HttpRequest):
		# 调用修改镜架信息的服务方法
		result = services.SaveEditEyeglassFrame(request)
		# 返回结果
		return result
"""
查询镜架详情
"""
class GetEyeglassFrameDetailView(View):
	def get(self, request: HttpRequest):
		# 调用查询对应镜架的方法
		result = services.GetEyeglassFrameDetail(request)
		return result
	
"""
获取所有镜架基本信息
"""
class GetAllEyeglassFrameEntryView(View):
	def get(self, request: HttpRequest):
		# 调用查询所有镜架基本信息的服务方法
		result = services.GetAllEyeglassFrameEntrys(request)
		# 返回结果
		return result
	
"""
获取所有镜架品牌
"""
class GetAllBrandsView(View):
	def get(self, request: HttpRequest):
		# 调用查询所有镜架品牌的服务方法
		result = services.GetAllBrands(request)
		# 返回结果
		return result
	
"""
获取所有镜架型号
"""
class GetAllModelTypesView(View):
	def get(self, request: HttpRequest):
		# 调用查询所有镜架型号的服务方法
		result = services.GetAllModelTypes(request)
		# 返回结果
		return result
	
"""
获取所有镜架材质
"""
class GetAllMaterialsView(View):
	def get(self, request: HttpRequest):
		# 调用查询所有镜架材质的服务方法
		result = services.GetAllMaterials(request)
		# 返回结果
		return result
	
"""
获取所有镜架颜色
"""
class GetAllColorsView(View):
	def get(self, request: HttpRequest):
		# 调用查询所有镜架颜色的服务方法
		result = services.GetAllColors(request)
		# 返回结果
		return result
	
"""
获取所有镜架形状
"""
class GetAllShapesView(View):
	def get(self, request: HttpRequest):
		# 调用查询所有镜架形状的服务方法
		result = services.GetAllShapes(request)
		# 返回结果
		return result

"""
获取所有镜架风格
"""
class GetAllStylesView(View):
	def get(self, request: HttpRequest):
		# 调用查询所有镜架风格的服务方法
		result = services.GetAllStyles(request)
		# 返回结果
		return result
	

	

###################################################################################################################
"""
添加镜架风格
"""
def AddStyle(request: HttpRequest):
	if request.method == 'POST':
		style = request.POST.get('style', "")
		if style:
			styles = EyeglassFrameStyleType.objects.filter(style=style)
			if len(styles) == 0:
				style = EyeglassFrameStyleType(style=style)
				style.save()
				return JsonResponse(data={"result": "添加风格成功"})
			else:
				return JsonResponse(data={"result": "风格已存在"})
		else:
			return JsonResponse(data={"result": "风格不能为空"})
	else:
		return JsonResponse(data={"result": "请求方式错误"})
	
def AddStyleList(request: HttpRequest):
	if request.method == 'POST':
		style_list = request.POST.getlist('style', [])
		for style in style_list:
			styles = EyeglassFrameStyleType.objects.filter(style=style)
			if len(styles) == 0:
				style = EyeglassFrameStyleType(style=style)
				style.save()
		return JsonResponse(data={"result": "添加风格成功"})
	else:
		return JsonResponse(data={"result": "请求方式错误"})

"""
添加镜架材质
"""
def AddMaterial(request: HttpRequest):
	if request.method == 'POST':
		material = request.POST.get('material', "")
		if material:
			materials = EyeglassFrameMaterialType.objects.filter(material=material)
			if len(materials) == 0:
				material = EyeglassFrameMaterialType(material=material)
				material.save()
				return JsonResponse(data={"result": "添加材质成功"})
			else:
				return JsonResponse(data={"result": "材质已存在"})
		else:
			return JsonResponse(data={"result": "材质不能为空"})
	else:
		return JsonResponse(data={"result": "请求方式错误"})
	
def AddMaterialList(request: HttpRequest):
	if request.method == 'POST':
		material_list = request.POST.getlist('material', [])
		for material in material_list:
			materials = EyeglassFrameMaterialType.objects.filter(material=material)
			if len(materials) == 0:
				material = EyeglassFrameMaterialType(material=material)
				material.save()
		return JsonResponse(data={"result": "添加材质成功"})
	else:
		return JsonResponse(data={"result": "请求方式错误"})
	

"""
添加镜架颜色
"""
def AddColor(request: HttpRequest):
	if request.method == 'POST':
		color = request.POST.get('color', "")
		if color:
			colors = EyeglassFrameColorType.objects.filter(color=color)
			if len(colors) == 0:
				color = EyeglassFrameColorType(color=color)
				color.save()
				return JsonResponse(data={"result": "添加颜色成功"})
			else:
				return JsonResponse(data={"result": "颜色已存在"})
		else:
			return JsonResponse(data={"result": "颜色不能为空"})
	else:
		return JsonResponse(data={"result": "请求方式错误"})
	
def AddColorList(request: HttpRequest):
	if request.method == 'POST':
		color_list = request.POST.getlist('color', [])
		for color in color_list:
			colors = EyeglassFrameColorType.objects.filter(color=color)
			if len(colors) == 0:
				color = EyeglassFrameColorType(color=color)
				color.save()
		return JsonResponse(data={"result": "添加颜色成功"})
	else:
		return JsonResponse(data={"result": "请求方式错误"})

"""
添加镜架形状
"""
def AddShape(request: HttpRequest):
	if request.method == 'POST':
		shape = request.POST.get('shape', "")
		if shape:
			shapes = EyeglassFrameShapeType.objects.filter(shape=shape)
			if len(shapes) == 0:
				shape = EyeglassFrameShapeType(shape=shape)
				shape.save()
				return JsonResponse(data={"result": "添加形状成功"})
			else:
				return JsonResponse(data={"result": "形状已存在"})
		else:
			return JsonResponse(data={"result": "形状不能为空"})
	else:
		return JsonResponse(data={"result": "请求方式错误"})
	
def AddShapeList(request: HttpRequest):
	if request.method == 'POST':
		shape_list = request.POST.getlist('shape', [])
		for shape in shape_list:
			shapes = EyeglassFrameShapeType.objects.filter(shape=shape)
			if len(shapes) == 0:
				shape = EyeglassFrameShapeType(shape=shape)
				shape.save()
		return JsonResponse(data={"result": "添加形状成功"})
	else:
		return JsonResponse(data={"result": "请求方式错误"})
















