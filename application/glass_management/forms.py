from django import forms

from application.glass_management import models

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
        # exclude = ['entry','create_user', 'update_user', 'frontview', 'sideview', 'topview', 'frontview_bg', 'sideview_bg', 'topview_bg']
        exclude = ['entry','create_user', 'update_user', 'frontview', 'sideview', 'topview']

"""
镜架风格关联表
"""
class EyeglassFrameEntryStyleForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFrameEntryStyle
        exclude = ['entry','create_user', 'update_user']



