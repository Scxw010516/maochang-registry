import cv2
import os
import tempfile

import redis
import json

from django.core.files.base import ContentFile
import numpy as np
from io import BytesIO
from PIL import Image

from utils import R, regular
from django.db import transaction
from django.core.files import File

from application.glass_management import models
from application.glass_management import forms

from application.celery import app

def save_output_mask(output_mask, instance):
    """
    将process输出的mask保存到Django模型的ImageField中

    Args:
    output_mask: process函数的输出mask
    instance: Django EyglassFrameImage实例
    """
    # 需要保存的mask字段
    mask_fields = {
        'frame': output_mask['data']['frame'],
        'lens': output_mask['data']['lens'],
        'templeWf': output_mask['data']['templeWf'],
        'nose': output_mask['data']['nose'],
        'front': output_mask['data']['front'],
    }

    for field_name, mask_array in mask_fields.items():
        if mask_array is not None:
            # 创建临时文件
            temp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            try:
                # 保存numpy array为图片文件
                cv2.imwrite(temp.name, mask_array)
                # 打开临时文件并保存到ImageField
                with open(temp.name, 'rb') as f:
                    # 模型的字段名与mask fields的key相同
                    getattr(instance, field_name).save(
                        f'{field_name}.png',
                        File(f),
                        save=False
                    )
            finally:
                # 清理临时文件
                temp.close()
                os.unlink(temp.name)
    # 保存模型实例
    instance.save()

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
    EyeglassFrameCoordinate_instance = models.EyeglassFrameCoordinate.objects.filter(entry=entry_instance).first()
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

# 从Redis中获取Celery任务
"""
redis中的任务数据格式如下：
    {'body': 'W1siMjAxMzAyMzEzMDIwMjEwMTE5Il0sIHt9LCB7ImNhbGxiYWNrcyI6IG51bGwsICJlcnJiYWNrcyI6IG51bGwsICJjaGFpbiI6IG51bGwsICJjaG9yZCI6IG51bGx9XQ==', 
    'content-encoding': 'utf-8', 
    'content-type': 'application/json', 
    'headers': {'lang': 'py', 
                'task': 'application.celery_task.tasks.calc', 
                'id': 'ad6b25c6-3c9c-47e7-8a94-9e8ce84d7a1b', 
                'shadow': None, 
                'eta': None, 
                'expires': None, 
                'group': None, ''
                'group_index': None, 
                'retries': 0, 
                'timelimit': [None, None],
                    'root_id': 'ad6b25c6-3c9c-47e7-8a94-9e8ce84d7a1b', 
                    'parent_id': None, 
                    'argsrepr': "('201302313020210119',)",
                    'kwargsrepr': '{}', 
                    'origin': 'gen89@f3f77a063db2', 
                    'ignore_result': False, 
                    'replaced_task_nesting': 0, 
                    'stamped_headers': None, 
                    'stamps': {}}, 
                    'properties': {'correlation_id': 'ad6b25c6-3c9c-47e7-8a94-9e8ce84d7a1b', 
                                'reply_to': '279e92be-4720-3a48-8bbd-0dd9c8b5e798', 
                                'delivery_mode': 2, 
                                'delivery_info': {'exchange': '', 
                                                'routing_key': 
                                                'celery'}, 
                    'priority': 0, 
                    'body_encoding': 'base64',
                        'delivery_tag': '7eb85d6f-bbb3-43d3-90c2-bf0126f23ce4'}}"
"""

# 从 Redis 中获取所有计算任务
def get_calc_queue():
    # 连接到 Redis
    redis_client = redis.Redis(host='redis', port=6379, db=1)
    # 查询默认 Celery 队列中的任务
    queue_name = 'celery'  # 默认队列名称
    tasks = redis_client.lrange(queue_name, 0, -1)  # 获取队列中的所有任务
    # 解析任务数据
    for task in tasks:
        try:
            task_data = json.loads(task)
            task_id = task_data.get('headers', {}).get('id', None)
            task_args = task_data.get('headers', {}).get('argsrepr', [])
            if task_id is None or not task_args:
                print("Task ID or Args are missing in task data")
                continue
            print("Task ID:", task_id)
            print("Task Args:", task_args)
        except json.JSONDecodeError as e:
            print("Failed to decode task data:", e)

# 从 Redis 中获取指定任务
def search_calc_task(sku):
    # 连接到 Redis
    redis_client = redis.Redis(host='redis', port=6379, db=1)
    # 查询默认 Celery 队列中的任务
    queue_name = 'celery'
    tasks = redis_client.lrange(queue_name, 0, -1)
    # 解析任务数据
    for task in tasks:
        try:
            task_data = json.loads(task)
            # 判断任务类型是否为calc
            if task_data.get('headers', {}).get('task', '') == "application.celery_task.tasks.calc":
                task_id = task_data.get('headers', {}).get('id', None)
                task_args = task_data.get('headers', {}).get('argsrepr', '[]')
                task_args_list = eval(task_args)  # 将字符串转换为元组
                first_arg = task_args_list[0]
                if sku in first_arg:
                    print("find task:", task_id,";sku:",sku)
                    return task_id
        except json.JSONDecodeError as e:
            print("Failed to decode task data:", e)
    print("No matching task found:",sku)
    return 0

def delete_calc_task(sku):
    # 连接到 Redis
    redis_client = redis.Redis(host='redis', port=6379, db=1)
    # 查询默认 Celery 队列中的任务
    queue_name = 'celery'
    tasks = redis_client.lrange(queue_name, 0, -1)
    # 解析任务数据
    for task in tasks:
        try:
            # 只有calc任务，所以暂时不需要判断任务类型
            task_data = json.loads(task)
            if task_data.get('headers', {}).get('task', '') == "application.celery_task.tasks.calc":
                task_id = task_data.get('headers', {}).get('id', None)
                task_args = task_data.get('headers', {}).get('argsrepr', '[]')
                task_args_list = eval(task_args)  # 将字符串转换为元组
                first_arg = task_args_list[0]
                if sku in first_arg:
                    # 从队列中移除任务
                    redis_client.lrem(queue_name, 1, task)
                    print("Task removed:", task_id)
        except json.JSONDecodeError as e:
            print("Failed to decode task data:", e)
    return None

# def check_redis_connection():
#     # 直接使用导入的 app
#     ins = app.control.inspect(destination=None)
#     print("active:", ins.active())
    
#     try:
#         redis_client = redis.Redis(host='redis', port=6379, db=1)
        
#         # 检查所有相关的 keys
#         celery_keys = {
#             'bindings': redis_client.keys('_kombu.binding.*'),
#             'active': redis_client.keys('celery-*'),
#             'tasks': redis_client.lrange('celery', 0, -1)
#         }
        
#         print("Celery 状态:")
#         print(f"- 绑定: {celery_keys['bindings']}")
#         print(f"- 活动任务: {celery_keys['active']}")
#         print(f"- 待处理任务: {len(celery_keys['tasks'])}")
        
#         return celery_keys
        
#     except redis.RedisError as e:
#         print(f"Redis 查询失败: {str(e)}")
#         return None
    

 

 
