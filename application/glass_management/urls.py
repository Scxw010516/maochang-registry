from django.urls import path  # 导入路径相关配置

from application.glass_management import views

urlpatterns = [
    ###################镜架采集与管理####################
    path('api/search-modeltype-sku', views.SearchModeltypeOrSKUView.as_view()), # post: 查询型号SKU
    path('api/search-sku', views.SearchSKUView.as_view()), # get: 查询镜架SKU
    path('api/delete-eyeglassframes', views.DeleteEyeglassFrameEntrysView.as_view()), # get: 删除镜架SKU
    path('api/save-new-eyeglassframe', views.SaveNewEyeglassFrameView.as_view()), # post: 添加新镜架
    path('api/save-edit-eyeglassframe', views.SaveEditEyeglassFrameView.as_view()), # post: 编辑镜架
    path('api/get-eyeglassframe-detail', views.GetEyeglassFrameDetailView.as_view()), # get: 获取镜架详情
    path('api/get-all-eyeglassframes_entrys', views.GetAllEyeglassFrameEntryView.as_view()), # get: 获取所有镜架基本信息
    path('api/get-all-brands', views.GetAllBrandsView.as_view()), # get: 获取所有品牌
    path('api/get-all-model-types', views.GetAllModelTypesView.as_view()), # get: 获取所有型号
    path('api/get-all-materials', views.GetAllMaterialsView.as_view()), # get: 获取所有材质
    path('api/get-all-colors', views.GetAllColorsView.as_view()), # get: 获取所有颜色
    path('api/get-all-shapes', views.GetAllShapesView.as_view()), # get: 获取所有形状
    path('api/get-all-styles', views.GetAllStylesView.as_view()), # get: 获取所有风格

    ###################以下为测试用####################
    path('api/add-style', views.AddStyle), # post: 添加风格
    path('api/add-style-list', views.AddStyleList), # post: 添加风格列表
    path('api/add-material', views.AddMaterial), # post: 添加材质
    path('api/add-material-list', views.AddMaterialList), # post: 添加材质列表
    path('api/add-color', views.AddColor), # post: 添加颜色
    path('api/add-color-list', views.AddColorList), # post: 添加颜色列表
    path('api/add-shape', views.AddShape), # post: 添加形状
    path('api/add-shape-list', views.AddShapeList), # post: 添加形状列表
]
