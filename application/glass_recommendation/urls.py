from django.urls import path  # 导入路径相关配置

from application.glass_recommendation import views
urlpatterns = [
    ###################推荐客户端采集####################
    path('api/register-recommandation-user', views.RegisterRecommendationUserView.as_view()), # post: 注册推荐客户端用户
    path('api/save-face-scanresult', views.SaveNewRecommendationUserFacialImageAndFacialScanResultView.as_view()), # post: 保存人脸扫描图像和结果
    path('api/save-baseinfo-optometry-lens', views.SaveNewRecommendationUserBaseInfoAndOptometryAndLensView.as_view()), # post: 保存基础信息、验光信息和镜片需求

]
