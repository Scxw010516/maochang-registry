# +----------------------------------------------------------------------
# | DjangoAdmin敏捷开发框架 [ 赋能开发者，助力企业发展 ]
# +----------------------------------------------------------------------
# | 版权所有 2021~2024 北京DjangoAdmin研发中心
# +----------------------------------------------------------------------
# | Licensed LGPL-3.0 DjangoAdmin并不是自由软件，未经许可禁止去掉相关版权
# +----------------------------------------------------------------------
# | 官方网站: https://www.djangoadmin.cn
# +----------------------------------------------------------------------
# | 作者: @一米阳光 团队荣誉出品
# +----------------------------------------------------------------------
# | 版权和免责声明:
# | 本团队对该软件框架产品拥有知识产权（包括但不限于商标权、专利权、著作权、商业秘密等）
# | 均受到相关法律法规的保护，任何个人、组织和单位不得在未经本团队书面授权的情况下对所授权
# | 软件框架产品本身申请相关的知识产权，禁止用于任何违法、侵害他人合法权益等恶意的行为，禁
# | 止用于任何违反我国法律法规的一切项目研发，任何个人、组织和单位用于项目研发而产生的任何
# | 意外、疏忽、合约毁坏、诽谤、版权或知识产权侵犯及其造成的损失 (包括但不限于直接、间接、
# | 附带或衍生的损失等)，本团队不承担任何法律责任，本软件框架禁止任何单位和个人、组织用于
# | 任何违法、侵害他人合法利益等恶意的行为，如有发现违规、违法的犯罪行为，本团队将无条件配
# | 合公安机关调查取证同时保留一切以法律手段起诉的权利，本软件框架只能用于公司和个人内部的
# | 法律所允许的合法合规的软件产品研发，详细声明内容请阅读《框架免责声明》附件；
# +----------------------------------------------------------------------

from django import forms

from application.item import models


# 站点表单验证
class ItemForm(forms.ModelForm):
    # 站点名称
    name = forms.CharField(
        max_length=150,
        error_messages={
            'required': '站点名称不能为空',
            'max_length': '站点名称长度不得超过150个字符',
        }
    )
    # 站点类型：1普通站点 2其他站点
    type = forms.IntegerField(
        min_value=1,
        max_value=2,
        error_messages={
            'required': '站点类型不能为空',
            'min_value': '站点类型值在1~2之间',
            'max_value': '站点类型值在1~2之间',
        }
    )
    # 站点URL
    url = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '站点URL不能为空',
            'max_length': '站点URL长度不得超过255个字符',
        }
    )
    # 站点图片
    image = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '站点图片不能为空',
            'max_length': '站点图片长度不得超过255个字符',
        }
    )
    # 站点状态：1-正常 2-停用
    status = forms.IntegerField(
        min_value=1,
        max_value=2,
        error_messages={
            'required': '站点状态不能为空',
            'min_value': '站点状态值在1~2之间',
            'max_value': '站点状态值在1~2之间',
        }
    )
    # 站点备注
    note = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'max_length': '站点备注长度不得超过255个字符',
        }
    )
    # 站点排序
    sort = forms.IntegerField(
        min_value=0,
        max_value=99999,
        error_messages={
            'required': '站点排序不能为空',
            'min_value': '站点排序值在0~99999之间',
            'max_value': '站点排序值在0~99999之间',
        }
    )

    class Meta:
        # 绑定模型
        model = models.Item
        # 指定部分字段验证
        fields = ['name', 'type', 'status', 'sort']
