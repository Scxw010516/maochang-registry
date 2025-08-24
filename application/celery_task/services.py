import cv2
import os
import tempfile
import requests
import json
import datetime
import random

from django.core.files.base import ContentFile
import numpy as np
from io import BytesIO
from PIL import Image

from utils import R, regular
from django.db import transaction
from django.core.files import File

#OBS函数
from utils.obs.obs_client import get_image_object,get_image_object_raw,get_image_object_as_3channel_bytes

from application.glass_management import models
from application.glass_management import forms

from application.celery import app


def get_current_timestamp():
    """
    生成当前时间戳
    
    Returns:
        str: 格式化的时间戳字符串，格式为 "YYYY-MM-DD HH:MM:SS"
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
                    getattr(instance, field_name).save(f'{field_name}.png', File(f), save=False)
            finally:
                # 清理临时文件
                temp.close()
                os.unlink(temp.name)
    # 保存模型实例
    instance.save()

# todo：修改保存方法：
#   if mask_array is not None:
#             # 将numpy array转换为bytes
#             success, img_buffer = cv2.imencode('.png', mask_array)
#             if success:
#                 # 直接使用ContentFile保存到ImageField，避免临时文件
#                 getattr(instance, field_name).save(
#                     f'{field_name}.png',
#                     ContentFile(img_buffer.tobytes()),
#                     save=False
#                 )
#             else:
#                 print(f"编码mask失败: {field_name}")
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
        'sideview_beautify': output_images['data']['sideview_beautify'],
    }

    for field_name, image_array in image_fields.items():
        if image_array is not None:
            # 创建临时文件
            temp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            try:
                # 保存numpy array为图片文件
                cv2.imwrite(temp.name, image_array)
                # 打开临时文件并保存到ImageField
                with open(temp.name, 'rb') as f:
                    # 模型的字段名与image fields的key相同
                    getattr(instance, field_name).save(f'{field_name}.png', File(f), save=False)
            finally:
                # 清理临时文件
                temp.close()
                os.unlink(temp.name)
    # 保存模型实例
    instance.save()


def save_output_point(output_point, entry_id):
    # 清洗数据：将 numpy 类型转为 Python 原生类型
    def convert(data):
        if isinstance(data, np.integer):
            return int(data)
        elif isinstance(data, np.floating):
            return float(data)
        elif isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, dict):
            return {k: convert(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [convert(v) for v in data]
        else:
            return data
    try:
        # 重构output_point['data']，确保数据格式正确
        cleaned_data = convert(output_point['data'])

        front_points = cleaned_data.get('front', {})
        left_points = cleaned_data.get('left', {})
        up_points = cleaned_data.get('up', {})
        EyeglassFrameCoordinate_instance = models.EyeglassFrameCoordinate.objects.filter(entry_id=entry_id).first()
        if not EyeglassFrameCoordinate_instance:
            # 不存在镜架坐标数据表实例，则创建
            print("Creating new EyeglassFrameCoordinate instance")
            EyeglassFrameCoordinate_instance = models.EyeglassFrameCoordinate.objects.create(
                entry_id=entry_id,
                front_points=front_points,
                left_points=left_points,
                up_points=up_points,
            )
            EyeglassFrameCoordinate_instance.save()

        else:
            # 存在镜架坐标数据表实例，则更新
            print("Updating existing EyeglassFrameCoordinate instance")
            EyeglassFrameCoordinate_instance.front_points = front_points
            EyeglassFrameCoordinate_instance.left_points = left_points
            EyeglassFrameCoordinate_instance.up_points = up_points
            EyeglassFrameCoordinate_instance.save()
    except Exception as e:
        raise ValueError("保存镜架坐标数据失败", e)



def save_output_parameter(output_parameter, entry_id):
    # 数据位数处理：保留到小数点后四位
    for key in output_parameter['data']:
        output_parameter['data'][key] = round(output_parameter['data'][key], 4)
    # 查询镜架像素测量数据表实例
    EyeglassFramePixelMeasurement_instance = models.EyeglassFramePixelMeasurement.objects.filter(
        entry_id=entry_id
    ).first()
    if not EyeglassFramePixelMeasurement_instance:
        # 不存在镜架像素测量数据表实例，则创建
        form_EyeglassFramePixelMeasurement = forms.EyeglassFramePixelMeasurementForm(output_parameter['data'])
    else:
        # 存在镜架像素测量数据表实例，则更新
        form_EyeglassFramePixelMeasurement = forms.EyeglassFramePixelMeasurementForm(
            output_parameter['data'], instance=EyeglassFramePixelMeasurement_instance
        )
    if form_EyeglassFramePixelMeasurement.is_valid():
        # 构建并保存镜架像素测量数据表数据库实例
        EyeglassFramePixelMeasurement_instance = form_EyeglassFramePixelMeasurement.save(commit=False)
        # 关联镜架基本信息表外键
        EyeglassFramePixelMeasurement_instance.entry_id = entry_id
        EyeglassFramePixelMeasurement_instance.save()
    else:
        raise ValueError("镜架像素测量数据表表单验证失败")


def save_output_size(output_size, entry_id):
    # 数据位数处理：保留到小数点后四位
    for key in output_size['data']:
        output_size['data'][key] = round(output_size['data'][key], 4)
    # 查询镜架毫米测量数据表实例
    EyeglassFrameMillimeterMeasurement_instance = models.EyeglassFrameMillimeterMeasurement.objects.filter(
        entry_id=entry_id
    ).first()
    if not EyeglassFrameMillimeterMeasurement_instance:
        # 不存在镜架毫米测量数据表实例，则创建
        form_EyeglassFrameMillimeterMeasurement = forms.EyeglassFrameMillimeterMeasurementForm(output_size['data'])
    else:
        # 存在镜架毫米测量数据表实例，则更新
        form_EyeglassFrameMillimeterMeasurement = forms.EyeglassFrameMillimeterMeasurementForm(
            output_size['data'], instance=EyeglassFrameMillimeterMeasurement_instance
        )
    if form_EyeglassFrameMillimeterMeasurement.is_valid():
        # 构建并保存镜架毫米测量数据表数据库实例
        EyeglassFrameMillimeterMeasurement_instance = form_EyeglassFrameMillimeterMeasurement.save(commit=False)
        # 关联镜架基本信息表外键
        EyeglassFrameMillimeterMeasurement_instance.entry_id = entry_id
        EyeglassFrameMillimeterMeasurement_instance.save()
    else:
        raise ValueError("镜架毫米测量数据表表单验证失败")


def save_output_shape(output_shape, entry_id):
    # 数据位数处理：保留到小数点后四位
    for key in output_shape['data']:
        if key != 'frame_size':
            output_shape['data'][key] = round(output_shape['data'][key], 4)
    # 查询镜架计算数据表实例
    EyeglassFrameCalculation_instance = models.EyeglassFrameCalculation.objects.filter(entry_id=entry_id).first()
    if not EyeglassFrameCalculation_instance:
        # 不存在镜架计算数据表实例，则创建
        form_EyeglassFrameCalculation = forms.EyeglassFrameCalculationForm(output_shape['data'])
    else:
        # 存在镜架计算数据表实例，则更新
        form_EyeglassFrameCalculation = forms.EyeglassFrameCalculationForm(
            output_shape['data'], instance=EyeglassFrameCalculation_instance
        )
    if form_EyeglassFrameCalculation.is_valid():
        # 构建并保存镜架计算数据表数据库实例
        EyeglassFrameCalculation_instance = form_EyeglassFrameCalculation.save(commit=False)
        # 关联镜架基本信息表外键
        EyeglassFrameCalculation_instance.entry_id = entry_id
        EyeglassFrameCalculation_instance.save()
    else:
        raise ValueError("镜架计算数据表表单验证失败")

def get_sanlian_token():
    """
    获取三联的token
    """
    try:
        token_data = {
            "client_id": "SF_inspection",
            "client_secret": "yN8-wA3=oR2^yM1&xJ5;zU4&a",
            "username":"kdA",
            "accountId": "1789897953700315136",
            "nonce": str(random.randint(1000, 9999)),
            "timestamp": get_current_timestamp()  # 自动生成当前时间戳
        }
        response = requests.post(
            "https://sanlianjituan.test.kdcloud.com/kapi/oauth2/getToken", 
            json=token_data,
        )
        print(f"获取三联token响应: {response.json()}")
        # 直接返回token，如果任何环节出错则抛出异常
        if response.json().get("errorCode") != '0':
            raise ValueError("获取三联token失败")
        token = response.json().get("data").get("access_token")
        return token
    except Exception:
        # 重新抛出异常，让调用者处理
        raise


def update_sanlian_eyeglass(id, token):
    """
    更新三联眼镜信息
    """
    try:
        EyeglassFrameEntry_instance = models.EyeglassFrameEntry.objects.filter(id=id).first()
        EyeglassFrameMillimeterMeasurement_instance = models.EyeglassFrameMillimeterMeasurement.objects.filter(
            entry_id=id
        ).first()

        def safe_int(value, default=0):
            """安全地将值转换为整数，如果值为None则返回默认值"""
            if value is None:
                return default
            if type(value) == int:
                return value
            return int(value)

        def safe_str(value, default=""):
            """安全地将值转换为字符串，如果值为None则返回默认值"""
            if value is None:
                return default
            if type(value) == str:
                return value
            return str(value)
        
        data ={
            "number": safe_str(EyeglassFrameEntry_instance.sku),
            "createorg_number": "1",
            "shcp_textfield": safe_str(EyeglassFrameEntry_instance.brand),
            "shcp_model": safe_str(EyeglassFrameEntry_instance.model_type),
            "shcp_price1": EyeglassFrameEntry_instance.price,  # 价格可能需要特殊处理
            "shcp_materialquality": safe_str(EyeglassFrameEntry_instance.material),
            "shcp_color": safe_str(EyeglassFrameEntry_instance.color),
            "shcp_shape": safe_str(EyeglassFrameEntry_instance.shape),
            "shcp_nosepad": EyeglassFrameEntry_instance.isnosepad,
            "shcp_stocks": safe_int(EyeglassFrameEntry_instance.stock),
            "shcp_radian": safe_int(EyeglassFrameEntry_instance.lens_radian),
            "shcp_width": safe_int(EyeglassFrameEntry_instance.lens_width_st),
            "shcp_nosepadwidth": safe_int(EyeglassFrameEntry_instance.bridge_width_st),
            "shcp_leglength": safe_int(EyeglassFrameEntry_instance.temple_length_st),
            "shcp_weight": safe_int(EyeglassFrameEntry_instance.weight),
            "shcp_style": ",1,",
            "shcp_frameheight": safe_str(EyeglassFrameMillimeterMeasurement_instance.frame_height),
            "shcp_glass_width": safe_int(EyeglassFrameMillimeterMeasurement_instance.frame_width),
            "shcp_leftpile_heigth": safe_int(EyeglassFrameMillimeterMeasurement_instance.pile_height_left),
            "shcp_rightpile_heigth": safe_int(EyeglassFrameMillimeterMeasurement_instance.pile_height_right),
            "shcp_frame_width": safe_int(EyeglassFrameMillimeterMeasurement_instance.frame_width),
            "shcp_leftring_width": safe_int(EyeglassFrameMillimeterMeasurement_instance.lens_width_left),
            "shcp_rightring_width": safe_int(EyeglassFrameMillimeterMeasurement_instance.lens_width_right),
            "shcp_leftring_heigth": safe_int(EyeglassFrameMillimeterMeasurement_instance.lens_height_left),
            "shcp_rightring_heigth": safe_int(EyeglassFrameMillimeterMeasurement_instance.lens_height_right),
            "shcp_leftring_length": safe_int(EyeglassFrameMillimeterMeasurement_instance.lens_diagonal_left),
            "shcp_rightring_length": safe_int(EyeglassFrameMillimeterMeasurement_instance.lens_diagonal_right),
            "shcp_rightring_area": safe_int(EyeglassFrameMillimeterMeasurement_instance.lens_area_right),
            "shcp_integerfield": safe_int(EyeglassFrameMillimeterMeasurement_instance.lens_area_left),
            "shcp_nosepadwidth1": safe_int(EyeglassFrameMillimeterMeasurement_instance.bridge_width),
            "shcp_lowangle": safe_int(EyeglassFrameMillimeterMeasurement_instance.vertical_angle),
            "shcp_frontangle": safe_int(EyeglassFrameMillimeterMeasurement_instance.forward_angle),
            "shcp_legangle": safe_int(EyeglassFrameMillimeterMeasurement_instance.temple_angle),
            "shcp_anglelength": safe_int(EyeglassFrameMillimeterMeasurement_instance.drop_length),
            "shcp_facecurveness": safe_int(EyeglassFrameMillimeterMeasurement_instance.face_angle),
            "shcp_integerfield3": safe_int(EyeglassFrameMillimeterMeasurement_instance.sagittal_angle_left),
            "shcp_rightlow_angle": safe_int(EyeglassFrameMillimeterMeasurement_instance.sagittal_angle_right),
            "shcp_integerfield1": safe_int(EyeglassFrameMillimeterMeasurement_instance.temple_length_left),
            "shcp_rightleg_length": safe_int(EyeglassFrameMillimeterMeasurement_instance.temple_length_right),
            "shcp_integerfield2": safe_int(EyeglassFrameMillimeterMeasurement_instance.temporal_width),
            "shcp_integerfield4": safe_int(EyeglassFrameMillimeterMeasurement_instance.spread_angle_left),
            "shcp_rightleg_angle": safe_int(EyeglassFrameMillimeterMeasurement_instance.spread_angle_right),
            "shcp_pilelength": safe_int(EyeglassFrameMillimeterMeasurement_instance.pile_distance),
        }
        response = requests.post(
            "https://sanlianjituan.test.kdcloud.com/kapi/v2/shcp/basedata/bd_material/updateSFinfo",
            headers={"Content-Type": "application/json", "accesstoken": token},
            json={"data": data}
        )
        print(f"更新镜架信息响应: {response.json()}")
    except Exception as e:
        print(f"更新镜架信息错误: {e}")
        raise

def read_image_from_field(image_field):
    """从Django的ImageField中获得url读取图像并转换为OpenCV格式"""
    if not image_field :
        return None
    img_path = str(image_field)
    img = get_image_object(img_path)
    # print("Image path:", img_path)
    return img

def read_image_from_field_to_raw(image_field):
    """从Django的ImageField中获得url读取图像并返回原始字节流"""
    if not image_field :
        return None
    img_path = str(image_field)
    img = get_image_object_raw(img_path)
    # print("Image path:", img_path)
    return img

def read_image_from_field_as_3channel_bytes(image_field):
    """从Django的ImageField中获得url读取图像并强制转换为3通道，然后返回原始字节流"""
    if not image_field :
        return None
    img_path = str(image_field)
    img = get_image_object_as_3channel_bytes(img_path)
    # print("Image path:", img_path)
    return img
    
# Celery任务管理工具类
class TaskManager:
    """使用Celery原生API管理任务队列，避免直接操作Redis"""

    @staticmethod
    def get_calc_queue():
        """获取所有计算任务"""
        try:
            # 使用Celery的inspect API获取队列信息
            inspector = app.control.inspect()

            # 获取排队中的任务
            scheduled_tasks = inspector.scheduled()
            reserved_tasks = inspector.reserved()
            active_tasks = inspector.active()

            calc_tasks = []

            # 检查所有类型的任务
            for worker_name, tasks in (scheduled_tasks or {}).items():
                for task in tasks:
                    if task.get('name') == 'application.celery_task.tasks.calc':
                        calc_tasks.append(
                            {
                                'id': task.get('id'),
                                'args': task.get('args', []),
                                'state': 'scheduled',
                                'worker': worker_name,
                            }
                        )

            for worker_name, tasks in (reserved_tasks or {}).items():
                for task in tasks:
                    if task.get('name') == 'application.celery_task.tasks.calc':
                        calc_tasks.append(
                            {
                                'id': task.get('id'),
                                'args': task.get('args', []),
                                'state': 'reserved',
                                'worker': worker_name,
                            }
                        )

            for worker_name, tasks in (active_tasks or {}).items():
                for task in tasks:
                    if task.get('name') == 'application.celery_task.tasks.calc':
                        calc_tasks.append(
                            {
                                'id': task.get('id'),
                                'args': task.get('args', []),
                                'state': 'active',
                                'worker': worker_name,
                            }
                        )

            return calc_tasks

        except Exception as e:
            print(f"获取任务队列失败: {str(e)}")
            return []

    @staticmethod
    def search_calc_task(sku):
        """搜索指定SKU的计算任务"""
        try:
            calc_tasks = TaskManager.get_calc_queue()

            for task in calc_tasks:
                # 检查任务参数中是否包含指定的SKU
                args = task.get('args', [])
                if args and len(args) > 0 and sku in str(args[0]):
                    print(f"找到任务: {task['id']}, SKU: {sku}, 状态: {task['state']}")
                    return task['id']

            print(f"未找到匹配的任务: {sku}")
            return None

        except Exception as e:
            print(f"搜索任务失败: {str(e)}")
            return None

    @staticmethod
    def delete_calc_task(sku):
        """删除指定SKU的计算任务"""
        try:
            # 先搜索任务
            task_id = TaskManager.search_calc_task(sku)

            if task_id:
                # 使用Celery的revoke方法撤销任务
                app.control.revoke(task_id, terminate=True)
                print(f"任务已删除: {task_id}")
                return True
            else:
                print(f"未找到要删除的任务: {sku}")
                return False

        except Exception as e:
            print(f"删除任务失败: {str(e)}")
            return False

    @staticmethod
    def check_calc_task_exists(sku):
        """检查指定SKU的任务是否存在"""
        return TaskManager.search_calc_task(sku) is not None
    
    
    @staticmethod
    def get_tryon_queue():
        """获取所有计算任务"""
        try:
            # 使用Celery的inspect API获取队列信息
            inspector = app.control.inspect()

            # 获取排队中的任务
            scheduled_tasks = inspector.scheduled()
            reserved_tasks = inspector.reserved()
            active_tasks = inspector.active()

            tryon_tasks = []

            # 检查所有类型的任务
            for worker_name, tasks in (scheduled_tasks or {}).items():
                for task in tasks:
                    if task.get('name') == 'application.celery_task.tasks.tryon':
                        tryon_tasks.append(
                            {
                                'id': task.get('id'),
                                'args': task.get('args', []),
                                'state': 'scheduled',
                                'worker': worker_name,
                            }
                        )

            for worker_name, tasks in (reserved_tasks or {}).items():
                for task in tasks:
                    if task.get('name') == 'application.celery_task.tasks.tryon':
                        tryon_tasks.append(
                            {
                                'id': task.get('id'),
                                'args': task.get('args', []),
                                'state': 'reserved',
                                'worker': worker_name,
                            }
                        )

            for worker_name, tasks in (active_tasks or {}).items():
                for task in tasks:
                    if task.get('name') == 'application.celery_task.tasks.tryon':
                        tryon_tasks.append(
                            {
                                'id': task.get('id'),
                                'args': task.get('args', []),
                                'state': 'active',
                                'worker': worker_name,
                            }
                        )

            return tryon_tasks

        except Exception as e:
            print(f"获取任务队列失败: {str(e)}")
            return []

    @staticmethod
    def search_tryon_task(sku):
        """搜索指定SKU的计算任务"""
        try:
            tryon_tasks = TaskManager.get_tryon_queue()

            for task in tryon_tasks:
                # 检查任务参数中是否包含指定的SKU
                args = task.get('args', [])
                if args and len(args) > 0 and sku in str(args[0]):
                    print(f"找到任务: {task['id']}, SKU: {sku}, 状态: {task['state']}")
                    return task['id']

            print(f"未找到匹配的任务: {sku}")
            return None

        except Exception as e:
            print(f"搜索任务失败: {str(e)}")
            return None

    @staticmethod
    def delete_tryon_task(sku):
        """删除指定SKU的计算任务"""
        try:
            # 先搜索任务
            task_id = TaskManager.search_tryon_task(sku)

            if task_id:
                # 使用Celery的revoke方法撤销任务
                app.control.revoke(task_id, terminate=True)
                print(f"任务已删除: {task_id}")
                return True
            else:
                print(f"未找到要删除的任务: {sku}")
                return False

        except Exception as e:
            print(f"删除任务失败: {str(e)}")
            return False

    @staticmethod
    def check_tryon_task_exists(sku):
        """检查指定SKU的任务是否存在"""
        return TaskManager.search_tryon_task(sku) is not None


# 保持向后兼容的函数接口
def get_calc_queue():
    """获取所有计算任务 - 使用Celery原生API"""
    return TaskManager.get_calc_queue()


def search_calc_task(sku):
    """搜索指定SKU的计算任务 - 使用Celery原生API"""
    return TaskManager.search_calc_task(sku)


def delete_calc_task(sku):
    """删除指定SKU的计算任务 - 使用Celery原生API"""
    return TaskManager.delete_calc_task(sku)


# def check_redis_connection():
#     # 直接使用导入的 app
#     ins = app.control.inspect(destination=None)
#     print("active:", ins.active())

#     try:
#         redis_client = redis.Redis(host='redis', port=6379, db=0)

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
