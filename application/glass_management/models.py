import os
import hashlib
from enum import Enum
from django.db import models
from application.models import BaseModel
from django.utils.deconstruct import deconstructible
from utils.obs.django_obs_storage import obs_storage

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
    # warehouse = models.ForeignKey(Warehouse, unique=False, blank=False, null=False, on_delete=models.CASCADE, verbose_name="所属仓库")
    warehouse = models.IntegerField(unique=False, blank=False, null=False, default=0, verbose_name="所属仓库")
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
    # AI试戴处理状态字段
    aiface_tryon_state = models.SmallIntegerField(choices=PROCESS_STATE_CHOICES, unique=False, blank=False, null=False, default=0, verbose_name="AI人脸试戴状态")
    # 试戴镜腿处理逻辑
    is_tryon_leg_auto = models.BooleanField(unique=False, blank=False, null=False, default=True, verbose_name="是否自动处理镜腿")
    # 试戴颜色处理逻辑
    is_tryon_beautify_origin = models.BooleanField(unique=False, blank=False, null=False, default=True, verbose_name="是否使用原始beautify进行试戴")
    # 是否启用
    is_active = models.BooleanField(default=True, verbose_name="是否启用")

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
    # 镜架基本信息关联外键（逻辑外键）
    entry_id = models.IntegerField(unique=True, blank=False, null=False, verbose_name="镜架基本信息ID")

    class Meta:
        indexes = [models.Index(fields=["entry_id"])]


class EyeglassFrameMillimeterMeasurement(EyeglassFrameMeasurement):
    """镜架毫米测量数据"""
    # 镜架基本信息关联外键（逻辑外键）
    entry_id = models.IntegerField(unique=True, blank=False, null=False, verbose_name="镜架基本信息ID")

    class Meta:
        indexes = [models.Index(fields=["entry_id"])]


class EyeglassFrameCalculation(BaseModel):
    """镜架计算数据 镜架推荐用"""
    # 镜架基本信息关联外键（逻辑外键）
    entry_id = models.IntegerField(unique=True, blank=False, null=False, verbose_name="镜架基本信息ID")
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
        indexes = [models.Index(fields=["entry_id"])]


class EyeglassFrameCoordinate(BaseModel):
    """镜架坐标数据"""
    # 镜架基本信息关联外键（逻辑外键）
    entry_id = models.IntegerField(unique=True, blank=False, null=False, verbose_name="镜架基本信息ID")
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
    ## 侧视图坐标数据，json_set
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
            "tail_point": [-1, -1],
            "top_left_point": [-1, -1], // 镜腿试戴选点，左上点
            "top_right_point": [-1, -1], // 镜腿试戴选点，右上点
            "bottom_left_point": [-1, -1], // 镜腿试戴选点，左下点
            "bottom_right_point": [-1, -1], // 镜腿试戴选点，右下点
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
        indexes = [models.Index(fields=["entry_id"])]


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


class BeautyType(str, Enum):
    """镜架的美化类型"""

    Y0 = "y0"
    Y1 = "y1"
    Y2 = "y2"
    Y3 = "y3"


@deconstructible
class UniversalPathGenerator:
    """通用文件路径生成器，支持类型枚举"""
    def __init__(self, base_dir, extension, path_type="default", type_identifier=None):
        self.base_dir = base_dir
        self.extension = extension
        self.path_type = path_type
        self.type_identifier = type_identifier  # 支持枚举值

    def __call__(self, instance, filename):
        """根据不同类型生成文件保存路径"""
        if self.path_type == "eyeglass":
            return self._generate_eyeglass_path(instance, filename)
        elif self.path_type == "aiface":
            return self._generate_aiface_path(instance, filename)
        elif self.path_type == "tryon_result":
            return self._generate_tryon_result_path(instance, filename)
        else:
            return self._generate_default_path(instance, filename)

    def _generate_eyeglass_path(self, instance, filename):
        """生成眼镜相关文件路径，支持类型标识符"""
        entry = EyeglassFrameEntry.objects.get(id=instance.entry_id, is_delete=False)
        sku_hash = hashlib.md5(entry.sku.encode("utf-8")).hexdigest()
        
        # 如果有类型标识符，将其包含在路径中
        if self.type_identifier is not None:
            sub_dir = os.path.join(
                str(self.type_identifier),
                sku_hash[:2],
                sku_hash[2:4],
                entry.sku
            )
            filename = f"{entry.sku}_{self.type_identifier}.{self.extension}"
        else:
            sub_dir = os.path.join(
                sku_hash[:2],
                sku_hash[2:4],
                entry.sku
            )
            filename = f"{entry.sku}.{self.extension}"
        
        return os.path.join(self.base_dir, sub_dir, filename)

    def _generate_aiface_path(self, instance, filename):
        """生成AI人脸文件路径"""
        name_hash = hashlib.md5(instance.name.encode("utf-8")).hexdigest()
        sub_dir = os.path.join(
            name_hash[:2],
            name_hash[2:4]
        )
        filename = f"{instance.name}_aiface.{self.extension}"
        return os.path.join(self.base_dir, sub_dir, filename)

    def _generate_tryon_result_path(self, instance, filename):
        """生成试戴结果文件路径"""
        entry_hash = hashlib.md5(str(instance.entry_id).encode("utf-8")).hexdigest()
        sub_dir = os.path.join(
            entry_hash[:2],
            entry_hash[2:4]
        )
        filename = f"{instance.entry_id}_{instance.face_id}_tryon_result.{self.extension}"
        return os.path.join(self.base_dir, sub_dir, filename)

    def _generate_default_path(self, instance, filename):
        """默认路径生成方法"""
        id_hash = hashlib.md5(str(instance.id).encode("utf-8")).hexdigest()
        sub_dir = os.path.join(
            id_hash[:2],
            id_hash[2:4]
        )
        return os.path.join(self.base_dir, sub_dir, filename)

class EyeglassFrameImage(BaseModel):
    """镜架图片数据"""
    # 镜架基本信息关联外键（逻辑外键）
    entry_id = models.IntegerField(unique=True, blank=False, null=False, verbose_name="镜架基本信息ID")
    # 镜架图片字段
    ## 镜架三视图
    frontview = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe", "jpg", "eyeglass", ViewType.FRONT.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="正视图")
    sideview = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe", "jpg", "eyeglass", ViewType.SIDE.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="侧视图")
    topview = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe", "jpg", "eyeglass", ViewType.TOP.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="俯视图")
    ## 镜架mask图 
    frame = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_mask", "png", "eyeglass", MaskType.FRAME.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="镜框mask图")
    lens = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_mask", "png", "eyeglass", MaskType.LENS.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="镜圈mask图")
    templeWf = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_mask", "png", "eyeglass", MaskType.TEMPLE.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="镜腿mask图")
    nose = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_mask", "png", "eyeglass", MaskType.NOSE.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="鼻托mask图")
    front = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_mask", "png", "eyeglass", MaskType.FRONT.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="正视图mask图")
    ## 镜架分割图(前景图)
    frontview_seg = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_seg", "png", "eyeglass", ViewType.FRONT.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="正视图分割图")
    sideview_seg = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_seg", "png", "eyeglass", ViewType.SIDE.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="侧视图分割图")
    ## 镜架美化图
    frontview_beautify = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_beautify", "png", "eyeglass", ViewType.FRONT.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="正视图美化图")
    sideview_beautify = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_beautify", "png", "eyeglass", ViewType.SIDE.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="侧视图美化图")
    frontview_beautify_processed = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_beautify_processed", "png", "eyeglass", ViewType.FRONT.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="外部处理，正视图美化图")
    sideview_beautify_processed = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_beautify_processed", "png", "eyeglass", ViewType.SIDE.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="外部处理，侧视图美化图")
    # 镜架美图
    beauty_y0 = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_beauty", "jpg", "eyeglass", BeautyType.Y0.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="镜架美图y0")
    beauty_y1 = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_beauty", "jpg", "eyeglass", BeautyType.Y1.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="镜架美图y1")
    beauty_y2 = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_beauty", "jpg", "eyeglass", BeautyType.Y2.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="镜架美图y2")
    beauty_y3 = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_beauty", "jpg", "eyeglass", BeautyType.Y3.value),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="镜架美图y3")

    class Meta:
        indexes = [models.Index(fields=["entry_id"])]

class EyeglassFramePreloadData(BaseModel):
    """镜架预加载数据 从excel加载"""
    # 导入信息字段
    batch_no = models.CharField(unique=False, blank=False, null=False, max_length=255, default=0,verbose_name="Excel导入的批次号",help_text="批次号格式：BATCH_YYYYMMDD_HHMMSS")

    # 镜架基本信息字段
    sku = models.CharField(unique=False, blank=False, null=False, max_length=255, verbose_name="镜架SKU")
    brand = models.CharField(unique=False, blank=True, null=True, max_length=255, verbose_name="镜架品牌")
    model_type = models.CharField(unique=False, blank=True, null=True, max_length=255, verbose_name="镜架型号")
    price = models.DecimalField(max_digits=15, decimal_places=2, unique=False, blank=True, null=True, verbose_name="售价")
    MATERIAL_CHOICES = (
        (0, "天然材料"),
        (1, "贵金属"),
        (2, "板材"),
        (3, "钢材"),
        (4, "钛材"),
        (5, "合金"),
        (6, "其他材料"),
    )
    material = models.SmallIntegerField(choices=MATERIAL_CHOICES, unique=False, blank=True, null=True, verbose_name="镜架材质")
    COLOR_CHOICES = (
        (0, "玳瑁色"),
        (1, "双色"),
        (2, "多彩"),
        (3, "深色"),
        (4, "浅色"),
    )
    color = models.SmallIntegerField(choices=COLOR_CHOICES, unique=False, blank=True, null=True, verbose_name="镜架颜色")
    SHAPE_CHOICES = (
        (0, "飞行员形"),
        (1, "不规则形"),
        (2, "圆形"),
        (3, "偏圆形"),
        (4, "方形"),
        (5, "偏方形"),
    )
    shape = models.SmallIntegerField(choices=SHAPE_CHOICES, unique=False, blank=True, null=True, verbose_name="镜架形状")
    isnosepad = models.BooleanField(unique=False, blank=True, null=True, verbose_name="是否带鼻托")
    IS_TRANSPARENT_CHOICES = (
        (0, "不透明"),
        (1, "全透明"),
        (2, "有色透明")
    )
    is_transparent = models.SmallIntegerField(choices=IS_TRANSPARENT_CHOICES, unique=False, blank=True, null=True, verbose_name="透明度")
    FRAME_TYPE_CHOICES = (
        (0, "全框"),
        (1, "半框"),
        (2, "无框"),
    )
    frame_type = models.SmallIntegerField(choices=FRAME_TYPE_CHOICES, unique=False, blank=True, null=True, verbose_name="镜框类型：0-全框 1-半框 2-无框")
    # 镜架尺寸参数
    lens_radian = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="撑片弧度")
    lens_width_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="镜圈宽度")
    bridge_width_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="鼻梁宽度")
    temple_length_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="镜腿长度")
    # 镜架库存参数
    stock = models.PositiveIntegerField(unique=False, blank=True, null=True, default=0, verbose_name="库存")

    class Meta:
        indexes = [models.Index(fields=["batch_no","sku"])]




class AIFace(BaseModel):
    """镜架管理端试戴用的AI人脸（3000*3000像素的jpg）"""
    name = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="人脸名称")
    pupil_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="瞳距") # 成年人在64左右
    image = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_tryon_aiface", "jpg", "aiface"),storage=obs_storage, unique=False, blank=False, null=True, verbose_name="人脸图片")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")



class EyeglassTryonResult(BaseModel):
    """眼镜试戴结果"""
    # 逻辑外键关联
    entry_id = models.IntegerField(verbose_name="镜架基本信息ID")
    face_id = models.IntegerField(verbose_name="AI人脸ID")
    # 试戴图片
    tryon_image = models.ImageField(upload_to=UniversalPathGenerator("images/eyeglassframe_tryon_result", "jpg", "tryon_result"),storage=obs_storage,unique=False, blank=False, null=True, verbose_name="试戴效果图")
    # 处理状态
    TRYON_STATE_CHOICES = (
        (0, "待处理"),
        (1, "处理中"),
        (2, "处理完成"),
        (3, "处理失败"),
    )
    tryon_state = models.SmallIntegerField(choices=TRYON_STATE_CHOICES, default=0, verbose_name="试戴处理状态")
    
    class Meta:
        unique_together = [('entry_id', 'face_id')]  # 确保每个眼镜-人脸组合唯一
        indexes = [models.Index(fields=["entry_id", "face_id"])]
