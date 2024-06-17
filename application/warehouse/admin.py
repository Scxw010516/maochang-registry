from django.contrib import admin

# Register your models here.
from application.warehouse.models import Warehouse # 镜架材质类型表

admin.site.register(Warehouse) # 镜架材质类型表

