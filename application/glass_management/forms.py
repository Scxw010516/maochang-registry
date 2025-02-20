from django import forms

from application.glass_management import models

"""
镜架基本信息表
"""
class EyeglassFrameEntryForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFrameEntry
        exclude = ['create_user', 'update_user','pixel_measurement_state','millimeter_measurement_state','calculation_state','coordinate_state','image_mask_state','image_seg_state','image_beautify_state']

"""
镜架毫米测量数据
"""
class EyeglassFrameMillimeterMeasurementForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFrameMillimeterMeasurement
        exclude = ['entry', 'create_user', 'update_user']

"""
镜架像素测量数据
"""
class EyeglassFramePixelMeasurementForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFramePixelMeasurement
        exclude = ['entry', 'create_user', 'update_user']

"""
镜架计算数据
"""
class EyeglassFrameCalulationForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFrameCalulation
        exclude = ['entry', 'create_user', 'update_user']

"""
镜架坐标数据
"""
class EyeglassFrameCoordinateForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFrameCoordinate
        exclude = ['entry', 'create_user', 'update_user']

"""
镜架图片数据
"""
class EyeglassFrameImageForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFrameImage
        exclude = ['entry', 'create_user', 'update_user']

"""
镜架预加载数据
"""
class EyeglassFramePreloadDataForm(forms.ModelForm):
    class Meta:
        model = models.EyeglassFramePreloadData
        exclude = ['entry', 'create_user', 'update_user']



