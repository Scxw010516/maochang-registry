import os

from django.db import models
from application.models import BaseModel

"""
镜架材质表
"""
class EyeglassFrameMaterialType(BaseModel):
    material = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="镜架材质")
    def __str__(self):
        return '镜架材质：{}'.format(self.material)

"""
镜架颜色表
"""
class EyeglassFrameColorType(BaseModel):
    color = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="镜架颜色")
    def __str__(self):
        return '镜架颜色：{}'.format(self.color)
    
"""
镜架形状表
"""
class EyeglassFrameShapeType(BaseModel):
    shape = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="镜架形状")
    def __str__(self):
        return '镜架形状：{}'.format(self.shape)

"""
镜架基本信息表
"""
class EyeglassFrameEntry(BaseModel):
    sku = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="镜架SKU")
    brand = models.CharField(unique=False, blank=False, null=False, max_length=255, verbose_name="镜架品牌")
    model_type = models.CharField(unique=False, blank=False, null=False, max_length=255, verbose_name="镜架型号")
    price = models.DecimalField(max_digits=15, decimal_places=2, unique=False, blank=False, null=False, verbose_name="售价")
    material = models.ForeignKey(EyeglassFrameMaterialType, unique=False, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架材质")
    color = models.ForeignKey(EyeglassFrameColorType, unique=False, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架颜色")
    shape = models.ForeignKey(EyeglassFrameShapeType, unique=False, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架形状")
    isnosepad = models.BooleanField(unique=False, blank=False, null=False, verbose_name="是否带鼻托")
    stock = models.IntegerField(unique=False, blank=True, null=True, verbose_name="库存")
    lens_radian = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="撑片弧度")

"""
镜架风格类型表
"""
class EyeglassFrameStyleType(BaseModel):
    style = models.CharField(unique=True, blank=False,null=False, max_length=255, verbose_name="风格")

    def __str__(self):
        return '风格：{}'.format(self.style)

"""
镜架风格关联表
"""
class EyeglassFrameEntryStyle(BaseModel):
    entry = models.ForeignKey(EyeglassFrameEntry, unique=False, null=False, blank=False, on_delete=models.CASCADE, verbose_name='镜架基本信息')
    style = models.ForeignKey(EyeglassFrameStyleType, unique=False, null=False, blank=False, on_delete=models.CASCADE, verbose_name='镜架风格')

"""
镜架扫描结果表
"""
# 动态获取镜架三视图保存路径
def get_upload_eyeglass_path(instance, filename):
    filename = instance.entry.sku + '_' + filename
    return os.path.join('images/eyeglassframe/', filename)
# 镜架扫描结果表
class EyeglassFrameDetectionResult(BaseModel):
    # 镜架基本信息关联外键
    entry = models.OneToOneField(EyeglassFrameEntry, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name='镜架基本信息')
    # 镜架三视图相对路径
    frontview = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name='正视图')
    sideview = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name='侧视图')
    topview = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name='俯视图')
    # 镜架三视图背景相对路径
    frontview_bg = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name='正视图背景')
    sideview_bg = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name='侧视图背景')
    topview_bg = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name='俯视图背景')
    # 30个镜架扫描参数
    # 正视图扫描参数
    frame_height = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜框高度")
    frame_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜框宽度")
    pile_height_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左桩头高度")
    pile_height_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右桩头高度")
    frame_top_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜框顶部宽度")
    top_points = models.CharField(max_length=255, unique=False, blank=False, null=False, verbose_name="镜框左右最高点坐标（两组）")
    frame_rects = models.CharField(max_length=255, unique=False, blank=False, null=False, verbose_name="镜框左右矩形坐标及宽高（两组）")
    lens_width_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜圈宽度")
    lens_width_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜圈宽度")
    lens_height_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜圈高度")
    lens_height_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜圈高度")
    lens_diagonal_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜圈对角线长度")
    lens_diagonal_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜圈对角线长度")
    lens_area_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜圈面积")
    lens_area_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜圈面积")
    bridge_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="鼻梁宽度")
    lens_center_points = models.CharField(max_length=255, unique=False, blank=False, null=False, verbose_name="镜圈中心点坐标（两组）")
    lens_top_points = models.CharField(max_length=255, unique=False, blank=False, null=False, verbose_name="镜圈顶部点坐标（两组）")
    # 侧视图扫描参数
    vertical_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="垂俯角")
    forward_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="前倾角")
    temple_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜腿角")
    drop_length = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="垂长")
    # 俯视图扫描参数
    face_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="面弯")
    sagittal_angle_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左垂内角")
    sagittal_angle_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右垂内角")
    temple_length_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜腿长度")
    temple_length_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜腿长度")
    temporal_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="颞距")
    spread_angle_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜腿外张角")
    spread_angle_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜腿外张角")
    pile_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="桩头距离")
    # 镜架重量参数
    weight = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="重量")

###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

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
