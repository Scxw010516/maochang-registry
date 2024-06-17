# 推荐接口文档--Vue 前端、Django 后端、WebSocket 工控机端

## Vue-Django

### 1.注册推荐 user

请求 URL

```
POST api/register-recommandation-user
```

请求参数
| 参数名 | 类型 | 描述 | 必填 |
| ---- | ---- | ---- | ---- |
| username | str | 用户识别号 | 是 |

请求示例

```
POST api/search-recommandation-user ,FormData
```

响应参数
| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
# 注册成功
{
    "status": 200,
    "data": {
        'code': 0,
        'msg': '用户注册成功'
    }
}
# 注册失败
{
    "status": 200,
    "data": {
        'code': -1,
        'msg': '用户已存在'
    }
}
```

### 2.保存人脸图片和人脸扫描数据

请求 URL

```
POST api/save-face-scanresult
```

请求参数
| 参数名 | 类型 | 描述 | 必填 |
| ---- | ---- | ---- | ---- |
| username | str | 用户识别码 | 是 |
| frontview | file | 正面照片 | 是 |
| leftview | file | 左侧照片 | 是 |
| rightview | file | 右侧照片 | 是 |
| outer_canthic_diameter | decimal(15,4) | 外眼角距 | 是 |
| inner_canthic_diameter | decimal(15,4) | 内眼角距 | 是 |
| eye_width_left | decimal(15,4) | 左眼宽度 | 是 |
| eye_width_right | decimal(15,4) | 右眼宽度 | 是 |
| eye_height_left | decimal(15,4) | 左眼高度 | 是 |
| eye_height_right | decimal(15,4) | 右眼高度 | 是 |
| ala_nasi_width | decimal(15,4) | 鼻翼宽度 | 是 |
| nasion_width | decimal(15,4) | 鼻梁宽度 | 是 |
| nose_height | decimal(15,4) | 鼻子高度 | 是 |
| nose_pivot_angle | decimal(15,4) | 鼻子角度 | 是 |
| head_width | decimal(15,4) | 头宽 | 是 |
| side_face_length_left | decimal(15,4) | 左脸宽 | 是 |
| side_face_length_right | decimal(15,4) | 右脸宽 | 是 |
| outer_canthic_ear_left | decimal(15,4) | 左眼角耳朵距 | 是 |
| outer_canthic_ear_right | decimal(15,4) | 右眼角耳朵距 | 是 |
| eyebrow_center_width | decimal(15,4) | 眉心宽度 | 是 |
| face_height | decimal(15,4) | 脸高 | 是 |
| lip_width | decimal(15,4) | 唇宽 | 是 |
| lip_height | decimal(15,4) | 唇高 | 是 |
| face_type | int | 脸型 | 是 |
| skin_color_type | int | 肤色 | 是 |

请求示例

```
POST api/save-new-recommandation-user ,FormData
```

响应参数
| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
{
    "status": 200,
    "data": {
        'code': 0,
        'msg': '保存成功'
    }
}
```

### 3.保存基础信息、验光信息和镜片需求

请求 URL

```
POST api/save-baseinfo-optometry-lens
```

请求参数
| 参数名 | 类型 | 描述 | 必填 |
| ---- | ---- | ---- | ---- |
| username | str | 用户识别码 | 是 |
| gender | int | 性别 | 是 |
| age_range | int | 年龄段 | 是 |
| pupil_distance | decimal(15,4) | 瞳距 | 是 |
| myopia_hyperopia_left | decimal(15,4) | 左眼球镜 | 是 |
| myopia_hyperopia_right | decimal(15,4) | 右眼球镜 | 是 |
| astigmatism_left | decimal(15,4) | 左眼散光 | 是 |
| astigmatism_right | decimal(15,4) | 右眼散光 | 是 |
| refractive_index | decimal(15,4) | 折射率 | 是 |
| diameter | decimal(15,4) | 直径 | 是 |
| density | decimal(15,4) | 密度 | 是 |

请求示例

```
POST api/save-baseinfo-optometry-lens ,FormData
```

响应参数
| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
{
    "status": 200,
    "data": {
        'code': 0,
        'msg': '保存成功'
    }
}
```
