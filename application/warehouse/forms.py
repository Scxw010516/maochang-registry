from django import forms

from application.warehouse import models

"""
镜架仓库表
"""
class Warehouse(forms.ModelForm):
    class Meta:
        model = models.Warehouse
        exclude = ['create_user', 'update_user']


