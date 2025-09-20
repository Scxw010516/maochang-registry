from celery import shared_task

import json
import cv2
import requests
import os

from django.core.files.base import ContentFile
import numpy as np
from io import BytesIO
from PIL import Image

from utils import R, regular
from django.db import transaction
from django.core.files import File
from config.env import TRYON_URL
from application.glass_management import models
from application.glass_management import forms
# 引入通用函数
import application.celery_task.services as services

# 引入镜架计算模型
from .glass_detect.glasses import process, get_models
from .glass_detect.config import default_options
# from .glass_detect.glasses import get_capture_images



"""
计算眼镜参数并保存计算结果

args:
    sku: str, 镜架SKU
"""

# 重试四次，第四次不进行业务逻辑，仅失败处理
@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 4, 'countdown': 60})
def calc(self, sku):
    """
    计算眼镜参数并保存计算结果

    Args:
        sku: str, 镜架SKU
    """
    print(f"执行计算任务：{sku}, 任务ID: {self.request.id}, 重试次数: {self.request.retries}")

    existing_task_id = services.TaskManager.search_calc_task(sku)
    if existing_task_id:
        for task_id in existing_task_id:
            if task_id != self.request.id:
                print(f"发现重复任务 {task_id}，正在删除...")
                services.TaskManager.delete_calc_task(task_id)      

    # 查询镜架基本信息表
    EyeglassFrameEntry_instance = models.EyeglassFrameEntry.objects.filter(sku=sku,is_delete=False).first()
    if not EyeglassFrameEntry_instance:
        # 镜架基本信息表不存在
        error_msg = f"计算失败：镜架基本信息表不存在，SKU: {sku}"
        print(error_msg)
        return error_msg
    
    # """
    # 发送镜架参数
    # """
    # # 获取token
        
    # update.delay_on_commit(sku)

    # return

    if self.request.retries >= 3: # 第四次重试，则取消任务
        EyeglassFrameEntry_instance.pixel_measurement_state = 3
        EyeglassFrameEntry_instance.millimeter_measurement_state = 3
        EyeglassFrameEntry_instance.calculation_state = 3
        EyeglassFrameEntry_instance.coordinate_state = 3
        EyeglassFrameEntry_instance.image_mask_state = 3
        EyeglassFrameEntry_instance.image_seg_state = 3
        EyeglassFrameEntry_instance.image_beautify_state = 3
        # 保存
        EyeglassFrameEntry_instance.save()
        print("以达到最大重试次数，计算失败")
        return 
    
    # 🔧 重试时的状态恢复逻辑
    initial_states = None
    if self.request.retries > 0:
        print(f"任务重试中，正在恢复初始状态...")
        # 记录当前状态作为"失败前状态"，用于日志
        current_states = {
            'pixel_measurement_state': EyeglassFrameEntry_instance.pixel_measurement_state,
            'millimeter_measurement_state': EyeglassFrameEntry_instance.millimeter_measurement_state,
            'calculation_state': EyeglassFrameEntry_instance.calculation_state,
            'coordinate_state': EyeglassFrameEntry_instance.coordinate_state,
            'image_mask_state': EyeglassFrameEntry_instance.image_mask_state,
            'image_seg_state': EyeglassFrameEntry_instance.image_seg_state,
            'image_beautify_state': EyeglassFrameEntry_instance.image_beautify_state,
        }
        print(f"重试前状态: {current_states}")

        # 恢复到初始状态（0=待计算）
        with transaction.atomic():
            EyeglassFrameEntry_instance.pixel_measurement_state = 0
            EyeglassFrameEntry_instance.millimeter_measurement_state = 0
            EyeglassFrameEntry_instance.calculation_state = 0
            EyeglassFrameEntry_instance.coordinate_state = 0
            EyeglassFrameEntry_instance.image_mask_state = 0
            EyeglassFrameEntry_instance.image_seg_state = 0
            EyeglassFrameEntry_instance.image_beautify_state = 0
            EyeglassFrameEntry_instance.is_update = 0
            EyeglassFrameEntry_instance.save()
        print("状态已恢复到初始状态(0)")
    else:
        # 首次执行，记录初始状态
        initial_states = {
            'pixel_measurement_state': EyeglassFrameEntry_instance.pixel_measurement_state,
            'millimeter_measurement_state': EyeglassFrameEntry_instance.millimeter_measurement_state,
            'calculation_state': EyeglassFrameEntry_instance.calculation_state,
            'coordinate_state': EyeglassFrameEntry_instance.coordinate_state,
            'image_mask_state': EyeglassFrameEntry_instance.image_mask_state,
            'image_seg_state': EyeglassFrameEntry_instance.image_seg_state,
            'image_beautify_state': EyeglassFrameEntry_instance.image_beautify_state,
        }
        print(f"首次执行，记录初始状态: {initial_states}")

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
    entry_id = EyeglassFrameEntry_instance.id  # 获取镜架基本信息表ID
    # 获取镜架三视图路径
    EyeglassFrameImage_instance = models.EyeglassFrameImage.objects.filter(entry_id=entry_id,is_delete=False).first()
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
        print(f"计算失败：镜架三视图不存在，SKU: {sku}")
        return "计算失败：镜架三视图不存在"

    try:
        # 读取三视图
        up_image = services.read_image_from_field(EyeglassFrameImage_instance.topview)
        front_image = services.read_image_from_field(EyeglassFrameImage_instance.frontview)
        left_image = services.read_image_from_field(EyeglassFrameImage_instance.sideview)
        images = {"up": up_image, "front": front_image, "left": left_image}
        # images=services.get_capture_images(sku)
        # 读取模型
        calc_models = get_models()
        # 设置计算参数
        frame = EyeglassFrameEntry_instance.frame_type  # 获取镜架框架类型
        material = EyeglassFrameEntry_instance.material  # 获取镜架材质
        transparent = EyeglassFrameEntry_instance.is_transparent  # 获取镜架透明度
        options = default_options
        options["types"] = {
            "frame": frame,  # 对应EyeglassFrameEntry表的frame_type
            "material": material,  # 对应EyeglassFrameEntry表的material
            "transparent": transparent,  # 对应EyeglassFrameEntry表的is_transparent
            "special": False,  # 默认为False
        }
        lens_width_st = EyeglassFrameEntry_instance.lens_width_st
        bridge_width_st = EyeglassFrameEntry_instance.bridge_width_st
        temple_length_st = EyeglassFrameEntry_instance.temple_length_st
        if lens_width_st and bridge_width_st and temple_length_st:
            options["standard_size"] = [ float(lens_width_st) if lens_width_st is not None else 0.0,
                    float(bridge_width_st) if bridge_width_st is not None else 0.0,
                    float(temple_length_st) if temple_length_st is not None else 0.0]
            # List[float]类型，对应EyeglassFrameEntry表的lens_width_st、bridge_width_st、temple_length_st。严格按顺序
                
        else:
            options["standard_size"] = None
        print(f"计算参数: {options}")
        # 计算参数
        output = process(images, calc_models, options)
        print(output)

    except Exception as e:
        print(f"计算参数失败: {str(e)}")
        # 🔧 失败时的状态处理
        with transaction.atomic():
            # 如果是最后一次重试失败，设置为失败状态(3)
            if self.request.retries >= 2:  # max_retries = 3, 所以最后一次是retries=2, 第四次只用于报错
                print("已达到最大重试次数，设置为失败状态")
                EyeglassFrameEntry_instance.pixel_measurement_state = 3
                EyeglassFrameEntry_instance.millimeter_measurement_state = 3
                EyeglassFrameEntry_instance.calculation_state = 3
                EyeglassFrameEntry_instance.coordinate_state = 3
                EyeglassFrameEntry_instance.image_mask_state = 3
                EyeglassFrameEntry_instance.image_seg_state = 3
                EyeglassFrameEntry_instance.image_beautify_state = 3
                EyeglassFrameEntry_instance.save()
                return f"计算失败：计算参数失败 - {str(e)}"
            else:
                # 如果还会重试，恢复到初始状态，让重试逻辑处理
                print(f"计算失败，准备重试 (当前重试次数: {self.request.retries})")
                EyeglassFrameEntry_instance.pixel_measurement_state = 0
                EyeglassFrameEntry_instance.millimeter_measurement_state = 0
                EyeglassFrameEntry_instance.calculation_state = 0
                EyeglassFrameEntry_instance.coordinate_state = 0
                EyeglassFrameEntry_instance.image_mask_state = 0
                EyeglassFrameEntry_instance.image_seg_state = 0
                EyeglassFrameEntry_instance.image_beautify_state = 0
                EyeglassFrameEntry_instance.save()
                # 抛出异常以触发重试
                raise self.retry(exc=e, countdown=60)

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
                services.save_output_mask(output['mask'], EyeglassFrameImage_instance)
                EyeglassFrameEntry_instance.image_mask_state = 2
                print("mask保存成功")
            else:
                EyeglassFrameEntry_instance.image_mask_state = 3

        except Exception as e:
            EyeglassFrameEntry_instance.image_mask_state = 3
            print("mask处理失败:" + e)

        """
        images处理
        """
        try:
            # 如果images计算成功，保存images；更新计算状态
            if output['image']['state']:
                services.save_output_images(output['image'], EyeglassFrameImage_instance)
                EyeglassFrameEntry_instance.image_seg_state = 2
                EyeglassFrameEntry_instance.image_beautify_state = 2
                print("images保存成功")
            else:
                EyeglassFrameEntry_instance.image_seg_state = 3
                EyeglassFrameEntry_instance.image_beautify_state = 3 
        except Exception as e:
            EyeglassFrameEntry_instance.image_seg_state = 3
            EyeglassFrameEntry_instance.image_beautify_state = 3
            print("images处理失败:" + str(e))

        """
        point处理: 镜架坐标数据 EyeglassFrameCoordinateForm
        """
        try:
            if output['point']['state']:
                services.save_output_point(output['point'], entry_id)
                # 更新计算状态
                EyeglassFrameEntry_instance.coordinate_state = 2
                print("point保存成功")
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
            print("paarameter处理")
            if output['parameter']['state']:
                services.save_output_parameter(output['parameter'], entry_id)
                # 更新计算状态
                EyeglassFrameEntry_instance.pixel_measurement_state = 2
                print("parameter保存成功")
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
            print("size处理")
            if output['size']['state']:
                services.save_output_size(output['size'], entry_id)
                # 更新计算状态
                EyeglassFrameEntry_instance.millimeter_measurement_state = 2
                print("size保存成功")
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
                services.save_output_shape(output['shape'], entry_id)
                # 更新计算状态
                EyeglassFrameEntry_instance.calculation_state = 2
                print("shape保存成功")
            else:
                # 处理镜架计算数据缺失
                raise ValueError("镜架计算数据缺失")
        except Exception as e:
            EyeglassFrameEntry_instance.calculation_state = 3
            print("shape处理失败:" + str(e))  # 删除重复任务（如果还有的话）
        # services.TaskManager.delete_calc_task(sku)
    # 返回
    print('计算任务执行完毕：' + sku)
    EyeglassFrameEntry_instance.is_tryon_leg_auto = True
    EyeglassFrameEntry_instance.is_tryon_beautify_origin = True
    EyeglassFrameEntry_instance.save()

    """
    发送镜架参数
    """
    if not EyeglassFrameEntry_instance:
        # 镜架基本信息表不存在
        error_msg = f"计算失败：镜架基本信息表不存在，SKU: {sku}"
        print(error_msg)
        return error_msg
    # try:
    update.delay_on_commit(sku)

    # except Exception as e:
    #     print(f"更新镜架信息失败: {e}")
    #     return
    """
    生成试戴任务
    """
    # 计算任务正确完成
    if  EyeglassFrameEntry_instance.pixel_measurement_state == 2 and EyeglassFrameEntry_instance.millimeter_measurement_state == 2 and EyeglassFrameEntry_instance.calculation_state == 2 and EyeglassFrameEntry_instance.coordinate_state == 2 and EyeglassFrameEntry_instance.image_mask_state == 2 and EyeglassFrameEntry_instance.image_seg_state == 2 and EyeglassFrameEntry_instance.image_beautify_state == 2:
        """
        生成试戴任务：传递镜架基本信息表的sku值
        """
        EyeglassFrameEntry_instance.aiface_tryon_state = 0 # 待试戴
        tryon.delay_on_commit(sku)
        print("生成试戴任务成功：" + str(sku))
    else:
        print("生成试戴任务失败：" + str(sku))
    # 保存镜架基本信息表
    EyeglassFrameEntry_instance.save()
    print("镜架基本信息表已保存")

    return sku


"""
镜架试戴任务
    args:sku
"""
# 重试四次，第四次不进行业务逻辑，仅失败处理
@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 4, 'countdown': 60})
def tryon(self, sku):
    print(f"执行试戴任务：{sku}, 任务ID: {self.request.id}, 重试次数: {self.request.retries}")

    existing_task_id = services.TaskManager.search_tryon_task(sku)
    if existing_task_id:
        for task_id in existing_task_id:
            if task_id != self.request.id:
                print(f"发现重复任务 {task_id}，正在删除...")
                services.TaskManager.delete_tryon_task(task_id)      

    # calc(sku)
    # 查询镜架基本信息表
    EyeglassFrameEntry_instance = models.EyeglassFrameEntry.objects.filter(sku=sku,is_delete=False).first()
    if not EyeglassFrameEntry_instance:
        # 镜架基本信息表不存在
        error_msg = f"试戴失败：镜架基本信息表不存在，SKU: {sku}"
        print(error_msg)
        return error_msg
    
    if self.request.retries >=4:
        EyeglassFrameEntry_instance.aiface_tryon_state = 3 # 试戴失败
        EyeglassFrameEntry_instance.save()
        print("以达到最大重试次数，试戴失败")
        return
    
    # 检查计算状态
    calculate_state =  EyeglassFrameEntry_instance.pixel_measurement_state == 2 and EyeglassFrameEntry_instance.millimeter_measurement_state == 2 and EyeglassFrameEntry_instance.calculation_state  == 2 and EyeglassFrameEntry_instance.coordinate_state  == 2  and EyeglassFrameEntry_instance.image_mask_state  == 2 and EyeglassFrameEntry_instance.image_seg_state  == 2  and EyeglassFrameEntry_instance.image_beautify_state  == 2 
    if calculate_state == False:
        print("参数计算未完成，无法试戴")
        EyeglassFrameEntry_instance.aiface_tryon_state = 3 # 试戴失败
        EyeglassFrameEntry_instance.save()
        return
    # 查询镜架图片数据表
    EyeglassFrameImage_instance = models.EyeglassFrameImage.objects.filter(entry_id=EyeglassFrameEntry_instance.id,is_delete=False).first()
    if not EyeglassFrameImage_instance:
        # 镜架图片数据表不存在  
        error_msg = f"试戴失败：镜架图片数据表不存在，SKU: {sku}"
        print(error_msg)
        return error_msg
    
    # 处理图片不存在的情况
    if not EyeglassFrameImage_instance.frontview_beautify or not EyeglassFrameImage_instance.front or not EyeglassFrameImage_instance.sideview_beautify:
        # 镜架图片数据表不存在  
        error_msg = f"试戴失败：镜架图片数据表不存在，SKU: {sku}"
        print(error_msg)
        return error_msg
    # 读取镜架图片和信息
    if EyeglassFrameEntry_instance.is_tryon_beautify_origin:
        # 使用原始美化图片
        eyeglass_image = services.read_image_from_field_to_raw(EyeglassFrameImage_instance.frontview_beautify) # 眼镜正面照片
        eyeglass_leg = services.read_image_from_field_to_raw(EyeglassFrameImage_instance.sideview_beautify) # 眼镜侧面照片
    else:
        # 使用处理后美化图片
        eyeglass_image = services.read_image_from_field_to_raw(EyeglassFrameImage_instance.frontview_beautify_processed) # 眼镜正面照片
        eyeglass_leg = services.read_image_from_field_to_raw(EyeglassFrameImage_instance.sideview_beautify_processed) # 眼镜侧面照片、

    eyeglass_mask = services.read_image_from_field_to_raw(EyeglassFrameImage_instance.front) # 眼镜正面黑白图
    eyeglass_leg_mask = services.read_image_from_field_to_raw(EyeglassFrameImage_instance.templeWf) # 眼镜腿黑白图
    is_transparent = EyeglassFrameEntry_instance.is_transparent
    is_tryon_leg_auto = EyeglassFrameEntry_instance.is_tryon_leg_auto
    EyeglassFrameCoordinate_instance = models.EyeglassFrameCoordinate.objects.filter(entry_id=EyeglassFrameEntry_instance.id,is_delete=False).first()
    if EyeglassFrameCoordinate_instance:
        left_points = EyeglassFrameCoordinate_instance.left_points 
        top_left_point = left_points.get("top_left_point") if left_points.get("top_left_point") else [0,0]
        top_right_point = left_points.get("top_right_point") if left_points.get("top_right_point") else [0,0]
        bottom_left_point = left_points.get("bottom_left_point") if left_points.get("bottom_left_point") else [0,0]
        bottom_right_point = left_points.get("bottom_right_point") if left_points.get("bottom_right_point") else [0,0]
    else:
        top_left_point = [0,0]
        top_right_point = [0,0]
        bottom_left_point = [0,0]
        bottom_right_point = [0,0]
    eyeglass_leg_temple_points = json.dumps([top_left_point, top_right_point, bottom_right_point, bottom_left_point])
    print(f"镜架图片和信息读取完成，is_tryon_leg_auto: {is_tryon_leg_auto}, eyeglass_leg_temple_points: {eyeglass_leg_temple_points}")
    # 🔧 重试时的状态恢复逻辑
    initial_states = None
    if self.request.retries > 0:
        print(f"任务重试中，正在恢复初始状态...")
        # 记录当前状态作为"失败前状态"，用于日志
        current_states = {
            "aiface_tryon_state": EyeglassFrameEntry_instance.aiface_tryon_state,
        }
        print(f"重试前状态: {current_states}")

        # 恢复到初始状态（0=待计算）
        with transaction.atomic():
            EyeglassFrameEntry_instance.aiface_tryon_state = 0
            EyeglassFrameEntry_instance.save()
        print("状态已恢复到初始状态(0)")
    else:
        # 首次执行，记录初始状态
        initial_states = {
            "aiface_tryon_state": EyeglassFrameEntry_instance.aiface_tryon_state,
        }
        print(f"首次执行，记录初始状态: {initial_states}")

    """
    更新试戴状态为处理中
    """
    # 数据库事务处理
    with transaction.atomic():
        # 更新镜架基本信息表 计算状态为 1 计算中
        EyeglassFrameEntry_instance.aiface_tryon_state = 1
        # 保存
        EyeglassFrameEntry_instance.save()
        # 更新试戴结果表
        # 获取所有的试戴结果表实例
        eyeglassTryonResult_instances = models.EyeglassTryonResult.objects.filter(entry_id=EyeglassFrameEntry_instance.id,is_delete=False)
        # 读取所有启用的人脸
        aiface_entrys = models.AIFace.objects.filter(is_active=True,is_delete=False)
        for aiface_entry in aiface_entrys:
            # 查询人脸对应的试戴结果表实例
            eyeglassTryonResult_instance = eyeglassTryonResult_instances.filter(face_id=aiface_entry.id).first()
            # 判断试戴结果表实例为空
            if not eyeglassTryonResult_instance:
                # 创建试戴结果表实例
                eyeglassTryonResult_instance = models.EyeglassTryonResult.objects.create(
                    entry_id=EyeglassFrameEntry_instance.id,
                    face_id=aiface_entry.id,
                    tryon_state=0, # 待处理
                )
                eyeglassTryonResult_instance.save()
            else: # 存在试戴结果表实例，则更新
                eyeglassTryonResult_instance.tryon_state = 0 # 待处理
                eyeglassTryonResult_instance.save()

    """
    所有启用的人脸依次试戴
    """
    try:
        tryon_success_flag = True
        # 遍历所有启用的人脸
        for aiface_entry in aiface_entrys:
            # 读取人脸图片
            face_name = aiface_entry.name # 人脸名称
            if not aiface_entry.image:
                # 人脸图片数据表不存在  
                error_msg = f"试戴失败：{face_name}人脸图片不存在，SKU: {sku}"
                print(error_msg)
                continue
            aiface_image = services.read_image_from_field_as_3channel_bytes(aiface_entry.image) # 人脸正面照片
            pupillary_distance = aiface_entry.pupil_distance # 瞳距(毫米)
            # 构建请求参数
            files =  {
                "face_image": aiface_image,
                "eyeglass_image": eyeglass_image,
                "eyeglass_mask": eyeglass_mask,
                "eyeglass_leg": eyeglass_leg,
                "eyeglass_leg_mask":eyeglass_leg_mask
            }
            data = {
                "eyeglass_leg_temple_points": str(eyeglass_leg_temple_points),
                "pupillary_distance": str(pupillary_distance),
                "is_transparent": str(is_transparent),
                "is_manual": str(not is_tryon_leg_auto),
            }
            # 查询试戴结果示例
            eyeglassTryonResult_instance =  models.EyeglassTryonResult.objects.filter(
                entry_id=EyeglassFrameEntry_instance.id,
                face_id=aiface_entry.id,
                is_delete=False
            ).first()
            # 不存在，则创建试戴结果示例
            if not eyeglassTryonResult_instance:
                eyeglassTryonResult_instance = models.EyeglassTryonResult.objects.create(
                    entry_id=EyeglassFrameEntry_instance.id,
                    face_id=aiface_entry.id,
                )
            eyeglassTryonResult_instance.tryon_state=1 # 处理中
            eyeglassTryonResult_instance.save()
            # API服务地址
            # 发送试戴请求
            response = requests.post(f"{TRYON_URL}/try-on",files=files,data=data)
            # 处理响应，处理成功
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'image' in content_type.lower():
                    # 保存试戴结果
                    eyeglassTryonResult_instance.tryon_image.save(
                        f'image.jpg',
                        ContentFile(response.content),
                        save=False
                    )
                    eyeglassTryonResult_instance.tryon_state=2 # 处理成功
                    eyeglassTryonResult_instance.save()
                    continue
            # 返回错误，试戴失败
            print("试戴失败")
            eyeglassTryonResult_instance.tryon_state=3 # 处理失败
            print(f"{face_name} 试戴失败，状态码: {response.status_code}")
            tryon_success_flag = False
    except Exception as e:
        print(f"计算参数失败: {str(e)}")
        # 🔧 失败时的状态处理
        with transaction.atomic():
            # 如果是最后一次重试失败，设置为失败状态(3)
            if self.request.retries >= 2:  # max_retries = 3, 所以最后一次是retries=2
                print("已达到最大重试次数，设置为失败状态")
                EyeglassFrameEntry_instance.aiface_tryon_state = 3
                EyeglassFrameEntry_instance.save()
                return f"计算失败：计算参数失败 - {str(e)}"
            else:
                # 如果还会重试，恢复到初始状态，让重试逻辑处理
                print(f"计算失败，准备重试 (当前重试次数: {self.request.retries})")
                EyeglassFrameEntry_instance.aiface_tryon_state = 0
                EyeglassFrameEntry_instance.save()
                # 抛出异常以触发重试
                raise self.retry(exc=e, countdown=60)

    """
    镜架基本信息表：更新试戴状态
    """
    # 数据库事务处理
    with transaction.atomic():
        if(tryon_success_flag):
            EyeglassFrameEntry_instance.aiface_tryon_state = 2 # 处理成功
        else:
            EyeglassFrameEntry_instance.aiface_tryon_state = 3 # 处理失败
        # 保存镜架基本信息表
        EyeglassFrameEntry_instance.save()
        # print("镜架基本信息表已保存")
    # 返回
    return sku

"""
发送镜架参数到三联系统
"""
@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 4, 'countdown': 60})
def update(self, sku):

    print(f"执行更新任务：{sku}, 任务ID: {self.request.id}, 重试次数: {self.request.retries}")

    # 查询镜架基本信息表
    EyeglassFrameEntry_instance = models.EyeglassFrameEntry.objects.filter(sku=sku, is_delete=False).first()
    if not EyeglassFrameEntry_instance:
        error_msg = f"更新失败：镜架基本信息表不存在，SKU: {sku}"
        print(error_msg)
        return error_msg
    
    # 第四次重试，直接失败
    if self.request.retries >= 3:
        EyeglassFrameEntry_instance.is_update = 3  # 更新失败
        EyeglassFrameEntry_instance.update_info = "达到最大重试次数"
        EyeglassFrameEntry_instance.save()
        print("已达到最大重试次数，更新失败")
        return
    
    # 重试时的状态恢复逻辑
    if self.request.retries > 0:
        print(f"任务重试中，正在恢复初始状态...")
        current_states = {
            'is_update': EyeglassFrameEntry_instance.is_update,
            'update_info': EyeglassFrameEntry_instance.update_info
        }
        print(f"重试前状态: {current_states}")
        
        with transaction.atomic():
            EyeglassFrameEntry_instance.is_update = 0  # 待更新
            EyeglassFrameEntry_instance.update_info = None
            EyeglassFrameEntry_instance.save()
        print("状态已恢复到初始状态(0)")
    
    try:
        # 更新状态为更新中
        with transaction.atomic():
            EyeglassFrameEntry_instance.is_update = 1  # 更新中
            EyeglassFrameEntry_instance.save()
        
        # 获取token
        token = services.get_sanlian_token()
        if not token:
            raise ValueError("获取token失败")
        
        # 更新三联系统数据
        services.update_sanlian_eyeglass(EyeglassFrameEntry_instance.id, token)
        
        # 更新成功
        # with transaction.atomic():
        #     EyeglassFrameEntry_instance.is_update = 2  # 更新成功
        #     EyeglassFrameEntry_instance.update_info = None
        #     EyeglassFrameEntry_instance.save()
        
        # print(f"更新镜架信息成功: {sku}")
        return sku

    except Exception as e:
        print(f"更新镜架信息失败: {str(e)}")
        
        # 失败时的状态处理
        with transaction.atomic():
            if self.request.retries >= 2:  # 最后一次重试失败
                print("已达到最大重试次数，设置为失败状态")
                EyeglassFrameEntry_instance.is_update = 3  # 更新失败
                EyeglassFrameEntry_instance.update_info = f"{str(e)}"
                EyeglassFrameEntry_instance.save()
                return f"更新失败: {str(e)}"
            else:
                # 还会重试，恢复到初始状态
                print(f"更新失败，准备重试 (当前重试次数: {self.request.retries})")
                EyeglassFrameEntry_instance.is_update = 0  # 待更新
                EyeglassFrameEntry_instance.update_info = None
                EyeglassFrameEntry_instance.save()
                # 触发重试
                raise self.retry(exc=e, countdown=60)
