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
from application.glass_recommendation.models import *
from application.glass_recommendation import services

"""
注册新用户
"""
class RegisterRecommendationUserView(View):
	def get(self, request: HttpRequest):
		# 调用注册新用户的服务方法
		result = services.RegisterRecommendationUser(request)
		# 返回结果
		return result

"""
保存新用户人脸图像和人脸扫描结果
"""
class SaveNewRecommendationUserFacialImageAndFacialScanResultView(View):
	def post(self, request: HttpRequest):
		# 调用保存新用户人脸图像和人脸扫描结果的服务方法
		result = services.SaveNewRecommendationUserFacialImageAndFacialScanResult(request)
		# 返回结果
		return result

"""
保存新用户基础信息、验光信息和镜片需求
"""
class SaveNewRecommendationUserBaseInfoAndOptometryAndLensView(View):
	def post(self, request: HttpRequest):
		# 调用保存新用户基础信息、验光信息和镜片需求的服务方法
		result = services.SaveNewRecommendationUserBaseInfoAndOptometryAndLens(request)
		# 返回结果
		return result














