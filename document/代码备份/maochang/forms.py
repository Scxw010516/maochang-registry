from django import forms

from application.maochang import models

"""
镜架基本信息表
"""
class EyeglassFrameEntryForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFrameEntry
        exclude = ['create_user', 'update_user']

"""
镜架扫描结果表
"""
class EyeglassFrameDetectionResultForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFrameDetectionResult
        exclude = ['entry','create_user', 'update_user', 'frontview', 'sideview', 'topview', 'frontview_bg', 'sideview_bg', 'topview_bg']

"""
镜架风格关联表
"""
class EyeglassFrameEntryStyleForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFrameEntryStyle
        exclude = ['entry','create_user', 'update_user']

##########################################################################
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


