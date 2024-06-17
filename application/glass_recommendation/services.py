import json
import decimal
from utils import R, regular
from utils import utils
from django.db import transaction
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, HttpRequest

from application.glass_recommendation import models
from application.glass_recommendation import forms

# 推荐客户端

def RegisterRecommendationUser(request:HttpRequest):
    """
    查询推荐客户端用户, 拍摄300人脸版本

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数
    username = request.GET.get("username")

    # 参数为空或空字符串判断
    if not username:
        return R.failed(msg="参数输入错误")
    
    try:
        # 直接使用get()方法进行查询，提高效率
        user = models.RecommendationUser.objects.get(username=username)
        return R.failed(msg="用户名已存在")
    except models.RecommendationUser.DoesNotExist:
        pass
    
    # 验证推荐客户端用户表表单
    form_RecommendationUser = forms.RecommendationUserForm(request.GET)
    # 验证推荐客户端用户表表单
    if form_RecommendationUser.is_valid():
        # 构建并保存推荐客户端用户表的数据库实例
        RecommendationUser_instance = form_RecommendationUser.save()
        # 返回成功信息
        return R.ok(msg="用户注册成功")
    else:
        # 处理推荐客户端用户表表单验证失败的情况
        return R.failed(msg="参数输入错误")

def SaveNewRecommendationUserFacialImageAndFacialScanResult(request:HttpRequest):
    """
    保存新推荐客户端用户人脸图片和人脸扫描数据，创建新的数据库实例：推荐客户端用户人脸图像表、推荐客户端用户人脸扫描数据表

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数
    if not request.POST:
        return R.failed(msg="参数错误")
    
    # 获取用户识别码
    username = request.POST.get("username")
    # 用户识别码为空判断
    if not username:
        return R.failed(msg="用户ID为空")
    
    # 查询推荐客户端用户是否存在
    user = models.RecommendationUser.objects.filter(username=username).first()
    # 推荐客户端用户为空判断
    if not user:
        return R.failed(msg="用户不存在")
    
    try:
        # 数据库事务处理
        with transaction.atomic():
            """
            推荐客户端用户人脸图像表处理
            """
            # 创建推荐客户端用户人脸图像表实例
            form_RecommendationUserFacialImage = forms.RecommendationUserFacialImageForm(request.POST)
            # 验证推荐客户端用户人脸图像表表单
            if form_RecommendationUserFacialImage.is_valid():
                # 构建并保存推荐客户端用户人脸图像表的数据库实例
                RecommendationUserFacialImage_instance = form_RecommendationUserFacialImage.save(commit=False)
                # 关联推荐客户端用户基础信息表外键
                RecommendationUserFacialImage_instance.user = user
                # 获取人脸图像文件
                frontview = request.FILES.get("frontview")
                leftview = request.FILES.get("leftview")
                rightview = request.FILES.get("rightview")
                # 获取人脸图像文件错误处理
                if not frontview or not leftview or not rightview:
                    # 抛出异常
                    raise ValueError("人脸图像不能为空")
                # 保存人脸图像文件
                RecommendationUserFacialImage_instance.frontview = frontview
                RecommendationUserFacialImage_instance.leftview = leftview
                RecommendationUserFacialImage_instance.rightview = rightview
                # 保存推荐客户端用户人脸图像表实例
                RecommendationUserFacialImage_instance.save()
            else:
                # 处理推荐客户端用户人脸图像表表单验证失败的情况
                err_msg = regular.get_err(form_RecommendationUserFacialImage)
                # 抛出异常
                raise ValueError(err_msg)
            
            """
            推荐客户端用户人脸扫描数据表处理
            """
            # 创建推荐客户端用户人脸扫描数据表实例
            form_RecommendationUserFacialScanResult = forms.RecommendationUserFacialScanResultForm(request.POST)
            # 验证推荐客户端用户人脸扫描数据表表单
            if form_RecommendationUserFacialScanResult.is_valid():
                # 构建并保存推荐客户端用户人脸扫描数据表的数据库实例
                RecommendationUserFacialScanResult_instance = form_RecommendationUserFacialScanResult.save(commit=False)
                # 关联推荐客户端用户基础信息表外键
                RecommendationUserFacialScanResult_instance.user = user
                # 保存推荐客户端用户人脸扫描数据表实例
                RecommendationUserFacialScanResult_instance.save()
            else:
                # 处理推荐客户端用户人脸扫描数据表表单验证失败的情况
                err_msg = regular.get_err(form_RecommendationUserFacialScanResult)
                # 抛出异常
                raise ValueError(err_msg)
            
            # 返回成功信息
            return R.ok(msg="人脸图片保存成功")
    except ValueError as ve:
        return R.failed(msg=str(ve))
    except Exception as e:
        return R.failed(msg=str(e))
    
def SaveNewRecommendationUserBaseInfoAndOptometryAndLens(request:HttpRequest):
    """
    保存新推荐客户端用户基础信息、验光信息和镜片需求，创建新的数据库实例：推荐客户端用户基础信息表、推荐客户端用户验光信息表、推荐客户端用户镜片需求表

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数
    if not request.POST:
        return R.failed(msg="参数错误")
    
    # 获取用户识别码
    username = request.POST.get("username")
    # 用户识别码为空判断
    if not username:
        return R.failed(msg="用户ID为空")
    
    # 查询推荐客户端用户是否存在
    user = models.RecommendationUser.objects.filter(username=username).first()
    # 推荐客户端用户为空判断
    if not user:
        return R.failed(msg="用户不存在")
    
    try:
        # 数据库事务处理
        with transaction.atomic():
            """
            推荐客户端用户基础信息表处理
            """
            # 创建推荐客户端用户基础信息表实例
            form_RecommendationUserBaseInfo = forms.RecommendationUserBaseInfoForm(request.POST)
            # 验证推荐客户端用户基础信息表表单
            if form_RecommendationUserBaseInfo.is_valid():
                # 保存推荐客户端用户基础信息表实例
                RecommendationUserBaseInfo_instance = form_RecommendationUserBaseInfo.save(commit=False)
                # 关联推荐客户端用户基础信息表外键
                RecommendationUserBaseInfo_instance.user = user
                # 保存推荐客户端用户基础信息表实例
                RecommendationUserBaseInfo_instance.save()
            else:
                # 处理推荐客户端用户基础信息表表单验证失败的情况
                err_msg = regular.get_err(form_RecommendationUserBaseInfo)
                # 抛出异常
                raise ValueError(err_msg)
            
            """
            推荐客户端用户验光信息表处理
            """
            # 创建推荐客户端用户验光信息表实例
            form_RecommendationUserOptometry = forms.RecommendationUserOptometryForm(request.POST)
            # 验证推荐客户端用户验光信息表表单
            if form_RecommendationUserOptometry.is_valid():
                # 构建并保存推荐客户端用户验光信息表的数据库实例
                RecommendationUserOptometry_instance = form_RecommendationUserOptometry.save(commit=False)
                # 关联推荐客户端用户基础信息表外键
                RecommendationUserOptometry_instance.user = user
                # 保存推荐客户端用户验光信息表实例
                RecommendationUserOptometry_instance.save()
            else:
                # 处理推荐客户端用户验光信息表表单验证失败的情况
                err_msg = regular.get_err(form_RecommendationUserOptometry)
                # 抛出异常
                raise ValueError(err_msg)
            
            """
            推荐客户端用户镜片需求表处理
            """
            # 创建推荐客户端用户镜片需求表实例
            form_RecommendationUserLens = forms.RecommendationUserLensForm(request.POST)
            # 验证推荐客户端用户镜片需求表表单
            if form_RecommendationUserLens.is_valid():
                # 构建并保存推荐客户端用户镜片需求表的数据库实例
                RecommendationUserLens_instance = form_RecommendationUserLens.save(commit=False)
                # 关联推荐客户端用户基础信息表外键
                RecommendationUserLens_instance.user = user
                # 保存推荐客户端用户镜片需求表实例
                RecommendationUserLens_instance.save()
            else:
                # 处理推荐客户端用户镜片需求表表单验证失败的情况
                err_msg = regular.get_err(form_RecommendationUserLens)
                # 抛出异常
                raise ValueError(err_msg)
            
            # 返回成功信息
            return R.ok(msg="用户信息保存成功")
    except ValueError as ve:
        return R.failed(msg=str(ve))
    except Exception as e:
        return R.failed(msg=str(e))



# # 查询推荐客户端用户验光信息表
# optometry = models.RecommendationUserOptometry.objects.filter(user=user).first()
# # 查询推荐客户端用户镜片需求表
# lens = models.RecommendationUserLens.objects.filter(user=user).first()
# # 查询推荐客户端用户人脸扫描数据表
# facial_scan_result = models.RecommendationUserFacialScanResult.objects.filter(user=user).first()

# # 判断查询结果是否为空
# if not optometry or not lens or not facial_scan_result:
#     return R.failed(msg="用户数据不完整")

# # 构建查询结果
# search_result = {
#     # 推荐客户端用户基础信息表
#     'id': user.id,  # 用户ID,主键
#     'username': user.username,  # 用户名，唯一
#     'gender': user.gender,
#     'age_range': user.age_range,
#     # 推荐客户端用户验光信息表
#     'pupil_distance': optometry.pupil_distance,
#     'myopia_hyperopia_left': optometry.myopia_hyperopia_left,
#     'myopia_hyperopia_right': optometry.myopia_hyperopia_right,
#     'astigmatism_left': optometry.astigmatism_left,
#     'astigmatism_right': optometry.astigmatism_right,
#     # 推荐客户端用户镜片需求表
#     'refractive_index': lens.refractive_index,
#     'diameter': lens.diameter,
#     'density': lens.density,
#     # 推荐客户端用户人脸扫描数据表
#     'outer_canthic_diameter': facial_scan_result.outer_canthic_diameter,
#     'inner_canthic_diameter': facial_scan_result.inner_canthic_diameter,
#     'eye_width_left': facial_scan_result.eye_width_left,
#     'eye_width_right': facial_scan_result.eye_width_right,
#     'eye_height_left': facial_scan_result.eye_height_left,
#     'eye_height_right': facial_scan_result.eye_height_right,
#     'ala_nasi_width': facial_scan_result.ala_nasi_width,
#     'nasion_width': facial_scan_result.nasion_width,
#     'nose_height': facial_scan_result.nose_height,
#     'nose_pivot_angle': facial_scan_result.nose_pivot_angle,
#     'head_width': facial_scan_result.head_width,
#     'side_face_length_left': facial_scan_result.side_face_length_left,
#     'side_face_length_right': facial_scan_result.side_face_length_right,
#     'outer_canthic_ear_left': facial_scan_result.outer_canthic_ear_left,
#     'outer_canthic_ear_right': facial_scan_result.outer_canthic_ear_right,
#     'eyebrow_center_width': facial_scan_result.eyebrow_center_width,
#     'face_height': facial_scan_result.face_height,
#     'lip_width': facial_scan_result.lip_width,
#     'lip_height': facial_scan_result.lip_height,
#     'face_type': facial_scan_result.face_type,
#     'skin_color_type': facial_scan_result.skin_color_type,
# }








