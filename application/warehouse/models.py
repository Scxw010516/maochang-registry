import os

from django.db import models
from application.models import BaseModel

"""
镜架仓库表
"""
class Warehouse(BaseModel):
    # 仓库名称
    warehouse = models.CharField(unique=True, blank=False, null=False, max_length=255, verbose_name="仓库名称")
    # 仓库地址
    address = models.CharField(unique=False, blank=False, null=False, max_length=255, verbose_name="仓库地址")