# +----------------------------------------------------------------------
# | DjangoAdmin敏捷开发框架 [ 赋能开发者，助力企业发展 ]
# +----------------------------------------------------------------------
# | 版权所有 2021~2024 北京DjangoAdmin研发中心
# +----------------------------------------------------------------------
# | Licensed LGPL-3.0 DjangoAdmin并不是自由软件，未经许可禁止去掉相关版权
# +----------------------------------------------------------------------
# | 官方网站: https://www.djangoadmin.cn
# +----------------------------------------------------------------------
# | 作者: @一米阳光 团队荣誉出品
# +----------------------------------------------------------------------
# | 版权和免责声明:
# | 本团队对该软件框架产品拥有知识产权（包括但不限于商标权、专利权、著作权、商业秘密等）
# | 均受到相关法律法规的保护，任何个人、组织和单位不得在未经本团队书面授权的情况下对所授权
# | 软件框架产品本身申请相关的知识产权，禁止用于任何违法、侵害他人合法权益等恶意的行为，禁
# | 止用于任何违反我国法律法规的一切项目研发，任何个人、组织和单位用于项目研发而产生的任何
# | 意外、疏忽、合约毁坏、诽谤、版权或知识产权侵犯及其造成的损失 (包括但不限于直接、间接、
# | 附带或衍生的损失等)，本团队不承担任何法律责任，本软件框架禁止任何单位和个人、组织用于
# | 任何违法、侵害他人合法利益等恶意的行为，如有发现违规、违法的犯罪行为，本团队将无条件配
# | 合公安机关调查取证同时保留一切以法律手段起诉的权利，本软件框架只能用于公司和个人内部的
# | 法律所允许的合法合规的软件产品研发，详细声明内容请阅读《框架免责声明》附件；
# +----------------------------------------------------------------------

from django.db import models

# Create your models here.
from application.models import BaseModel

from config.env import TABLE_PREFIX


# 城市模型
class City(BaseModel):
    # 城市区号
    city_code = models.CharField(null=False, max_length=6, verbose_name="城市区号", help_text="城市区号")
    # 行政编码
    area_code = models.CharField(null=False, max_length=20, verbose_name="行政编码", help_text="行政编码")
    # 上级行政编码
    parent_code = models.CharField(null=True, max_length=20, verbose_name="上级行政编码", help_text="上级行政编码")
    # 邮政编码
    zip_code = models.CharField(null=False, max_length=6, verbose_name="邮政编码", help_text="邮政编码")
    # 城市级别
    level = models.IntegerField(default=0, verbose_name="城市级别：1-省份 2-城市 3-县区 4-街道",
                                help_text="城市级别：1-省份 2-城市 3-县区 4-街道")
    # 上级城市ID
    pid = models.IntegerField(null=False, default=0, verbose_name="上级城市ID", help_text="上级城市ID")
    # 城市名称
    name = models.CharField(null=False, max_length=150, verbose_name="城市名称", help_text="城市名称")
    # 城市简称
    short_name = models.CharField(null=False, max_length=150, verbose_name="城市简称", help_text="城市简称")
    # 城市全称
    full_name = models.CharField(null=True, max_length=150, verbose_name="城市全称", help_text="城市全称")
    # 城市拼音
    pinyin = models.CharField(null=True, max_length=150, verbose_name="城市拼音", help_text="城市拼音")
    # 城市经度
    lng = models.CharField(null=True, max_length=150, verbose_name="城市经度", help_text="城市经度")
    # 城市纬度
    lat = models.CharField(null=True, max_length=150, verbose_name="城市纬度", help_text="城市纬度")

    class Meta:
        # 数据表名
        db_table = TABLE_PREFIX + "city"
        verbose_name = "城市表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '城市{}'.format(self.id)
