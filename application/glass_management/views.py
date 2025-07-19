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


# """
# 获取所有品牌
# """
# def all_brands(request):
# 	entries_property = set()
# 	for entry in EyeglassFrameEntry.objects.all():
# 		entries_property.add(entry.brand)
# 	return JsonResponse(data={"result": list(entries_property)})

# """
# 获取所有型号
# """
# def all_model_types(request):
# 	entries_property = set()
# 	for entry in EyeglassFrameEntry.objects.all():
# 		entries_property.add(entry.model_type)
# 	return JsonResponse(data={"result": list(entries_property)})

# """
# 获取所有材质类型
# """
# def all_materials(request):
# 	entries_property = set()
# 	for entry in EyeglassFrameEntry.objects.all():
# 		entries_property.add(entry.material)
# 	return JsonResponse(data={"result": list(entries_property)})

# """
# 获取所有风格类型
# """
# def all_styles(request):
# 	entries_property = set()
# 	for _entry in EyeglassFrameEntry.objects.all():
# 		for link in EyeglassFrameEntryStyle.objects.filter(entry=_entry):
# 			entries_property.add(link.style.style)
# 	return JsonResponse(data={"result": list(entries_property)})

# """
# 按给定条件筛选镜架
# """
# def filter_by(request: HttpRequest):
# 	ids = set()
# 	if request.method == 'POST':
# 		brand_list: List[str] = json.loads(request.POST.get("brand_list", "[]"))
# 		material_list: List[str] = json.loads(request.POST.get("material_list", "[]"))
# 		style_list: List[str] = json.loads(request.POST.get("style_list", "[]"))
# 		if len(style_list) > 0:
# 			styles = EyeglassFrameStyleType.objects.filter(
# 				style__in=style_list
# 			)
# 			for entry in EyeglassFrameEntryStyle.objects.filter(
# 				style__in=styles
# 			):
# 				if entry.entry.brand in brand_list and entry.entry.material in material_list:
# 					ids.add(str(entry.entry.id))
# 	return JsonResponse(data={"result": list(ids)})

# """
# 先对镜架根据推荐度进行排序，再按给定条件筛选镜架
# """
# def filter_by_v2(request: HttpRequest):
# 	ids = set()
# 	if request.method == 'POST':
# 		brand_list: List[str] = json.loads(request.POST.get("brand_list", "[]"))
# 		material_list: List[str] = json.loads(request.POST.get("material_list", "[]"))
# 		style_list: List[str] = json.loads(request.POST.get("style_list", "[]"))
# 		face_params = json.loads(request.POST.get("face_params", "{}"))
# 		a =  face_params['头宽'] if '头宽' in face_params.keys() else 0.
# 		b =  face_params['鼻根宽'] if '鼻根宽' in face_params.keys() else 0.
# 		c =  face_params['左外眼角耳距'] if '左外眼角耳距' in face_params.keys() else 0.
# 		recommended = [i["glasses_id"] for i in recommend(24, "", a, b, c, None)]
# 		print(recommended)
# 		if len(style_list) > 0:
# 			styles = EyeglassFrameStyleType.objects.filter(
# 				style__in=style_list
# 			)
# 			for entry in EyeglassFrameEntryStyle.objects.filter(
# 				style__in=styles
# 			):
# 				if entry.entry.brand in brand_list and entry.entry.material in material_list:
# 					ids.add(str(entry.entry.id))
# 		rids = []
# 		for i in recommended:
# 			if str(i) in ids:
# 				rids.append(str(i))
# 		print(rids, ids)
# 	return JsonResponse(data={"result": rids})

# """
# 列出所有镜架
# """
# def list_all_eyeglass_frames(request: HttpRequest):
# 	result = []
# 	for entry in EyeglassFrameEntry.objects.all():
# 		result.append({
# 			"brand": entry.brand,
# 			"model-type": entry.model_type,
# 			"price": str(entry.price),
# 			"material": entry.material,
# 			"create-time": entry.create_time.strftime('%Y-%m-%d %H:%M:%S'),
# 			"update-time": entry.update_time.strftime('%Y-%m-%d %H:%M:%S')
# 		})
# 	return JsonResponse(data={"result": result})

# """
# 获取图片地址
# """
# def get_image_path(_id):
# 	return EyeglassFrameDetectionResult.objects.filter(entry=EyeglassFrameEntry.objects.filter(id=_id)[0])[0].foreview

# """
# 通过id获取图片地址
# """
# def get_image_path_by_id(request: HttpRequest):
# 	try:
# 		_id = int(json.loads(request.GET.get('id', "-1")))
# 	except:
# 		_id = -1
# 	return JsonResponse(data={"result": get_image_path(_id)})

# """
# 读取/生成镜架的预览图（商品介绍图）
# """
# def preview(request: HttpRequest):
# 	if request.method == 'GET':
# 		try:
# 			_id = int(json.loads(request.GET.get('id', "-1")))
# 		except:
# 			_id = -1
# 			print(request.GET.get('id', "-1"))

# 		if _id != -1:
# 			img = Image.open(get_image_path(_id))
# 			scale_factor = min(512/img.width, 512/img.height)
# 			img_ = img.resize((round(img.width*scale_factor), round(img.height*scale_factor)), Image.ANTIALIAS)
# 			img = Image.new('RGBA', (512, 512), 'white')
# 			img.paste(img_, ((512-img_.width)//2, (512-img_.height)//2))
# 		else:
# 			img = Image.new(mode="RGB", size=(256,256), color='gray')
# 		# _font = ImageFont.truetype("simsun.ttc", 24)
# 		# img = Image.new(mode="RGB", size=(256,256), color='gray')
# 		# if _id >= 0:
# 		# 	draw = ImageDraw.Draw(img)
# 		# 	draw.text((20, 20), "编号：" + str(_id), font=_font)
# 		# 	_entry = EyeglassFrameEntry.objects.filter(id=_id)
# 		# 	if len(_entry) > 0:
# 		# 		draw.text((20, 60), "品牌："+_entry[0].brand, font=_font)
# 		# 		draw.text((20, 100), "型号："+_entry[0].model_type, font=_font)
# 		# 		draw.text((20, 140), "材质："+_entry[0].material, font=_font)
# 		# 		styles = []
# 		# 		links = EyeglassFrameEntryStyle.objects.filter(entry=_entry[0])
# 		# 		if len(links) > 0:
# 		# 			styles = [style.style.style for style in links]
# 		# 		style_text = "，".join(styles)
# 		# 		draw.text((20, 180), "风格："+style_text[:7], font=_font)
# 		# 		draw.text((20, 220), "　　　"+style_text[7:], font=_font)
# 	else:
# 		img = Image.new(mode="RGB", size=(256,256), color='gray')
# 	response = HttpResponse(content_type="image/png")
# 	img.save(response, "PNG")
# 	return response



# """
# 读取单个镜架的信息（人脸端）
# """
# def details(request):
# 	if request.method == 'GET':
# 		try:
# 			_id = int(json.loads(request.GET.get('id', "-1")))
# 		except:
# 			_id = -1
# 			print(request.GET.get('id', "-1"))
# 		if _id >= 0:
# 			entry = EyeglassFrameEntry.objects.filter(id=_id)[0]
# 			return JsonResponse(data={"result": {
# 				"brand": entry.brand,
# 				"model_type": entry.model_type,
# 				"price": str(entry.price),
# 				"material": entry.material,
# 				"create-time": entry.create_time.strftime('%Y-%m-%d %H:%M:%S'),
# 				"update-time": entry.update_time.strftime('%Y-%m-%d %H:%M:%S')
# 			}})
# 	else:
# 		return JsonResponse(data={"result": None})


# """
# 生成一些镜架（人脸端）
# """
# def generate_testing_data_for_customer_ui(request):
# 	# 10个风格，7个品牌，每个品牌4个型号，5个售价，5个材质，共700个镜架，每个镜架随机三种风格
# 	random.seed(42)
# 	styles: List[EyeglassFrameEntry] = []
# 	for i in range(0, 10):
# 		style = EyeglassFrameStyleType()
# 		style.style = "风格" + str(i)
# 		style.save()
# 		styles.append(style)

# 	eyeglass_frames: List[EyeglassFrameEntry] = []
# 	eyeglass_frames_styles: List[List[EyeglassFrameEntry]] = []
# 	for brand_idx in range(0, 7):
# 		for model_type_idx in range(0, 4):
# 			for price_idx in range(0, 5):
# 				for material_idx in range(0, 5):
# 					entry = EyeglassFrameEntry()
# 					entry.brand = "品牌" + str(brand_idx)
# 					entry.model_type = str(brand_idx) + "-" + str(model_type_idx)
# 					entry.price = 800 + price_idx * 200
# 					entry.material = "材质" + str(material_idx)
# 					eyeglass_frames.append(entry)
# 					eyeglass_frames_styles.append(random.sample(styles, 3))

# 	assert len(eyeglass_frames) == 700, eyeglass_frames
# 	random.shuffle(eyeglass_frames)
# 	for eyeglass_frame in eyeglass_frames:
# 		eyeglass_frame.save()

# 	for i, styles in enumerate(eyeglass_frames_styles):
# 		for style in styles:
# 			link = EyeglassFrameEntryStyle()
# 			link.entry = eyeglass_frames[i]
# 			link.style = style
# 			link.save()

# 	return JsonResponse(data={"result": 'ok'})

# """
# 下面的代码用于转发后端的视频流，暂时用不到
# """
# # class VideoCamera(object):
# # 	def __init__(self):
# # 		self.video = cv2.VideoCapture(0)

# # 	def __del__(self):
# # 		self.video.release()

# # 	def get_frame(self):
# # 		success, image = self.video.read()
# # 		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
# # 		# so we must encode it into JPEG in order to correctly display the
# # 		# video stream.

# # 		frame_flip = cv2.flip(image,1)
# # 		ret, jpeg = cv2.imencode('.jpg', frame_flip)
# # 		return jpeg.tobytes()

# # def gen(camera):
# # 	while True:
# # 		frame = camera.get_frame()
# # 		yield (b'--frame\r\n'
# # 				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# # def video_feed(request):
# # 	return StreamingHttpResponse(gen(VideoCamera()),
# # 					content_type='multipart/x-mixed-replace; boundary=frame')

# def test_recommend(request):
# 	return JsonResponse(data={"result": recommend(24, "", 139.19, 12.39, 83.63, None)})

###################################################################################################################
###################################################################################################################
###################################################################################################################

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
保存新镜架并生成新的计算任务
"""
class UploadNewEyeglassFrameView(View):
	def post(self, request: HttpRequest):
		# 调用上传参数方法
		result = services.UploadNewEyeglassFrame(request)
		# 返回结果
		return result
	
"""
生成计算任务
"""
class GenerateCalculateTaskView(View):
	def post(self, request: HttpRequest):
		# 调用上传参数方法
		result = services.GenerateCalculateTask(request)
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
获取所有镜架计算状态
"""
class GetAllCalculateStatesView(View):
	def get(self, request: HttpRequest):
		# 调用查询计算状态的服务方法
		result = services.GetAllCalculateStates(request)
		# 返回结果
		return result


"""
获取镜架试戴和美化图片
"""
class GetEyeglassFrameTryonAndBeautifyView(View):
	def get(self, request: HttpRequest):
		# 调用查询镜架试戴和美化图片的服务方法
		result = services.GetEyeglassFrameTryonAndBeautify(request)
		# 返回结果
		return result


"""
上传人脸图片
"""
class UploadAIFaceView(View):
	def post(self, request: HttpRequest):
		# 调用上传人脸图片的服务方法
		result = services.UploadAIFace(request)
		# 返回结果
		return result

"""
上传处理后的镜架美化图
"""
class UploadProcessedBeautifyImageView(View):
	def post(self, request: HttpRequest):
		# 调用上传处理后的镜架美化图的服务方法
		result = services.UploadProcessedBeautifyImage(request)
		# 返回结果
		return result
	
"""
更新镜腿标注
"""
class UpdateAnnotationLegView(View):
	def post(self, request: HttpRequest):
		# 调用更新镜腿标注的服务方法
		result = services.UpdateAnnotationLeg(request)
		# 返回结果
		return result
	
"""
更新试戴模式
"""
class UpdateTryonModeView(View):
	def post(self, request: HttpRequest):
		# 调用更新试戴模式的服务方法
		result = services.UpdateTryonMode(request)
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
获取所有镜架形状
"""
class GetAllIsTransparenrView(View):
	def get(self, request: HttpRequest):
		# 调用查询所有镜架形状的服务方法
		result = services.GetAllIsTransparent(request)
		# 返回结果
		return result

"""
获取所有镜框类型
"""
class GetAllFrameTypesView(View):
	def get(self, request: HttpRequest):
		# 调用查询所有镜架形状的服务方法
		result = services.GetAllFrameTypes(request)
		# 返回结果
		return result

	

	

####################################################以下是用postman或者apifox执行的###############################################################
"""
添加镜架风格
"""
# def AddStyle(request: HttpRequest):
# 	if request.method == 'POST':
# 		style = request.POST.get('style', "")
# 		if style:
# 			styles = EyeglassFrameStyleType.objects.filter(style=style)
# 			if len(styles) == 0:
# 				style = EyeglassFrameStyleType(style=style)
# 				style.save()
# 				return JsonResponse(data={"result": "添加风格成功"})
# 			else:
# 				return JsonResponse(data={"result": "风格已存在"})
# 		else:
# 			return JsonResponse(data={"result": "风格不能为空"})
# 	else:
# 		return JsonResponse(data={"result": "请求方式错误"})
	
# def AddStyleList(request: HttpRequest):
# 	if request.method == 'POST':
# 		style_list = request.POST.getlist('style', [])
# 		for style in style_list:
# 			styles = EyeglassFrameStyleType.objects.filter(style=style)
# 			if len(styles) == 0:
# 				style = EyeglassFrameStyleType(style=style)
# 				style.save()
# 		return JsonResponse(data={"result": "添加风格成功"})
# 	else:
# 		return JsonResponse(data={"result": "请求方式错误"})

"""
添加镜架材质
"""
# def AddMaterial(request: HttpRequest):
# 	if request.method == 'POST':
# 		material = request.POST.get('material', "")
# 		if material:
# 			materials = EyeglassFrameMaterialType.objects.filter(material=material)
# 			if len(materials) == 0:
# 				material = EyeglassFrameMaterialType(material=material)
# 				material.save()
# 				return JsonResponse(data={"result": "添加材质成功"})
# 			else:
# 				return JsonResponse(data={"result": "材质已存在"})
# 		else:
# 			return JsonResponse(data={"result": "材质不能为空"})
# 	else:
# 		return JsonResponse(data={"result": "请求方式错误"})
	
# def AddMaterialList(request: HttpRequest):
# 	if request.method == 'POST':
# 		material_list = request.POST.getlist('material', [])
# 		for material in material_list:
# 			materials = EyeglassFrameMaterialType.objects.filter(material=material)
# 			if len(materials) == 0:
# 				material = EyeglassFrameMaterialType(material=material)
# 				material.save()
# 		return JsonResponse(data={"result": "添加材质成功"})
# 	else:
# 		return JsonResponse(data={"result": "请求方式错误"})
	

"""
添加镜架颜色
"""
# def AddColor(request: HttpRequest):
# 	if request.method == 'POST':
# 		color = request.POST.get('color', "")
# 		if color:
# 			colors = EyeglassFrameColorType.objects.filter(color=color)
# 			if len(colors) == 0:
# 				color = EyeglassFrameColorType(color=color)
# 				color.save()
# 				return JsonResponse(data={"result": "添加颜色成功"})
# 			else:
# 				return JsonResponse(data={"result": "颜色已存在"})
# 		else:
# 			return JsonResponse(data={"result": "颜色不能为空"})
# 	else:
# 		return JsonResponse(data={"result": "请求方式错误"})
	
# def AddColorList(request: HttpRequest):
# 	if request.method == 'POST':
# 		color_list = request.POST.getlist('color', [])
# 		for color in color_list:
# 			colors = EyeglassFrameColorType.objects.filter(color=color)
# 			if len(colors) == 0:
# 				color = EyeglassFrameColorType(color=color)
# 				color.save()
# 		return JsonResponse(data={"result": "添加颜色成功"})
# 	else:
# 		return JsonResponse(data={"result": "请求方式错误"})

"""
添加镜架形状
"""
# def AddShape(request: HttpRequest):
# 	if request.method == 'POST':
# 		shape = request.POST.get('shape', "")
# 		if shape:
# 			shapes = EyeglassFrameShapeType.objects.filter(shape=shape)
# 			if len(shapes) == 0:
# 				shape = EyeglassFrameShapeType(shape=shape)
# 				shape.save()
# 				return JsonResponse(data={"result": "添加形状成功"})
# 			else:
# 				return JsonResponse(data={"result": "形状已存在"})
# 		else:
# 			return JsonResponse(data={"result": "形状不能为空"})
# 	else:
# 		return JsonResponse(data={"result": "请求方式错误"})
	
# def AddShapeList(request: HttpRequest):
# 	if request.method == 'POST':
# 		shape_list = request.POST.getlist('shape', [])
# 		for shape in shape_list:
# 			shapes = EyeglassFrameShapeType.objects.filter(shape=shape)
# 			if len(shapes) == 0:
# 				shape = EyeglassFrameShapeType(shape=shape)
# 				shape.save()
# 		return JsonResponse(data={"result": "添加形状成功"})
# 	else:
# 		return JsonResponse(data={"result": "请求方式错误"})
















