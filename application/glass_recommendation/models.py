import os

from django.db import models
from application.models import BaseModel


"""
推荐客户端用户表
"""
class RecommendationUser(BaseModel):
    # 用户识别码
    username = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="用户识别码")

"""
推荐客户端用户基础信息表
"""
class RecommendationUserBaseInfo(BaseModel):
    # 用户识别码
    user = models.OneToOneField(RecommendationUser, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="用户")
    # 用户基础信息
    # 性别：0-保密 1-男 2-女 
    GENDER_CHOICES = (
        # (0, "保密"),
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(choices=GENDER_CHOICES,unique=False, blank=False, null=False, verbose_name="性别：0-保密 1-男 2-女", help_text="性别：0-保密 1-男 2-女")
    # 年龄段：0-保密 1-14岁以下 2-15-25岁 3-26-35岁 4-36-45岁 5-46-60岁 6-61岁以上
    AGERANGE_CHOICES = (
        # (0, "保密"),
        (1, "14岁以下"),
        (2, "15-25岁"),
        (3, "26-35岁"),
        (4, "36-45岁"),
        (5, "46-60岁"),
        (6, "61岁以上"),
    )
    age_range = models.SmallIntegerField(choices=AGERANGE_CHOICES, unique=False, blank=False, null=False, verbose_name="年龄段：0-保密 1-14岁以下 2-15-25岁 3-26-35岁 4-36-45岁 5-46-60岁 6-61岁以上", help_text="年龄段：0-保密 1-14岁以下 2-15-25岁 3-26-35岁 4-36-45岁 5-46-60岁 6-61岁以上")
    # 精确年龄
    age = models.IntegerField(unique=False, blank=False, null=False, verbose_name="年龄")

"""
推荐客户端用户人脸图像表
"""
# 动态获取镜架三视图保存路径
def get_upload_userface_path(instance, filename):
    filename = instance.user.username + '_' + filename
    return os.path.join('images/userface/', filename)
class RecommendationUserFacialImage(BaseModel):
    # 用户识别码
    user = models.OneToOneField(RecommendationUser, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="用户")
    # 用户人脸图像
    frontview = models.ImageField(upload_to=get_upload_userface_path, unique=False, blank=False, null=False, verbose_name="用户人脸正视图")
    leftview = models.ImageField(upload_to=get_upload_userface_path, unique=False, blank=False, null=False, verbose_name="用户人脸左视图")
    rightview = models.ImageField(upload_to=get_upload_userface_path, unique=False, blank=False, null=False, verbose_name="用户人脸右视图")


"""
推荐客户端用户验光信息表
"""
class RecommendationUserOptometry(BaseModel):
    # 用户识别码
    user = models.OneToOneField(RecommendationUser, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="用户")
    # 用户验光信息
    # 瞳距
    pupil_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="瞳距")
    # 左眼屈光度（近视或远视）
    myopia_hyperopia_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左眼屈光度")
    # 右眼屈光度（近视或远视）
    myopia_hyperopia_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右眼屈光度")
    # 左眼屈光度（散光度）
    astigmatism_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左眼散光度")
    # 右眼屈光度（散光度）
    astigmatism_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右眼散光度")

"""
推荐客户端用户镜片需求表
"""
class RecommendationUserLens(BaseModel):
    # 用户识别码
    user = models.OneToOneField(RecommendationUser, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="用户")
    # 用户镜片信息
    # 镜片折射率
    refractive_index = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜片折射率")
    # 镜片直径
    diameter = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜片直径")
    # 镜片密度
    density = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜片密度")


"""
推荐客户端用户人脸扫描数据表
"""
class RecommendationUserFacialScanResult(BaseModel):
    # 用户识别码
    user = models.OneToOneField(RecommendationUser, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="用户")
    # 用户人脸数据
    outer_canthic_diameter = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="外眼角间距")
    inner_canthic_diameter = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="内眼角间距")
    eye_width_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左眼宽")
    eye_width_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右眼宽")
    eye_height_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左眼高")
    eye_height_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右眼高")
    ala_nasi_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="鼻翼宽")
    nasion_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="鼻根宽")
    nose_height = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="鼻高")
    nose_pivot_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="鼻基准角")
    head_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="头宽")
    side_face_length_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左侧面长")
    side_face_length_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右侧面长")
    outer_canthic_ear_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左外眼角耳距")
    outer_canthic_ear_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右外眼角耳距")
    eyebrow_center_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="眉上顶点距")
    face_height = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="脸高")
    lip_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="嘴唇宽")
    lip_height = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="嘴唇高")
    # 脸型：0-菱形脸 1-圆脸 2-方脸 3-长脸 4-心形脸 5-鹅蛋脸
    FACETYPE_CHOICES = (
        (0, "菱形脸"),
        (1, "圆脸"),
        (2, "方脸"),
        (3, "长脸"),
        (4, "心形脸"),
        (5, "鹅蛋脸"),
    )
    face_type = models.SmallIntegerField(choices=FACETYPE_CHOICES, unique=False, blank=False, null=False, verbose_name="脸型：0-菱形脸 1-圆脸 2-方脸 3-长脸 4-心形脸 5-鹅蛋脸")
    # 肤色：0-偏黑 1-适中 2-偏白
    SKINCOLOR_CHOICES = (
        (0, "偏黑"),
        (1, "适中"),
        (2, "偏白"),
    )
    skin_color_type = models.SmallIntegerField(choices=SKINCOLOR_CHOICES, unique=False, blank=False, null=False, verbose_name="肤色：0-偏黑 1-适中 2-偏白")

    

"""
推荐请求记录表（需加上推荐结果）
"""
class EyeglassFrameRecommendationRequest(BaseModel):
    # 用户人脸数据
    facial_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    nose_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    left_ear_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    right_ear_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    # 默认值63
    iris_center_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    left_eye_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    right_eye_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    left_eye_height = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    right_eye_height = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    inner_eyecorner_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    outter_eyecorner_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False)
    face_type = models.CharField(unique=False, blank=True, max_length=255)
    skin_color = models.CharField(unique=False, blank=True, max_length=255)
    # 用户验光信息
    pupil_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True)
    myopia_left = models.BigIntegerField(unique=False, blank=True)
    myopia_right = models.BigIntegerField(unique=False, blank=True)
    astigmatism_left = models.BigIntegerField(unique=False, blank=True)
    astigmatism_right = models.BigIntegerField(unique=False, blank=True)
    lens_weight = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True)
    # 用户个人信息
    gender = models.CharField(unique=False, blank=True, max_length=255)
    age = models.SmallIntegerField(unique=False, blank=True)
    career = models.CharField(unique=False, blank=True, max_length=255)
    price_max = models.BigIntegerField(unique=False, blank=True)
    price_min = models.BigIntegerField(unique=False, blank=True)
    # 用户筛选条件
    style_list = models.CharField(unique=False, blank=True, max_length=255)
    brand_list = models.CharField(unique=False, blank=True, max_length=255)
    material_list = models.CharField(unique=False, blank=True, max_length=255)
