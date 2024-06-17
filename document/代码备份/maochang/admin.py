from django.contrib import admin

# Register your models here.
from application.maochang.models import EyeglassFrameMaterialType # 镜架材质类型表
from application.maochang.models import EyeglassFrameColorType  # 镜架颜色类型表
from application.maochang.models import EyeglassFrameShapeType  # 镜架形状类型表
from application.maochang.models import EyeglassFrameEntry  # 镜架基本信息表
from application.maochang.models import EyeglassFrameStyleType  # 镜架风格类型表
from application.maochang.models import EyeglassFrameEntryStyle # 镜架基本信息与风格关联表
from application.maochang.models import EyeglassFrameDetectionResult # 镜架扫描结果表
from application.maochang.models import RecommendationUser # 推荐客户端用户表
from application.maochang.models import RecommendationUserBaseInfo # 推荐客户端用户基础信息表
from application.maochang.models import RecommendationUserFacialImage # 推荐客户端用户人脸图像表
from application.maochang.models import RecommendationUserOptometry # 推荐客户端用户验光信息表
from application.maochang.models import RecommendationUserLens # 推荐客户端用户镜片需求表
from application.maochang.models import RecommendationUserFacialScanResult # 推荐客户端用户人脸扫描结果表
from application.maochang.models import EyeglassFrameRecommendationRequest # 镜架推荐请求表

admin.site.register(EyeglassFrameMaterialType) # 镜架材质类型表
admin.site.register(EyeglassFrameColorType) # 镜架颜色类型表
admin.site.register(EyeglassFrameShapeType) # 镜架形状类型表
admin.site.register(EyeglassFrameEntry) # 镜架基本信息表
admin.site.register(EyeglassFrameStyleType) # 镜架风格类型表 
admin.site.register(EyeglassFrameEntryStyle) # 镜架基本信息与风格关联表
admin.site.register(EyeglassFrameDetectionResult) # 镜架检测结果表
admin.site.register(RecommendationUser) # 推荐客户端用户表
admin.site.register(RecommendationUserBaseInfo) # 推荐客户端用户基础信息表
admin.site.register(RecommendationUserFacialImage) # 推荐客户端用户人脸图像表
admin.site.register(RecommendationUserOptometry) # 推荐客户端用户验光信息表
admin.site.register(RecommendationUserLens) # 推荐客户端用户镜片需求表
admin.site.register(RecommendationUserFacialScanResult) # 推荐客户端用户人脸扫描结果表
admin.site.register(EyeglassFrameRecommendationRequest) # 镜架推荐请求表
