from celery import shared_task

import json
from utils import R, regular
from django.db import connection,connections
from eventlet.green.thread import get_ident
from django.db import transaction

from application.glass_management import models
from application.glass_management import forms


@shared_task
def calc(sku):
    """
    计算眼镜参数
    """
    #创建连接
    conn = connection
    conn._thread_ident = get_ident()
    print("连接已建立")
    models.EyeglassFrameEntry.objects.filter(sku=sku).update(calc_status='1') #更新计算状态为计算中
    # 计算
    calc_prams = {  "frame_height": 2,
        "frame_width": 2,
        "pile_height_left": 2,
        "pile_height_right": 2,
        "frame_top_width": 2,
        "top_points": 2,
        "frame_rects": 2,
        "lens_width_left": 2,
        "lens_width_right": 2,
        "lens_height_left": 2,
        "lens_height_right": 2,
        "lens_diagonal_left": 2,
        "lens_diagonal_right": 2,
        "lens_area_left": 2,
        "lens_area_right": 2,
        "bridge_width": 2,
        "lens_center_points": 2,
        "lens_top_points": 2,
        "vertical_angle": 2,
        "forward_angle": 2,
        "temple_angle": 2,
        "drop_length": 2,
        "face_angle": 2,
        "sagittal_angle_left": 2,
        "sagittal_angle_right": 2,
        "temple_length_left": 2,
        "temple_length_right": 2,
        "temporal_width": 2,
        "spread_angle_left": 2,
        "spread_angle_right": 2,
        "pile_distance": 2,}
    # calc_prams = json.dumps(calc_prams)
    print("calc_prams: ", calc_prams)
    # style={}
    # 储存
    # 数据库事务处理
    with transaction.atomic():
        # 查找镜架基本信息表
        EyeglassFrameEntry_instance = (
            models.EyeglassFrameEntry.objects.filter(sku=sku).first()
        )
        """
        镜架扫描结果表处理
        """
        # 查询镜架扫描结果表实例
        EyeglassFrameDetectionResult_instance = (
            models.EyeglassFrameDetectionResult.objects.filter(
                entry=EyeglassFrameEntry_instance
            ).first()
        )
        print("EyeglassFrameDetectionResult_instance: ", EyeglassFrameDetectionResult_instance)
        # 镜架扫描结果表实例为空判断
        if not EyeglassFrameDetectionResult_instance:
            # 抛出异常
            print("镜架扫描结果表实例为空")
        # 获取现有实例的重量字段值
        existing_weight = EyeglassFrameDetectionResult_instance.weight
        # 将重量字段值添加到 calc_prams
        calc_prams['weight'] = existing_weight
        # 创建镜架扫描结果表实例
        form_EyeglassFrameDetectionResult = (
            forms.EyeglassFrameDetectionResultForm(
                calc_prams, instance=EyeglassFrameDetectionResult_instance
            )
        )
        print("form_EyeglassFrameDetectionResult: ", form_EyeglassFrameDetectionResult)
        # 验证镜架扫描结果表表单
        if form_EyeglassFrameDetectionResult.is_valid():
            # 保存镜架扫描结果表实例
            EyeglassFrameDetectionResult_instance = (
                form_EyeglassFrameDetectionResult.save()
            )
        else:
            # 处理镜架扫描结果表表单验证失败的情况
            err_msg = regular.get_err(form_EyeglassFrameDetectionResult)
            # 抛出异常
            print("error form: 表单验证未通过")
      
    models.EyeglassFrameDataFromExcel.objects.filter(sku=sku).update(calc_status='0') #更新计算状态为计算完成
    #关闭本线程全部连接
    connections.close_all()
    print("连接已关闭")
    # 返回
    print(sku)
    print('执行完毕')
    return sku

# todo：添加轮询功能