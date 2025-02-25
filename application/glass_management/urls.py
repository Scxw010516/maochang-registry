from django.urls import path  # 导入路径相关配置

from application.glass_management import views
# from .data_import import generate_testing_data_for_customer_ui_v2, generate_testing_data_for_registry_ui

urlpatterns = [
    ###################古老API，待优化####################
    # path('video-feed', video_feed, name='video_feed'),
    # path('api/generate-testing-data-for-customer-ui', views.generate_testing_data_for_customer_ui),
    # path('api/generate-testing-data-for-customer-ui-v2', generate_testing_data_for_customer_ui_v2),
    # path('api/generate-testing-data-for-registry-ui', generate_testing_data_for_registry_ui),
    # path('api/all-brands', views.all_brands),
	# path('api/all-model-types', views.all_model_types),
	# path('api/all-materials', views.all_materials),
	# path('api/all-styles', views.all_styles),
    # path('api/list-all-eyeglass-frames', views.list_all_eyeglass_frames),
    # path('api/filter-by', views.filter_by),
    # path('api/filter-by-v2', views.filter_by_v2),
    # path('api/preview', views.preview),
    # path('api/details', views.details),
    # path('api/get-image-path-by-id', views.get_image_path_by_id),
    # path('api/test_recommend', views.test_recommend),
    
    ###################镜架采集与管理####################
    path('api/search-modeltype-sku', views.SearchModeltypeOrSKUView.as_view()), # post: 查询型号SKU
    path('api/search-sku', views.SearchSKUView.as_view()), # get: 查询镜架SKU
    path('api/delete-eyeglassframes', views.DeleteEyeglassFrameEntrysView.as_view()), # get: 删除镜架SKU
    path('api/upload-new-eyeglassframe', views.UploadNewEyeglassFrameView.as_view()), # post : 保存新镜架并生成新的计算任务
        path('api/generate-calculate-task', views.GenerateCalculateTaskView.as_view()), # post : 生成计算任务 

    path('api/save-new-eyeglassframe', views.SaveNewEyeglassFrameView.as_view()), # post: 添加新镜架
    path('api/save-edit-eyeglassframe', views.SaveEditEyeglassFrameView.as_view()), # post: 编辑镜架
    path('api/get-eyeglassframe-detail', views.GetEyeglassFrameDetailView.as_view()), # get: 获取镜架详情
    path('api/get-all-eyeglassframes_entrys', views.GetAllEyeglassFrameEntryView.as_view()), # get: 获取所有镜架基本信息
    path('api/get-all-brands', views.GetAllBrandsView.as_view()), # get: 获取所有品牌
    path('api/get-all-model-types', views.GetAllModelTypesView.as_view()), # get: 获取所有型号
    path('api/get-all-materials', views.GetAllMaterialsView.as_view()), # get: 获取所有材质
    path('api/get-all-colors', views.GetAllColorsView.as_view()), # get: 获取所有颜色
    path('api/get-all-shapes', views.GetAllShapesView.as_view()), # get: 获取所有形状
    path('api/get-all-is-transparent', views.GetAllIsTransparenrView.as_view()), # get: 获取所有透明度
    path('api/get-all-frame-types', views.GetAllFrameTypesView.as_view()), # get: 获取所有形状
    
    ###################以下为测试用####################
    # path('api/add-style', views.AddStyle), # post: 添加风格
    # path('api/add-style-list', views.AddStyleList), # post: 添加风格列表
    # path('api/add-material', views.AddMaterial), # post: 添加材质
    # path('api/add-material-list', views.AddMaterialList), # post: 添加材质列表
    # path('api/add-color', views.AddColor), # post: 添加颜色
    # path('api/add-color-list', views.AddColorList), # post: 添加颜色列表
    # path('api/add-shape', views.AddShape), # post: 添加形状
    # path('api/add-shape-list', views.AddShapeList), # post: 添加形状列表
]
