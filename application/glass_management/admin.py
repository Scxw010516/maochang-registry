from django.contrib import admin

# Register your models here.
from application.glass_management.models import EyeglassFrameMaterialType # 镜架材质类型表
from application.glass_management.models import EyeglassFrameColorType  # 镜架颜色类型表
from application.glass_management.models import EyeglassFrameShapeType  # 镜架形状类型表
from application.glass_management.models import EyeglassFrameEntry  # 镜架基本信息表
from application.glass_management.models import EyeglassFrameStyleType  # 镜架风格类型表
from application.glass_management.models import EyeglassFrameEntryStyle # 镜架基本信息与风格关联表
from application.glass_management.models import EyeglassFrameDetectionResult # 镜架扫描结果表

admin.site.register(EyeglassFrameMaterialType) # 镜架材质类型表
admin.site.register(EyeglassFrameColorType) # 镜架颜色类型表
admin.site.register(EyeglassFrameShapeType) # 镜架形状类型表
admin.site.register(EyeglassFrameEntry) # 镜架基本信息表
admin.site.register(EyeglassFrameStyleType) # 镜架风格类型表 
admin.site.register(EyeglassFrameEntryStyle) # 镜架基本信息与风格关联表
admin.site.register(EyeglassFrameDetectionResult) # 镜架检测结果表

