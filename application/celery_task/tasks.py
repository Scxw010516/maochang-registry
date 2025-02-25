from celery import shared_task

import json
import cv2
import os
# import tempfile

from django.core.files.base import ContentFile
import numpy as np
from io import BytesIO

from utils import R, regular
from django.db import connection,connections
from eventlet.green.thread import get_ident
from django.db import transaction
from django.core.files import File

from application.glass_management import models
from application.glass_management import forms

# 引入镜架计算模型
from .glass_detect.glasses import process,get_models
from .glass_detect.glasses import get_capture_images



@shared_task
def calc(sku):
    """
    计算眼镜参数并保存计算结果
    """
    #创建连接
    conn = connection
    conn._thread_ident = get_ident()
    print("连接已建立")
    # 查询镜架基本信息表
    EyeglassFrameEntry_instance = (
            models.EyeglassFrameEntry.objects.filter(sku=sku).first()
        )
    if not EyeglassFrameEntry_instance:
        # 镜架基本信息表不存在
       return  "计算失败：镜架基本信息表不存在"
            
    """
    更新计算状态为计算中
    """
    # 数据库事务处理
    with transaction.atomic():
        # 更新基本信息表 计算状态为 1 计算中
        EyeglassFrameEntry_instance.pixel_measurement_state = 1
        EyeglassFrameEntry_instance.millimeter_measurement_state = 1
        EyeglassFrameEntry_instance.calculation_state = 1
        EyeglassFrameEntry_instance.coordinate_state = 1
        EyeglassFrameEntry_instance.image_mask_state = 1
        EyeglassFrameEntry_instance.image_seg_state = 1
        EyeglassFrameEntry_instance.image_beautify_state = 1 
        # 保存
        EyeglassFrameEntry_instance.save()

    """
    计算参数
    """
    # 获取镜架三视图路径
    images = get_capture_images("201300053024730500")
    EyeglassFrameImage_instance = models.EyeglassFrameImage.objects.filter(entry=EyeglassFrameEntry_instance).first()
    if not EyeglassFrameImage_instance:
        EyeglassFrameImage_instance = models.EyeglassFrameImage.objects.create(entry = EyeglassFrameEntry_instance)
        
    # EyeglassFrameImage_instance = (
    #         models.EyeglassFrameImage.objects.filter(entry = EyeglassFrameEntry_instance).first()
    #     )
    # if not EyeglassFrameImage_instance:
    #     # 三视图不存在，更新计算状态为计算失败
    #     # 数据库事务处理
    #     with transaction.atomic():
    #         # 更新基本信息表 计算状态为 3 计算失败
    #         EyeglassFrameEntry_instance.pixel_measurement_state = 3
    #         EyeglassFrameEntry_instance.millimeter_measurement_state = 3
    #         EyeglassFrameEntry_instance.calculation_state = 3
    #         EyeglassFrameEntry_instance.coordinate_state = 3
    #         EyeglassFrameEntry_instance.image_mask_state = 3
    #         EyeglassFrameEntry_instance.image_seg_state = 3
    #         EyeglassFrameEntry_instance.image_beautify_state = 3 
    #         # 保存
    #         EyeglassFrameEntry_instance.save()
    #     return "计算失败：镜架三视图不存在"

    # up_image_path = EyeglassFrameImage_instance.topview
    # front_image_path = EyeglassFrameImage_instance.frontview
    # left_image_path = EyeglassFrameImage_instance.sideview
    # # 读取三视图
    # up_image = cv2.imread(f"{up_image_path}")
    # front_image = cv2.imread(f"{front_image_path}")
    # left_image = cv2.imread(f"{left_image_path}")
    # images = {"up": up_image, "front": front_image, "left": left_image}
    # 读取模型
    calc_models = get_models()
    # 设置计算参数
    frame = EyeglassFrameEntry_instance.frame_type # 获取镜架框架类型
    material = EyeglassFrameEntry_instance.material # 获取镜架材质
    transparent = EyeglassFrameEntry_instance.is_transparent # 获取镜架透明度
    options = {
        "types": {
            "frame": frame, # 对应EyeglassFrameEntry表的frame_type
            "material": material, # 对应EyeglassFrameEntry表的material
            "transparent": transparent, # 对应EyeglassFrameEntry表的is_transparent
            "special": False, # 默认为False
        }
    }
    # 计算参数
    output = process(images, calc_models, options)
    print(output)
    """
    保存计算结果: mask images point parameter size shape
    数据表：镜架像素测量数据，镜架毫米测量数据，镜架计算数据，镜架坐标数据，镜架图片数据
    镜架基本信息表：更新计算状态
    """
    # 数据库事务处理
    with transaction.atomic():
        """
        mask处理
        """
        # 如果mask计算成功，保存mask；更新计算状态
        if output['mask']['state']: 
            save_output_mask(output['mask'], EyeglassFrameImage_instance)
            EyeglassFrameEntry_instance.image_mask_state = 2
        else:
            EyeglassFrameEntry_instance.image_mask_state = 3

        # """
        # images处理
        # """
        # # 如果images计算成功，保存images；更新计算状态
        # if output['image']['state']: 
        #     save_output_images(output['image'], EyeglassFrameImage_instance)
        #     EyeglassFrameEntry_instance.image_seg_state = 2
        #     EyeglassFrameEntry_instance.image_beautify_state = 2
        # else:
        #     EyeglassFrameEntry_instance.image_seg_state = 3
        #     EyeglassFrameEntry_instance.image_beautify_state = 3

        # """
        # point处理: 镜架坐标数据 EyeglassFrameCoordinateForm
        # """
        # if output['point']['state']:
        #     # 创建镜架坐标数据表实例，关联镜架基本信息表外键
        #     form_EyeglassFrameCoordinate = (
        #         forms.EyeglassFrameCoordinateForm(
        #             output['point']['data']+{"entry": EyeglassFrameEntry_instance}
        #         )
        #     )
        #     if form_EyeglassFrameCoordinate.is_valid():
        #         # 构建并保存镜架坐标数据表数据库实例
        #         EyeglassFrameCoordinate_instance = (
        #             form_EyeglassFrameCoordinate.save()
        #         )
        #         # 更新计算状态
        #         EyeglassFrameEntry_instance.coordinate_state = 2
        #     else:
        #         # 处理镜架坐标数据表表单验证失败的情况
        #         EyeglassFrameEntry_instance.coordinate_state = 3
        # else:
        #     # 处理镜架坐标数据表表单验证失败的情况
        #     EyeglassFrameEntry_instance.coordinate_state = 3

        # """
        # parameter处理: 镜架像素测量数据 EyeglassFramePixelMeasurement
        # """
        # if output['parameter']['state']:
        #     # 创建镜架像素测量数据表实例，关联镜架基本信息表外键
        #     form_EyeglassFramePixelMeasurement = (
        #         forms.EyeglassFramePixelMeasurementForm(
        #             output['parameter']['data']+{"entry": EyeglassFrameEntry_instance}
        #         )
        #     )
        #     if form_EyeglassFramePixelMeasurement.is_valid():
        #         # 构建并保存镜架坐标数据表数据库实例
        #         EyeglassFramePixelMeasurement_instance = (
        #             form_EyeglassFramePixelMeasurement.save()
        #         )
        #         # 更新计算状态
        #         EyeglassFrameEntry_instance.pixel_measurement_state = 2
        #     else:
        #         # 处理镜架坐标数据表表单验证失败的情况
        #         EyeglassFrameEntry_instance.pixel_measurement_state = 3
        # else:
        #     # 处理镜架坐标数据表表单验证失败的情况
        #     EyeglassFrameEntry_instance.pixel_measurement_state = 3
        
        # """
        # size处理: 镜架毫米测量数据 EyeglassFrameMillimeterMeasurement
        # """
        # if output['size']['state']:
        #     # 创建镜架毫米测量数据表实例，关联镜架基本信息表外键
        #     form_EyeglassFrameMillimeterMeasurement = (
        #         forms.EyeglassFrameMillimeterMeasurementForm(
        #             output['size']['data']+{"entry": EyeglassFrameEntry_instance}
        #         )
        #     )
        #     if  form_EyeglassFrameCoordinate.is_valid():
        #         # 构建并保存镜架坐标数据表数据库实例
        #         EyeglassFrameMillimeterMeasurement_instance = (
        #             form_EyeglassFrameMillimeterMeasurement.save()
        #         )
        #         # 更新计算状态
        #         EyeglassFrameEntry_instance.millimeter_measurement_state = 2
        #     else:
        #         # 处理镜架坐标数据表表单验证失败的情况
        #         EyeglassFrameEntry_instance.millimeter_measurement_state = 3
        # else:
        #     # 处理镜架坐标数据表表单验证失败的情况
        #     EyeglassFrameEntry_instance.millimeter_measurement_state = 3
        

        # """
        # shape处理: 镜架计算数据 EyeglassFrameCalulation
        # """
        # if output['shape']['state']:
        #     # 创建镜架计算数据表实例，关联镜架基本信息表外键
        #     form_EyeglassFrameCalculation = (
        #         forms.EyeglassFrameCalculationForm(
        #             output['shape']['data']+{"entry": EyeglassFrameEntry_instance}
        #         )
        #     )
        #     if form_EyeglassFrameCalculation.is_valid():
        #         # 构建并保存镜架计算数据表数据库实例
        #         EyeglassFrameCalculation_instance = (
        #             form_EyeglassFrameCalculation.save()
        #         )
        #         # 更新计算状态
        #         EyeglassFrameEntry_instance.calculation_state = 2
        #     else:
        #         # 处理镜架计算数据表表单验证失败的情况
        #         EyeglassFrameEntry_instance.calculation_state = 3
        # else:
        #     # 处理镜架计算数据表表单验证失败的情况
        #     EyeglassFrameEntry_instance.calculation_state = 3

        # 保存镜架基本信息表
        EyeglassFrameEntry_instance.save()
    
    #关闭本线程全部连接
    connections.close_all()
    print("连接已关闭")
    # 返回
    print(sku)
    print('执行完毕')
    return sku


# def process_and_save(image_np, model_instance):
#     """处理OpenCV数组并存储到Django模型的ImageField
    
#     Args:
#         image_np: OpenCV格式的numpy数组 (H x W x C)
#         model_instance: Django模型实例
#     """
#     # 内存编码阶段
#     retval, buffer = cv2.imencode('.png', image_np)
#     if not retval:
#         raise RuntimeError("图像编码失败")

#     # 内存流转换
#     in_memory_file = BytesIO(buffer.tobytes())
    
#     # 构建存储对象
#     content_file = ContentFile(in_memory_file.getvalue())
    
#     # 数据库存储
#     filename = f"processed_{model_instance.id}.png" # 这里的文件名随便啥，只要是png结尾，因为下一步存数据库的时候，会被upload_to的文件名逻辑覆盖掉
#     model_instance.result_image.save(filename, content_file)
    
#     # 内存清理
#     in_memory_file.close()
#     del buffer, content_file
def save_output_mask(output_mask, instance):
    """
    保存mask 
    """
    # 需要保存的图片字段
    mask_fields = {
        'frame': output_mask['data']['frame'],
        'lens': output_mask['data']['lens'],
        'templeWf': output_mask['data']['templeWf'],
        'nose': output_mask['data']['nose'],
        'front': output_mask['data']['front'],
    }

    for field_name, mask_array in mask_fields.items():
        if mask_array is not None:
            """处理OpenCV数组并存储到Django模型的ImageField
    
            Args:
                image_np: OpenCV格式的numpy数组 (H x W x C)
                model_instance: Django模型实例
            """
            # 内存编码阶段
            retval, buffer = cv2.imencode('.png', mask_array)
            if not retval:
                raise RuntimeError("图像编码失败")

            # 内存流转换
            in_memory_file = BytesIO(buffer.tobytes())
            
            # 构建存储对象
            content_file = ContentFile(in_memory_file.getvalue())
            
            # 数据库存储
            filename = f"processed_{instance.id}.png" # 这里的文件名随便啥，只要是png结尾，因为下一步存数据库的时候，会被upload_to的文件名逻辑覆盖掉
            getattr(instance,field_name).save(filename, content_file)
            
            # 内存清理
            in_memory_file.close()
            del buffer, content_file

    # 保存模型实例
    instance.save()
    return output_mask

# def save_output_images(output_images, instance):
#     """
#     将process输出的图片保存到Django模型的ImageField中

#     Args:
#     output:process函数的输出字曲
#     instance:Django模型实例
#     """
#     # 需要保存的图片字段
#     image_fields = {
#         'frontview_seg': output_images['data']['frontview_seg'],
#         'sideview_seg': output_images['data']['sideview_seg'],
#         'frontview_beautify': output_images['data']['frontview_beautify'],
#         'sideview_beautify': output_images['data']['sideview_beautify']
#     }

#     for field_name, image_array in image_fields.items():
#         if image_array is not None:
#             #创建临时文件
#             temp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
#             try:
#                 # 保存numpy array为图片文件
#                 cv2.imwrite(temp.name, image_array)
#                 # 打开临时文件并保存到ImageField
#                 with open(temp.name, 'rb')as f:
#                     # 模型的字段名与image fields的key相同
#                     getattr(instance,field_name).save(
#                         f'{field_name}.png' ,
#                         File(f),
#                         save=False
#                     )
#             finally:
#                 # 清理临时文件
#                 temp.close()
#                 os.unlink(temp.name)
#     # 保存模型实例
#     instance.save()

# todo：添加定时添加任务功能