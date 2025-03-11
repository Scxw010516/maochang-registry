from celery import shared_task

import json
import cv2
import os
import tempfile

from django.core.files.base import ContentFile
import numpy as np
from io import BytesIO
from PIL import Image

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
    # #创建连接
    # conn = connection
    # conn._thread_ident = get_ident()
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

        # 保存镜架基本信息表
    
    EyeglassFrameEntry_instance.save()
    
    #关闭本线程全部连接
    # connections.close_all()
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

def save_output_images(output_images, instance):
    """
    将process输出的图片保存到Django模型的ImageField中

    Args:
    output:process函数的输出字曲
    instance:Django模型实例
    """
    # 需要保存的图片字段
    image_fields = {
        'frontview_seg': output_images['data']['frontview_seg'],
        'sideview_seg': output_images['data']['sideview_seg'],
        'frontview_beautify': output_images['data']['frontview_beautify'],
        'sideview_beautify': output_images['data']['sideview_beautify']
    }

    for field_name, image_array in image_fields.items():
        if image_array is not None:
            #创建临时文件
            temp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            try:
                # 保存numpy array为图片文件
                cv2.imwrite(temp.name, image_array)
                # 打开临时文件并保存到ImageField
                with open(temp.name, 'rb')as f:
                    # 模型的字段名与image fields的key相同
                    getattr(instance,field_name).save(
                        f'{field_name}.png' ,
                        File(f),
                        save=False
                    )
            finally:
                # 清理临时文件
                temp.close()
                os.unlink(temp.name)
    # 保存模型实例
    instance.save()

def save_output_point(output_point, entry_instance):
    # 查询镜架坐标数据表实例
    EyeglassFrameCoordinate_instance = models.EyeglassFrameCoordinate.objects.filter(entry=EyeglassFrameEntry_instance).first()
    if not EyeglassFrameCoordinate_instance:
        # 不存在镜架坐标数据表实例，则创建
        form_EyeglassFrameCoordinate = (
            forms.EyeglassFrameCoordinateForm(
                output_point['data']
            )
        )
    else:
        # 存在镜架坐标数据表实例，则更新
        form_EyeglassFrameCoordinate = (
            forms.EyeglassFrameCoordinateForm(
                output_point['data'],
                instance=EyeglassFrameCoordinate_instance
            )
        )
    if form_EyeglassFrameCoordinate.is_valid():
        # 构建并保存镜架坐标数据表数据库实例
        EyeglassFrameCoordinate_instance = (
            form_EyeglassFrameCoordinate.save(commit=False)
        )
        # 关联镜架基本信息表外键
        EyeglassFrameCoordinate_instance.entry = entry_instance
        EyeglassFrameCoordinate_instance.save()
    else:
        raise ValueError("镜架坐标数据表表单验证失败")

def save_output_parameter(output_parameter, entry_instance):
    # 数据位数处理：保留到小数点后四位
    for key in output_parameter['data']:
        output_parameter['data'][key] = round(output_parameter['data'][key], 4)
    # 查询镜架像素测量数据表实例
    EyeglassFramePixelMeasurement_instance = models.EyeglassFramePixelMeasurement.objects.filter(entry=entry_instance).first()
    if not EyeglassFramePixelMeasurement_instance:
        # 不存在镜架像素测量数据表实例，则创建
        form_EyeglassFramePixelMeasurement = (
            forms.EyeglassFramePixelMeasurementForm(
                output_parameter['data']
            )
        )
    else:
        # 存在镜架像素测量数据表实例，则更新
        form_EyeglassFramePixelMeasurement = (
            forms.EyeglassFramePixelMeasurementForm(
                output_parameter['data'],
                instance=EyeglassFramePixelMeasurement_instance
            )
        )
    if form_EyeglassFramePixelMeasurement.is_valid():
        # 构建并保存镜架像素测量数据表数据库实例
        EyeglassFramePixelMeasurement_instance = (
            form_EyeglassFramePixelMeasurement.save(commit=False)
        )
        # 关联镜架基本信息表外键
        EyeglassFramePixelMeasurement_instance.entry = entry_instance
        EyeglassFramePixelMeasurement_instance.save()
    else:
        raise ValueError("镜架像素测量数据表表单验证失败")

def save_output_size(output_size, entry_instance):
    # 数据位数处理：保留到小数点后四位
    for key in output_size['data']:
        output_size['data'][key] = round(output_size['data'][key], 4)
    # 查询镜架毫米测量数据表实例
    EyeglassFrameMillimeterMeasurement_instance = models.EyeglassFrameMillimeterMeasurement.objects.filter(entry=entry_instance).first()
    if not EyeglassFrameMillimeterMeasurement_instance:
        # 不存在镜架毫米测量数据表实例，则创建
        form_EyeglassFrameMillimeterMeasurement = (
            forms.EyeglassFrameMillimeterMeasurementForm(
                output_size['data']
            )
        )
    else:
        # 存在镜架毫米测量数据表实例，则更新
        form_EyeglassFrameMillimeterMeasurement = (
            forms.EyeglassFrameMillimeterMeasurementForm(
                output_size['data'],
                instance=EyeglassFrameMillimeterMeasurement_instance
            )
        )
    if form_EyeglassFrameMillimeterMeasurement.is_valid():
        # 构建并保存镜架毫米测量数据表数据库实例
        EyeglassFrameMillimeterMeasurement_instance = (
            form_EyeglassFrameMillimeterMeasurement.save(commit=False)
        )
        # 关联镜架基本信息表外键
        EyeglassFrameMillimeterMeasurement_instance.entry = entry_instance
        EyeglassFrameMillimeterMeasurement_instance.save()
    else:
        raise ValueError("镜架毫米测量数据表表单验证失败")

def save_output_shape(output_shape, entry_instance):
    # 数据位数处理：保留到小数点后四位
    for key in output_shape['data']:
        if key != 'frame_size':
            output_shape['data'][key] = round(output_shape['data'][key], 4)
    # 查询镜架计算数据表实例
    EyeglassFrameCalculation_instance = models.EyeglassFrameCalculation.objects.filter(entry=entry_instance).first()
    if not EyeglassFrameCalculation_instance:
        # 不存在镜架计算数据表实例，则创建
        form_EyeglassFrameCalculation = (
            forms.EyeglassFrameCalculationForm(
                output_shape['data']
            )
        )
    else:
        # 存在镜架计算数据表实例，则更新
        form_EyeglassFrameCalculation = (
            forms.EyeglassFrameCalculationForm(
                output_shape['data'],
                instance=EyeglassFrameCalculation_instance
            )
        )
    if form_EyeglassFrameCalculation.is_valid():
        # 构建并保存镜架计算数据表数据库实例
        EyeglassFrameCalculation_instance = (
            form_EyeglassFrameCalculation.save(commit=False)
        )
        # 关联镜架基本信息表外键
        EyeglassFrameCalculation_instance.entry = entry_instance
        EyeglassFrameCalculation_instance.save()
    else:
        raise ValueError("镜架计算数据表表单验证失败")

def read_image_from_field(image_field):
    """从Django的ImageField中读取图像并转换为OpenCV格式"""
    if not image_field:
        return None
    
    # 打开图像文件
    with image_field.open() as f:
        # 读取文件内容到内存中
        image_data = f.read()
    
    # 使用PIL读取图像
    pil_image = Image.open(BytesIO(image_data))
    
    # 转换为OpenCV格式
    open_cv_image = np.array(pil_image)
    # 如果图像是灰度图，则转换为RGB
    if len(open_cv_image.shape) == 2:
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_GRAY2BGR)
    else:
        # 转换为BGR格式（OpenCV默认）
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    return open_cv_image


# todo：添加定时添加任务功能