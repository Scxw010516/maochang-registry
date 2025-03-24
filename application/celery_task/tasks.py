from celery import shared_task

import json
import cv2
import os
from time import sleep

from django.core.files.base import ContentFile
import numpy as np
from io import BytesIO
from PIL import Image

from utils import R, regular
from django.db import transaction
from django.core.files import File

from application.glass_management import models
from application.glass_management import forms

# 引入通用函数
from application.celery_task.services import (
    read_image_from_field, # 从数据库读取图片
    save_output_mask, # 保存mask
    save_output_images, # 保存images
    save_output_point,  # 保存point
    save_output_parameter, # 保存parameter
    save_output_size, # 保存size
    save_output_shape, # 保存shape
    delete_calc_task, # 删除重复任务
)

# 引入镜架计算模型
from .glass_detect.glasses import process,get_models
from .glass_detect.glasses import get_capture_images

@shared_task()
def test( sku):
    try:
        
        # 模拟处理过程
        sleep(10)

        print("执行计算任务：" + sku)
        # 删除重复任务
        delete_calc_task(sku)
        
        return {'status': 'SUCCESS', 'sku': sku}
    except Exception as e:
        print("计算任务失败：" + str(e))
        raise
@shared_task()
def calc(sku):
    """
    计算眼镜参数并保存计算结果
    """
    print("执行计算任务："+sku)
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
    EyeglassFrameImage_instance = (
            models.EyeglassFrameImage.objects.filter(entry = EyeglassFrameEntry_instance).first()
        )
    if not EyeglassFrameImage_instance:
        # 三视图不存在，更新计算状态为计算失败
        # 数据库事务处理
        with transaction.atomic():
            # 更新基本信息表 计算状态为 3 计算失败
            EyeglassFrameEntry_instance.pixel_measurement_state = 3
            EyeglassFrameEntry_instance.millimeter_measurement_state = 3
            EyeglassFrameEntry_instance.calculation_state = 3
            EyeglassFrameEntry_instance.coordinate_state = 3
            EyeglassFrameEntry_instance.image_mask_state = 3
            EyeglassFrameEntry_instance.image_seg_state = 3
            EyeglassFrameEntry_instance.image_beautify_state = 3 
            # 保存
            EyeglassFrameEntry_instance.save()
        return "计算失败：镜架三视图不存在"
    
    try:
        # 读取三视图
        up_image = read_image_from_field(EyeglassFrameImage_instance.topview)
        front_image = read_image_from_field(EyeglassFrameImage_instance.frontview)
        left_image = read_image_from_field(EyeglassFrameImage_instance.sideview)
        images = {"up": up_image, "front": front_image, "left": left_image}
        # images=get_capture_images(sku)
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

    except Exception as e:
        with transaction.atomic():
            # 更新基本信息表 计算状态为 3 计算失败
            EyeglassFrameEntry_instance.pixel_measurement_state = 3
            EyeglassFrameEntry_instance.millimeter_measurement_state = 3
            EyeglassFrameEntry_instance.calculation_state = 3
            EyeglassFrameEntry_instance.coordinate_state = 3
            EyeglassFrameEntry_instance.image_mask_state = 3
            EyeglassFrameEntry_instance.image_seg_state = 3
            EyeglassFrameEntry_instance.image_beautify_state = 3 
            # 保存
            EyeglassFrameEntry_instance.save()
        return "计算失败：计算参数失败"
    
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
        try:
            # 如果mask计算成功，保存mask；更新计算状态
            if output['mask']['state']: 
                save_output_mask(output['mask'], EyeglassFrameImage_instance)
                EyeglassFrameEntry_instance.image_mask_state = 2
            else:
                EyeglassFrameEntry_instance.image_mask_state = 3
        except Exception as e:
            EyeglassFrameEntry_instance.image_mask_state = 3
            print("mask处理失败:"+ e)

        """
        images处理
        """
        # 如果images计算成功，保存images；更新计算状态
        if output['image']['state']: 
            save_output_images(output['image'], EyeglassFrameImage_instance)
            EyeglassFrameEntry_instance.image_seg_state = 2
            EyeglassFrameEntry_instance.image_beautify_state = 2
        else:
            EyeglassFrameEntry_instance.image_seg_state = 3
            EyeglassFrameEntry_instance.image_beautify_state = 3

        """
        point处理: 镜架坐标数据 EyeglassFrameCoordinateForm
        """
        
        try:
            if output['point']['state']:
                save_output_point(output['point'], EyeglassFrameEntry_instance)
                # 更新计算状态
                EyeglassFrameEntry_instance.coordinate_state = 2
            else:
                # 处理镜架坐标数据缺失
               raise ValueError("镜架坐标数据缺失")
        except Exception as e:
            EyeglassFrameEntry_instance.coordinate_state = 3
            print("point处理失败:" + str(e))

        """
        parameter处理: 镜架像素测量数据 EyeglassFramePixelMeasurement
        """
        try:
            if output['parameter']['state']:
                save_output_parameter(output['parameter'], EyeglassFrameEntry_instance)
                # 更新计算状态
                EyeglassFrameEntry_instance.pixel_measurement_state = 2
            else:
                # 处理镜架像素测量数据缺失
                raise ValueError("镜架像素测量数据缺失")
        except Exception as e:
            EyeglassFrameEntry_instance.pixel_measurement_state = 3
            print("parameter处理失败:" + str(e))
        
        """
        size处理: 镜架毫米测量数据 EyeglassFrameMillimeterMeasurement
        """
        try:
            if output['size']['state']:
                save_output_size(output['size'], EyeglassFrameEntry_instance)
                # 更新计算状态
                EyeglassFrameEntry_instance.millimeter_measurement_state = 2
            else:
                # 处理镜架毫米测量数据缺失
                raise ValueError("镜架毫米测量数据缺失")
        except Exception as e:
            EyeglassFrameEntry_instance.millimeter_measurement_state = 3
            print("size处理失败:" + str(e))

        """
        shape处理: 镜架计算数据 EyeglassFrameCalculation
        """
        try:
            if output['shape']['state']:
                save_output_shape(output['shape'], EyeglassFrameEntry_instance)
                # 更新计算状态
                EyeglassFrameEntry_instance.calculation_state = 2
            else:
                # 处理镜架计算数据缺失
                raise ValueError("镜架计算数据缺失")
        except Exception as e:
            EyeglassFrameEntry_instance.calculation_state = 3
            print("shape处理失败:" + str(e))

        # 删除重复任务
        delete_calc_task(sku)
        # 保存镜架基本信息表
        EyeglassFrameEntry_instance.save()  
        print("镜架基本信息表已保存")  
    # 返回
    print('计算任务执行完毕：'+sku)
    return sku


# todo：添加定时添加任务功能