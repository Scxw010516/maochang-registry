from django.contrib import admin

# Register your models here.
from application.glass_management.models import (
    # EyeglassFrameMaterialType,
    # EyeglassFrameColorType,
    # EyeglassFrameShapeType,
    EyeglassFrameEntry,
    EyeglassFrameMillimeterMeasurement,
    EyeglassFramePixelMeasurement,
    EyeglassFrameCalulation,
    EyeglassFrameCoordinate,
    EyeglassFrameImage
)

# admin.site.register(EyeglassFrameMaterialType) # 镜架材质类型表
# admin.site.register(EyeglassFrameColorType) # 镜架颜色类型表
# admin.site.register(EyeglassFrameShapeType) # 镜架形状类型表
admin.site.register(EyeglassFrameEntry) # 镜架基本信息表
# admin.site.register(EyeglassFrameDataFromExcel) # 注释掉此行，因为models.py中未定义此模型
admin.site.register(EyeglassFrameMillimeterMeasurement) # 镜架毫米测量数据
admin.site.register(EyeglassFramePixelMeasurement) # 镜架像素测量数据
admin.site.register(EyeglassFrameCalulation) # 镜架计算数据
admin.site.register(EyeglassFrameCoordinate) # 镜架坐标数据
admin.site.register(EyeglassFrameImage) # 镜架图片数据
