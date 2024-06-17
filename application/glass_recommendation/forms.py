from django import forms

from application.glass_recommendation import models

"""
推荐客户端用户基础信息表
"""
class RecommendationUserForm(forms.ModelForm):
    class Meta:
        model = models.RecommendationUser
        exclude = ['create_user', 'update_user']

"""
推荐客户端用户基础信息表
"""
class RecommendationUserBaseInfoForm(forms.ModelForm):
    class Meta:
        model = models.RecommendationUserBaseInfo
        exclude = ['user','create_user', 'update_user','age_range']

"""
推荐客户端用户人脸图像表
"""
class RecommendationUserFacialImageForm(forms.ModelForm):
    class Meta:
        model = models.RecommendationUserFacialImage
        exclude = ['user','create_user', 'update_user', 'frontview', 'leftview', 'rightview']
"""
推荐客户端用户验光信息表
"""
class RecommendationUserOptometryForm(forms.ModelForm):
    class Meta:
        model = models.RecommendationUserOptometry
        exclude = ['user','create_user', 'update_user']

"""
推荐客户端用户镜片需求表
"""
class RecommendationUserLensForm(forms.ModelForm):
    class Meta:
        model = models.RecommendationUserLens
        exclude = ['user','create_user', 'update_user']

"""
推荐客户端用户人脸扫描数据表
"""
class RecommendationUserFacialScanResultForm(forms.ModelForm):
    class Meta:
        model = models.RecommendationUserFacialScanResult
        exclude = ['user','create_user', 'update_user']


