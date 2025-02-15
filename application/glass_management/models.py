import os

from django.db import models
from application.models import BaseModel
from application.warehouse.models import Warehouse

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
    # 镜架基本信息参数
    brand = models.CharField(unique=False, blank=False, null=False, max_length=255, verbose_name="镜架品牌")
    model_type = models.CharField(unique=False, blank=False, null=False, max_length=255, verbose_name="镜架型号")
    price = models.DecimalField(max_digits=15, decimal_places=2, unique=False, blank=False, null=False, verbose_name="售价")
    material = models.ForeignKey(EyeglassFrameMaterialType, unique=False, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架材质")
    color = models.ForeignKey(EyeglassFrameColorType, unique=False, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架颜色")
    shape = models.ForeignKey(EyeglassFrameShapeType, unique=False, blank=False, null=False, on_delete=models.CASCADE, verbose_name="镜架形状")
    isnosepad = models.BooleanField(unique=False, blank=False, null=False, verbose_name="是否带鼻托")
    # 镜架尺寸参数
    lens_radian = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False, null=False, verbose_name="撑片弧度")
    lens_width_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="镜圈宽度")
    bridge_width_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="鼻梁宽度")
    temple_length_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="镜腿长度")
    # 镜架库存参数
    stock = models.IntegerField(unique=False, blank=True, null=True, verbose_name="库存")
    warehouse = models.ForeignKey(Warehouse, unique=False, blank=False, null=False, on_delete=models.CASCADE, verbose_name="所属仓库")
    # 计算任务
    calc_status = models.CharField(unique=False, blank=True, null=True,  max_length=255, verbose_name="计算任务")

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
    frontview = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=True, verbose_name='正视图')
    sideview = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=True, verbose_name='侧视图')
    topview = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=True, verbose_name='俯视图')
    # 镜架三视图背景相对路径
    # frontview_bg = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name='正视图背景')
    # sideview_bg = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name='侧视图背景')
    # topview_bg = models.ImageField(upload_to=get_upload_eyeglass_path, unique=False, blank=False, null=False, verbose_name='俯视图背景')
    # 30个镜架扫描参数
    # 正视图扫描参数
    frame_height = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="镜框高度")
    frame_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="镜框宽度")
    pile_height_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="左桩头高度")
    pile_height_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="右桩头高度")
    frame_top_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="镜框顶部宽度")
    top_points = models.CharField(max_length=255, unique=False, blank=False,  null=True, verbose_name="镜框左右最高点坐标（两组）")
    frame_rects = models.CharField(max_length=255, unique=False, blank=False,  null=True, verbose_name="镜框左右矩形坐标及宽高（两组）")
    lens_width_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="左镜圈宽度")
    lens_width_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="右镜圈宽度")
    lens_height_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="左镜圈高度")
    lens_height_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="右镜圈高度")
    lens_diagonal_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="左镜圈对角线长度")
    lens_diagonal_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="右镜圈对角线长度")
    lens_area_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="左镜圈面积")
    lens_area_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="右镜圈面积")
    bridge_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="鼻梁宽度")
    lens_center_points = models.CharField(max_length=255, unique=False, blank=False,  null=True, verbose_name="镜圈中心点坐标（两组）")
    lens_top_points = models.CharField(max_length=255, unique=False, blank=False,  null=True, verbose_name="镜圈顶部点坐标（两组）")
    # 侧视图扫描参数
    vertical_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="垂俯角")
    forward_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="前倾角")
    temple_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="镜腿角")
    drop_length = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="垂长")
    # 俯视图扫描参数
    face_angle = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="面弯")
    sagittal_angle_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="左垂内角")
    sagittal_angle_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="右垂内角")
    temple_length_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="左镜腿长度")
    temple_length_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="右镜腿长度")
    temporal_width = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="颞距")
    spread_angle_left = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="左镜腿外张角")
    spread_angle_right = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="右镜腿外张角")
    pile_distance = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="桩头距离")
    # 镜架重量参数
    weight = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=False,  null=True, verbose_name="重量")


"""
镜架导入数据表
"""
class EyeglassFrameDataFromExcel(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    sku = models.CharField(unique=True, blank=False, null=False, max_length=100, verbose_name="镜架SKU")
    brand = models.CharField(unique=False, blank=True, null=True, max_length=255, verbose_name="镜架品牌")
    model_type = models.CharField(unique=False, blank=True, null=True, max_length=255, verbose_name="镜架型号")
    price = models.DecimalField(max_digits=10, decimal_places=2, unique=False, blank=True, null=True, verbose_name="售价")
    material = models.CharField(unique=False, blank=True, null=True, max_length=255, verbose_name="镜架材质")
    color = models.CharField(unique=False, blank=True, null=True, max_length=255, verbose_name="镜架颜色")
    shape = models.CharField(unique=False, blank=True, null=True, max_length=255, verbose_name="镜架形状")
    stock = models.IntegerField(unique=False, blank=True, null=True, verbose_name="库存")
    lens_width_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="镜圈宽度")
    bridge_width_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="鼻梁宽度")
    temple_length_st = models.DecimalField(max_digits=15, decimal_places=4, unique=False, blank=True, null=True, verbose_name="镜腿长度")
    # 计算任务
    calc_status = models.CharField(unique=False, blank=True, null=True,  max_length=255, verbose_name="计算任务")
    
    class Meta:
        indexes = [
            models.Index(fields=['sku']),  # 为sku字段添加索引
            models.Index(fields=['model_type']),  # 为model_type字段添加索引
        ]