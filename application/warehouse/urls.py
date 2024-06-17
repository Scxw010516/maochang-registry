from django.urls import path  # 导入路径相关配置

from application.warehouse import views

urlpatterns = [
    ###################镜架仓库####################
    path('api/get-all-warehouses', views.GetAllWarehousesView.as_view()), # get: 查询所有镜架仓库
    path('api/add-warehouse', views.AddWarehouse), # post: 添加镜架仓库
]
