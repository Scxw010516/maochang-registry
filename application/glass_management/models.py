import os
import hashlib
from enum import Enum
from django.db import models
from application.models import BaseModel
from application.warehouse.models import Warehouse
from django.utils.deconstruct import deconstructible

class EyeglassFrameEntry(BaseModel):
    """镜架基本信息表"""
    sku = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="镜架SKU")
    # 镜架基本信息参数
    brand = models.CharField(unique=False, blank=False, null=False, max_length=255, verbose_name="镜架品牌")
    model_type = models.CharField(unique=False, blank=False, null=False, max_length=255, verbose_name="镜架型号")
    price = models.DecimalField(max_digits=15, decimal_places=2, unique=False, blank=False, null=False, verbose_name="售价")
    MATERIAL_CHOICES = (
        (0, "天然材料"), 
        (1, "贵金属"), 
        (2, "板材"), 
        (3, "钢材"),
        (4, "钛材"), 
        (5, "合金"), 
        (6, "其他材料"),
    )
    material = models.SmallIntegerField(choices=MATERIAL_CHOICES, unique=False, blank=False, null=False, verbose_name="镜架材质")
    COLOR_CHOICES = (
        (0, "玳瑁色"), 
        (1, "双色"), 
        (2, "多彩"), 
        (3, "深色"), 
        (4, "浅色"),
    )
    color = models.SmallIntegerField(choices=COLOR_CHOICES, unique=False, blank=False, null=False, verbose_name="镜架颜色")
    SHAPE_CHOICES = (
        (0, "飞行员形"), 
        (1, "不规则形"), 
        (2, "圆形"),
        (3, "偏圆形"), 
        (4, "方形"), 
        (5, "偏方形"),
    )
    shape = models.SmallIntegerField(choices=SHAPE_CHOICES, unique=False, blank=False, null=False, verbose_name="镜架形状")
    isnosepad = models.BooleanField(unique=False, blank=False, null=False, verbose_name="是否带鼻托")
    IS_TRANSPARENT_CHOICES = (
        (0, "不透明"), 
        (1, "全透明"), 
        (2, "有色透明")
    )
    is_transparent = models.IntegerField(choices=IS_TRANSPARENT_CHOICES, unique=False, blank=False, null=False, verbose_name="是否透明")
    FRAME_TYPE_CHOICES = (
        (0, "全框"),
        (1, "半框"),
        (2, "无框"),
    )
    frame_type = models.IntegerField(choices=FRAME_TYPE_CHOICES, unique=False, blank=False, null=False, verbose_name="镜框类型：0-全框 1-半框 2-无框")
    # 镜架尺寸参数
    lens_radian = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="撑片弧度")
    lens_width_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="镜圈宽度")
    bridge_width_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="鼻梁宽度")
    temple_length_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="镜腿长度")
    # 镜架重量参数
    weight = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="重量")
    # 镜架库存参数
    stock = models.PositiveIntegerField(unique=False, blank=False, null=False, default=0, verbose_name="库存")
    warehouse = models.ForeignKey(Warehouse, unique=False, blank=False, null=False, on_delete=models.CASCADE, verbose_name="所属仓库")
    # 镜架后台处理状态字段
    PROCESS_STATE_CHOICES = (
        (0, "待计算"),
        (1, "计算中"),
        (2, "计算完成"),
        (3, "计算失败"),
    )
    pixel_measurement_state = models.SmallIntegerField(choices=PROCESS_STATE_CHOICES, unique=False, blank=False, null=False, default=0, verbose_name="像素测量数据状态")
    millimeter_measurement_state = models.SmallIntegerField(choices=PROCESS_STATE_CHOICES, unique=False, blank=False, null=False, default=0, verbose_name="毫米测量数据状态")
    calculation_state = models.SmallIntegerField(choices=PROCESS_STATE_CHOICES, unique=False, blank=False, null=False, default=0, verbose_name="计算数据状态")
    coordinate_state = models.SmallIntegerField(choices=PROCESS_STATE_CHOICES, unique=False, blank=False, null=False, default=0, verbose_name="坐标数据状态")
    image_mask_state = models.SmallIntegerField(choices=PROCESS_STATE_CHOICES, unique=False, blank=False, null=False, default=0, verbose_name="mask图片数据状态")
    image_seg_state = models.SmallIntegerField(choices=PROCESS_STATE_CHOICES, unique=False, blank=False, null=False, default=0, verbose_name="分割图片数据状态")
    image_beautify_state = models.SmallIntegerField(choices=PROCESS_STATE_CHOICES, unique=False, blank=False, null=False, default=0, verbose_name="美化图片数据状态")

    @property
    def is_fully_processed(self):
        """检查是否所有处理都完成"""
        return all([
            self.pixel_measurement_state == 2,
            self.millimeter_measurement_state == 2,
            self.calculation_state == 2,
            self.coordinate_state == 2,
            self.image_mask_state == 2,
            self.image_seg_state == 2,
            self.image_beautify_state == 2,
        ])

    class Meta:
        indexes = [models.Index(fields=["id", "sku"])]


class EyeglassFrameMeasurement(BaseModel):
    """镜架测量数据基类"""
    # 正视图扫描参数
    frame_height = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="镜框高度")
    frame_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="镜框宽度")
    pile_height_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="左桩头高度")
    pile_height_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="右桩头高度")
    frame_top_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="镜框顶部宽度")
    lens_width_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="左镜圈宽度")
    lens_width_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="右镜圈宽度")
    lens_height_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="左镜圈高度")
    lens_height_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="右镜圈高度")
    lens_diagonal_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="左镜圈对角线长度")
    lens_diagonal_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="右镜圈对角线长度")
    lens_area_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="左镜圈面积")
    lens_area_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="右镜圈面积")
    bridge_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="鼻梁宽度")
    # 侧视图扫描参数
    vertical_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="垂俯角")
    forward_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="前倾角")
    temple_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="镜腿角")
    drop_length = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="垂长")
    # 俯视图扫描参数
    face_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="面弯")
    sagittal_angle_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="左垂内角")
    sagittal_angle_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="右垂内角")
    temple_length_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="左镜腿长度")
    temple_length_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="右镜腿长度")
    temporal_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="颞距")
    spread_angle_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="左镜腿外张角")
    spread_angle_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="右镜腿外张角")
    pile_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="桩头距离")

    class Meta:
        # 抽象类，不生成表
        abstract = True

class EyeglassFramePixelMeasurement(EyeglassFrameMeasurement):
    """镜架像素测量数据"""
    # 镜架基本信息关联外键
    entry = models.OneToOneField(EyeglassFrameEntry, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架基本信息")

    class Meta:
        indexes = [models.Index(fields=["entry"])]


class EyeglassFrameMillimeterMeasurement(EyeglassFrameMeasurement):
    """镜架毫米测量数据"""
    # 镜架基本信息关联外键
    entry = models.OneToOneField(EyeglassFrameEntry, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架基本信息")

    class Meta:
        indexes = [models.Index(fields=["entry"])]


class EyeglassFrameCalulation(BaseModel):
    """镜架计算数据"""
    # 镜架基本信息关联外键
    entry = models.OneToOneField(EyeglassFrameEntry, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架基本信息")
    # 计算数据，推荐用的二次计算数据
    FRAME_SIZE_CHOICES = (
        (0, "大框"),
        (1, "中框"),
        (2, "小框"),
    )
    frame_size = models.SmallIntegerField(choices=FRAME_SIZE_CHOICES, unique=False, blank=False, null=True, verbose_name="镜框大小")
    left_curvature = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="左平均曲率")
    right_curvature = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="右平均曲率")
    left_factors = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="左形状因子")
    right_factors = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="右形状因子")
    height_width_proportion = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=True, verbose_name="高宽比")

    class Meta:
        indexes = [models.Index(fields=["entry"])]


class EyeglassFrameCoordinate(BaseModel):
    """镜架坐标数据"""
    # 镜架基本信息关联外键
    entry = models.OneToOneField(EyeglassFrameEntry, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架基本信息")
    # 镜架坐标数据
    ## 正视图坐标数据
    front_points = models.JSONField(
        default=dict,
        blank=True,
        null=False,
        verbose_name="正视图坐标数据",
        help_text="""
        存储格式示例：
        {
            "frame_bounding_points": [[-1, -1], [-1, -1]],
            "pile_points": [[-1, -1], [-1, -1]],
            "lens_center_points": [[-1, -1], [-1, -1]],
            "lens_bounding_points": [[[-1, -1], [-1, -1]], [[-1, -1], [-1, -1]]],
            "lens_diagonal_points": [[[-1, -1], [-1, -1]], [[-1, -1], [-1, -1]]],
            "lens_top_points": [[-1, -1], [-1, -1]],
            "top_points": [[-1, -1], [-1, -1]],
            "bottom_points": [[-1, -1], [-1, -1]],
            "lens_bottom_points": [[-1, -1], [-1, -1]],
            "lens_side_points": [[[-1, -1], [-1, -1]], [[-1, -1], [-1, -1]]]
        }
        """
    )
    ## 侧视图坐标数据
    left_points = models.JSONField(
        default=dict,
        blank=True,
        null=False,
        verbose_name="侧视图坐标数据",
        help_text="""
        存储格式示例：
        {
            "head_point": [-1, -1],
            "down_point": [-1, -1],
            "turning_point": [-1, -1],
            "tail_point": [-1, -1]
        }
        """
    )
    ## 俯视图坐标数据
    up_points = models.JSONField(
        default=dict,
        blank=True,
        null=False,
        verbose_name="俯视图坐标数据",
        help_text="""
        存储格式示例：
        {
            "pile_points": [[-1, -1], [-1, -1]],
            "temporal_points": [[-1, -1], [-1, -1]],
            "turning_points": [[-1, -1], [-1, -1]],
            "tail_points": [[-1, -1], [-1, -1]],
            "bridge_point": [-1, -1]
        }
        """
    )
    class Meta:
        indexes = [models.Index(fields=["entry"])]


class ViewType(int, Enum):
    """镜架的视图类型"""
    TOP = 0
    FRONT = 1
    SIDE = 2

class MaskType(str, Enum):
    """镜架的mask类型"""
    FRAME = "frame"
    LENS = "lens"
    TEMPLE = "templeWf"
    NOSE = "nose"
    FRONT = "front"

@deconstructible # 使类可序列化
class EyeglassPathGenerator:
    def __init__(self, base_dir, type_identifier, extension):
        # 保存路径的基础目录
        self.base_dir = base_dir
        # 视图类型标识符
        self.type_identifier = type_identifier
        # 文件扩展名
        self.extension = extension

    def __call__(self, instance, filename):
        """生成文件保存路径"""
        # 生成sku的hash值
        sku_hash = hashlib.md5(instance.entry.sku.encode("utf-8")).hexdigest()
        # 使用hash值的前两位作为子目录，避免一个目录下文件过多
        sub_dir = os.path.join(
            str(self.type_identifier),
            sku_hash[:2],
            sku_hash[2:4],
            instance.entry.sku
        )
        filename = f"{instance.entry.sku}_{self.type_identifier}.{self.extension}"
        return os.path.join(self.base_dir, sub_dir, filename)

class EyeglassFrameImage(BaseModel):
    """镜架图片数据"""
    # 镜架基本信息关联外键
    entry = models.OneToOneField(EyeglassFrameEntry, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架基本信息")
    # 镜架图片字段
    ## 镜架三视图
    frontview = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe", ViewType.FRONT,"jpg"), unique=False, blank=False, null=True, verbose_name="正视图")
    sideview = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe", ViewType.SIDE,"jpg"), unique=False, blank=False, null=True, verbose_name="侧视图")
    topview = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe", ViewType.TOP,"jpg"), unique=False, blank=False, null=True, verbose_name="俯视图")
    ## 镜架mask图 
    frame = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe_mask", MaskType.FRAME,"png"), unique=False, blank=False, null=True, verbose_name="镜框mask图")
    lens = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe_mask", MaskType.LENS,"png"), unique=False, blank=False, null=True, verbose_name="镜圈mask图")
    templeWf = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe_mask", MaskType.TEMPLE,"png"), unique=False, blank=False, null=True, verbose_name="镜腿mask图")
    nose = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe_mask", MaskType.NOSE,"png"), unique=False, blank=False, null=True, verbose_name="鼻托mask图")
    front = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe_mask", MaskType.FRONT,"png"), unique=False, blank=False, null=True, verbose_name="正视图mask图")
    ## 镜架分割图(前景图)
    frontview_seg = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe_seg", ViewType.FRONT,"png"), unique=False, blank=False, null=True, verbose_name="正视图分割图")
    sideview_seg = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe_seg", ViewType.SIDE,"png"), unique=False, blank=False, null=True, verbose_name="侧视图分割图")
    ## 镜架美化图
    frontview_beautify = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe_beautify", ViewType.FRONT,"png"), unique=False, blank=False, null=True, verbose_name="正视图美化图")
    sideview_beautify = models.ImageField(upload_to=EyeglassPathGenerator("images/eyeglassframe_beautify", ViewType.SIDE,"png"), unique=False, blank=False, null=True, verbose_name="侧视图美化图")

    class Meta:
        indexes = [models.Index(fields=["entry"])]

# def get_upload_eyeglass_view_path_with_type(view_type: int):
#     """动态获取镜架三视图保存路径"""
#     def wrapper(instance, filename):
#         """闭包函数"""
#         # 生成sku的hash值
#         sku_hash = hashlib.md5(instance.entry.sku.encode("utf-8")).hexdigest()
#         # 使用hash值的前两位作为子目录，避免一个目录下文件过多
#         sub_dir = os.path.join(str(view_type), sku_hash[:2], sku_hash[2:4], instance.entry.sku)
#         filename = f"{instance.entry.sku}_{view_type}.jpg"
#         return os.path.join("images/eyeglassframe/", sub_dir, filename)
#     return wrapper

# def get_upload_eyeglass_mask_path_with_type(mask_type: str):
#     """动态获取镜架mask图保存路径"""
#     def wrapper(instance, filename):
#         """闭包函数"""
#         # 生成sku的hash值
#         sku_hash = hashlib.md5(instance.entry.sku.encode("utf-8")).hexdigest()
#         # 使用hash值的前两位作为子目录，避免一个目录下文件过多
#         sub_dir = os.path.join(mask_type, sku_hash[:2], sku_hash[2:4], instance.entry.sku)
#         filename = f"{instance.entry.sku}_{mask_type}.jpg"
#         return os.path.join("images/eyeglassframe_mask/", sub_dir, filename)
#     return wrapper

# def get_upload_eyeglass_seg_path_with_type(seg_type: int):
#     """动态获取镜架分割图保存路径"""
#     def wrapper(instance, filename):
#         """闭包函数"""
#         # 生成sku的hash值
#         sku_hash = hashlib.md5(instance.entry.sku.encode("utf-8")).hexdigest()
#         # 使用hash值的前两位作为子目录，避免一个目录下文件过多
#         sub_dir = os.path.join(str(seg_type), sku_hash[:2], sku_hash[2:4], instance.entry.sku)
#         filename = f"{instance.entry.sku}_{seg_type}.jpg"
#         return os.path.join("images/eyeglassframe_seg/", sub_dir, filename)
#     return wrapper

# def get_upload_eyeglass_beautify_path_with_type(beautify_type: int):
#     """动态获取镜架美化图保存路径"""
#     def wrapper(instance, filename):
#         """闭包函数"""
#         # 生成sku的hash值
#         sku_hash = hashlib.md5(instance.entry.sku.encode("utf-8")).hexdigest()
#         # 使用hash值的前两位作为子目录，避免一个目录下文件过多
#         sub_dir = os.path.join(str(beautify_type), sku_hash[:2], sku_hash[2:4], instance.entry.sku)
#         filename = f"{instance.entry.sku}_{beautify_type}.jpg"
#         return os.path.join("images/eyeglassframe_beautify/", sub_dir, filename)
#     return wrapper

# # 镜架扫描结果表
# class EyeglassFrameDetectionResult(BaseModel):
#     # 镜架基本信息关联外键
#     entry = models.OneToOneField(EyeglassFrameEntry, unique=True, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架基本信息")
#     # 镜架图片字段
#     ## 镜架三视图相对路径
#     frontview = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name="正视图")
#     sideview = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name="侧视图")
#     topview = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name="俯视图")
#     ## 正视图分隔结果图像相对路径
#     frontview_seg = models.ImageField(upload_to=get_upload_eyeglass_seg_path, unique=False, blank=True, null=True, verbose_name="正视图分隔结果")
#     sideview_seg = models.ImageField(upload_to=get_upload_eyeglass_seg_path, unique=False, blank=True, null=True, verbose_name="侧视图分隔结果")
#     ## 镜架三视图背景相对路径
#     frontview_bg = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name="正视图背景")
#     sideview_bg = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name="侧视图背景")
#     topview_bg = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name="俯视图背景")
#     # 镜架参数字段
#     ## 正视图扫描参数
#     frame_height = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜框高度")
#     frame_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜框宽度")
#     pile_height_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左桩头高度")
#     pile_height_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右桩头高度")
#     frame_top_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜框顶部宽度")
#     lens_width_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜圈宽度")
#     lens_width_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜圈宽度")
#     lens_height_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜圈高度")
#     lens_height_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜圈高度")
#     lens_diagonal_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜圈对角线长度")
#     lens_diagonal_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜圈对角线长度")
#     lens_area_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜圈面积")
#     lens_area_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜圈面积")
#     bridge_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="鼻梁宽度")
#     ## 侧视图扫描参数
#     vertical_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="垂俯角")
#     forward_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="前倾角")
#     temple_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="镜腿角")
#     drop_length = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="垂长")
#     ## 俯视图扫描参数
#     face_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="面弯")
#     sagittal_angle_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左垂内角")
#     sagittal_angle_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右垂内角")
#     temple_length_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜腿长度")
#     temple_length_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜腿长度")
#     temporal_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="颞距")
#     spread_angle_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="左镜腿外张角")
#     spread_angle_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="右镜腿外张角")
#     pile_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="桩头距离")

#     top_points = models.CharField(max_length=255, unique=False, blank=False, null=False, verbose_name="镜框左右最高点坐标（两组）")
#     frame_rects = models.CharField(max_length=255, unique=False, blank=False, null=False, verbose_name="镜框左右矩形坐标及宽高（两组）")
#     lens_center_points = models.CharField(max_length=255, unique=False, blank=False, null=False, verbose_name="镜圈中心点坐标（两组）")
#     lens_top_points = models.CharField(max_length=255, unique=False, blank=False, null=False, verbose_name="镜圈顶部点坐标（两组）")
#     # 镜架重量字段
#     weight = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="重量")

#     class Meta:
#         indexes = [models.Index(fields=["entry"])]

# """
# 镜架风格类型表
# """
# class EyeglassFrameStyleType(BaseModel):
#     style = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="风格")

# """
# 镜架风格关联表
# """
# class EyeglassFrameEntryStyle(BaseModel):
#     entry = models.ForeignKey(EyeglassFrameEntry, unique=False, null=False, blank=False, on_delete=models.CASCADE, verbose_name="镜架基本信息")
#     style = models.ForeignKey(EyeglassFrameStyleType, unique=False, null=False, blank=False, on_delete=models.CASCADE, verbose_name="镜架风格")

# """
# 镜架材质表
# """
# class EyeglassFrameMaterialType(BaseModel):
#     material = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="镜架材质")

# """
# 镜架颜色表
# """
# class EyeglassFrameColorType(BaseModel):
#     color = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="镜架颜色")

# """
# 镜架形状表
# """
# class EyeglassFrameShapeType(BaseModel):
#     shape = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="镜架形状")