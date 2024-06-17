from django.contrib import admin

# Register your models here.
from application.glass_recommendation.models import RecommendationUser # 推荐客户端用户表
from application.glass_recommendation.models import RecommendationUserBaseInfo # 推荐客户端用户基础信息表
from application.glass_recommendation.models import RecommendationUserFacialImage # 推荐客户端用户人脸图像表
from application.glass_recommendation.models import RecommendationUserOptometry # 推荐客户端用户验光信息表
from application.glass_recommendation.models import RecommendationUserLens # 推荐客户端用户镜片需求表
from application.glass_recommendation.models import RecommendationUserFacialScanResult # 推荐客户端用户人脸扫描结果表
from application.glass_recommendation.models import EyeglassFrameRecommendationRequest # 镜架推荐请求表

admin.site.register(RecommendationUser) # 推荐客户端用户表
admin.site.register(RecommendationUserBaseInfo) # 推荐客户端用户基础信息表
admin.site.register(RecommendationUserFacialImage) # 推荐客户端用户人脸图像表
admin.site.register(RecommendationUserOptometry) # 推荐客户端用户验光信息表
admin.site.register(RecommendationUserLens) # 推荐客户端用户镜片需求表
admin.site.register(RecommendationUserFacialScanResult) # 推荐客户端用户人脸扫描结果表
admin.site.register(EyeglassFrameRecommendationRequest) # 镜架推荐请求表
