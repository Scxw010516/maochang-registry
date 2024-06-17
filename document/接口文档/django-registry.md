# 镜架接口文档--Vue 前端、Django 后端、WebSocket 工控机端

## Vue-Django

### 1.查询镜架 SKU

请求 URL

```
GET  api/search-sku
```

请求参数
| 参数名 | 类型 | 描述 | 必填 |
| ------ | ---- | -------- | ---- |
| sku | str | 镜架 SKU | 是 |

请求示例

```
GET  api/search-sku?sku=123456
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
# 镜架SKU存在
{
    "status": 200,
    "data": {
        'code': 0,     # 状态码, 0:成功, -1:失败
        'data': {
            'id': int,              # 镜架ID
            'sku': str,             # 镜架SKU
            'brand': str,           # 镜架品牌
            'model_type': str,      # 镜架型号
            'price': float,         # 镜架价格
            'material': int,        # 镜架材质
            'color': int,           # 镜架颜色
            'shape': int,           # 镜架形状
            'isnosepad': int,       # 是否有鼻托, 0:无, 1:有
            'lens_radian': float,   # 撑片弧度
            'stock': int,           # 镜架库存
            'warehouse':int         # 仓库id
            'style': list[int],     # 镜架风格类型列表
            'create_time': str      # 创建时间
            'update_time': str      # 更新时间
        },
        'msg': ''
    }
}
# 镜架SKU不存在
{
    "status": 200,
    "data": {
        'code': 0,
        'msg': '镜架SKU不存在'
    }
}
# 查询参数为空
{
    "status": 200,
    "data": {
        'code': -1,
        'msg': '查询参数为空'
    }
}
```

### 2.删除镜架

请求 URL

```
POST  api/delete-eyeglassframes
```

请求参数
| 参数名 | 类型 | 描述 | 必填 | 备注 |
| ------ | ----- | ------- | ---- | ------------------------- |
| ids | int[] | 镜架 id | 是 | 镜架 id 列表，Json 序列化 |

请求示例

```
POST  api/delete-eyeglassframes
```

```ts
let formData = new FormData();
formData.append("ids", JSON.stringify(ids); // ids 为镜架 id 列表, 如 [1, 2, 3]
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
# 镜架删除成功
{
    "status": 200,
    "data": {
        'code': 0,     # 状态码, 0:成功, -1:失败
        'msg': '镜架删除成功'
    }
}
# 待删除镜架不存在
{
    "status": 200,
    "data": {
        'code': -1,
        'msg': '待删除镜架不存在'
    }
}
```

### 3.添加新镜架

请求 URL

```
POST  api/save-new-eyeglassframe
```

请求参数
| 参数名 | 类型 | 描述 | 必填 |
| -------------------- | ------------- | ------------------------------ | ---- |
| sku | varchar(255) | 镜架 SKU | 是 |
| brand | varchar(255) | 镜架品牌 | 是 |
| model_type | varchar(255) | 镜架型号 | 是 |
| price | decimal(15,2) | 镜架价格 | 是 |
| material | int | 镜架材质(材质表 id) | 是 |
| color | int | 镜架颜色 | 是 |
| shape | int | 镜架形状 | 是 |
| isnosepad | tinyint(1) | 是否有鼻托, 0:无, 1:有 | 是 |
| lens_radian | decimal(15,4) | 撑片弧度 | 是 |
| stock | int | 镜架库存 | 否 |
| warehouse | int | 仓库 id | 是 |
| style | list | 镜架风格类型 id 列表 | 是 |
| frontview | file | 镜架正视图文件 | 是 |
| sideview | file | 镜架侧视图文件 | 是 |
| topview | file | 镜架俯视图文件 | 是 |
| frontview_bg | file | 镜架正视图背景文件 | 是 |
| sideview_bg | file | 镜架侧视图背景文件 | 是 |
| topview_bg | file | 镜架俯视图背景文件 | 是 |
| frame_height | decimal(15,4) | 镜框高度 | 是 |
| frame_width | decimal(15,4) | 镜框宽度 | 是 |
| pile_height_left | decimal(15,4) | 左桩头高度 | 是 |
| pile_height_right | decimal(15,4) | 右桩头高度 | 是 |
| frame_top_width | decimal(15,4) | 镜框顶部宽度 | 是 |
| top_points | varchar(255) | 镜框左右最高点坐标（两组） | 是 |
| frame_rects | varchar(255) | 镜框左右矩形坐标及宽高（两组） | 是 |
| lens_width_left | decimal(15,4) | 左镜圈宽度 | 是 |
| lens_width_right | decimal(15,4) | 右镜圈宽度 | 是 |
| lens_height_left | decimal(15,4) | 左镜圈高度 | 是 |
| lens_height_right | decimal(15,4) | 右镜圈高度 | 是 |
| lens_diagonal_left | decimal(15,4) | 左镜圈对角线长度 | 是 |
| lens_diagonal_right | decimal(15,4) | 右镜圈对角线长度 | 是 |
| lens_area_left | decimal(15,4) | 左镜圈面积 | 是 |
| lens_area_right | decimal(15,4) | 右镜圈面积 | 是 |
| bridge_width | decimal(15,4) | 鼻梁宽度 | 是 |
| lens_center_points | varchar(255) | 镜圈中心点坐标（两组） | 是 |
| lens_top_points | varchar(255) | 镜圈顶部点坐标（两组） | 是 |
| vertical_angle | decimal(15,4) | 垂俯角 | 是 |
| forward_angle | decimal(15,4) | 前倾角 | 是 |
| temple_angle | decimal(15,4) | 镜腿角度 | 是 |
| drop_length | decimal(15,4) | 垂长 | 是 |
| face_angle | decimal(15,4) | 面弯 | 是 |
| sagittal_angle_left | decimal(15,4) | 左垂内角 | 是 |
| sagittal_angle_right | decimal(15,4) | 右垂内角 | 是 |
| temple_length_left | decimal(15,4) | 左镜腿长度 | 是 |
| temple_length_right | decimal(15,4) | 右镜腿长度 | 是 |
| temporal_width | decimal(15,4) | 颞距 | 是 |
| spread_angle_left | decimal(15,4) | 左镜腿外张角 | 是 |
| spread_angle_right | decimal(15,4) | 右镜腿外张角 | 是 |
| pile_distance | decimal(15,4) | 两个桩头之间的距离 | 是 |
| weight | decimal(15,4) | 重量 | 是 |

请求示例（前端 FormData 构建代码示例）

```
POST  api/save-new-eyeglassframe
Content-Type: multipart/form-data
```

```ts
// 注意ts在构建FormData时，append的第二个参数只能是字符串或者Blob对象，需要对数字类型和数组类型进行转换。以下仅供参考
let formData = new FormData();
formData.append("sku", "123456");
formData.append("brand", "品牌");
formData.append("model_type", "型号");
formData.append("price", 100.11); // 价格，保留两位小数
formData.append("material", 1); // 材质表id
formData.append("isnosepad", 1); // 是否有鼻托, 0:无, 1:有
formData.append("stock", 100);
formData.append("frontview", file); // file为文件对象
formData.append("sideview", file); // file为文件对象
formData.append("topview", file); // file为文件对象
formData.append("frame_height", 10);
formData.append("frame_width", 10);
formData.append("pile_height_left", 10);
formData.append("pile_height_right", 10);
formData.append("frame_top_width", 10);
formData.append("top_points", "1,2;3,4");
formData.append("frame_rects", "1,2,3,4;5,6,7,8");
formData.append("lens_width_left", 10);
formData.append("lens_width_right", 10);
formData.append("lens_height_left", 10);
formData.append("lens_height_right", 10);
formData.append("lens_diagonal_left", 10);
formData.append("lens_diagonal_right", 10);
formData.append("lens_area_left", 10);
formData.append("lens_area_right", 10);
formData.append("bridge_width", 10);
formData.append("lens_center_points", "1,2;3,4");
formData.append("lens_top_points", "1,2;3,4");
formData.append("vertical_angle", 10);
formData.append("forward_angle", 10);
formData.append("temple_angle", 10);
formData.append("drop_length", 10);
formData.append("face_angle", 10);
formData.append("sagittal_angle_left", 10);
formData.append("sagittal_angle_right", 10);
formData.append("temple_length_left", 10);
formData.append("temple_length_right", 10);
formData.append("temporal_width", 10);
formData.append("spread_angle_left", 10);
formData.append("spread_angle_right", 10);
formData.append("weight", 10);
formData.append("style_ids", [1, 2, 3]); // 镜架风格类型id列表
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
{
    "status": 200,
    "data": {
        'code': 0,     # 状态码, 0:成功, -1:失败
        'msg': '镜架添加成功'
    }
}
```

### 4.编辑镜架

请求 URL

```
POST  api/edit-eyeglassframe
```

请求参数
相比 3.添加新镜架，多了一个 id 参数，少了 frontview、sideview、topview 三个参数
| 参数名 | 类型 | 描述 | 必填 |
| -------------------- | ------------- | ------------------------------ | ---- |
| id | int | 镜架 ID | 是 |
| sku | varchar(255) | 镜架 SKU | 是 |
| brand | varchar(255) | 镜架品牌 | 是 |
| model_type | varchar(255) | 镜架型号 | 是 |
| price | decimal(15,2) | 镜架价格 | 是 |
| material | int | 镜架材质(材质表 id) | 是 |
| color | int | 镜架颜色 | 是 |
| shape | int | 镜架形状 | 是 |
| isnosepad | tinyint(1) | 是否有鼻托, 0:无, 1:有 | 是 |
| lens_radian | decimal(15,4) | 撑片弧度 | 是 |
| stock | int | 镜架库存 | 否 |
| warehouse | int | 仓库 id | 是 |
| style | list | 镜架风格类型 id 列表 | 是 |
| frame_height | decimal(15,4) | 镜框高度 | 是 |
| frame_width | decimal(15,4) | 镜框宽度 | 是 |
| pile_height_left | decimal(15,4) | 左桩头高度 | 是 |
| pile_height_right | decimal(15,4) | 右桩头高度 | 是 |
| frame_top_width | decimal(15,4) | 镜框顶部宽度 | 是 |
| top_points | varchar(255) | 镜框左右最高点坐标（两组） | 是 |
| frame_rects | varchar(255) | 镜框左右矩形坐标及宽高（两组） | 是 |
| lens_width_left | decimal(15,4) | 左镜圈宽度 | 是 |
| lens_width_right | decimal(15,4) | 右镜圈宽度 | 是 |
| lens_height_left | decimal(15,4) | 左镜圈高度 | 是 |
| lens_height_right | decimal(15,4) | 右镜圈高度 | 是 |
| lens_diagonal_left | decimal(15,4) | 左镜圈对角线长度 | 是 |
| lens_diagonal_right | decimal(15,4) | 右镜圈对角线长度 | 是 |
| lens_area_left | decimal(15,4) | 左镜圈面积 | 是 |
| lens_area_right | decimal(15,4) | 右镜圈面积 | 是 |
| bridge_width | decimal(15,4) | 鼻梁宽度 | 是 |
| lens_center_points | varchar(255) | 镜圈中心点坐标（两组） | 是 |
| lens_top_points | varchar(255) | 镜圈顶部点坐标（两组） | 是 |
| vertical_angle | decimal(15,4) | 垂俯角 | 是 |
| forward_angle | decimal(15,4) | 前倾角 | 是 |
| temple_angle | decimal(15,4) | 镜腿角度 | 是 |
| drop_length | decimal(15,4) | 垂长 | 是 |
| face_angle | decimal(15,4) | 面弯 | 是 |
| sagittal_angle_left | decimal(15,4) | 左垂内角 | 是 |
| sagittal_angle_right | decimal(15,4) | 右垂内角 | 是 |
| temple_length_left | decimal(15,4) | 左镜腿长度 | 是 |
| temple_length_right | decimal(15,4) | 右镜腿长度 | 是 |
| temporal_width | decimal(15,4) | 颞距 | 是 |
| spread_angle_left | decimal(15,4) | 左镜腿外张角 | 是 |
| spread_angle_right | decimal(15,4) | 右镜腿外张角 | 是 |
| pile_distance | decimal(15,4) | 两个桩头之间的距离 | 是 |
| weight | decimal(15,4) | 重量 | 是 |

请求示例（前端 FormData 构建代码示例）

```
同3.添加新镜架
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
同3.添加新镜架
```

### 5.查询镜架详情

请求 URL

```
GET  api/get-eyeglassframe-detail
```

请求参数
| 参数名 | 类型 | 描述 | 必填 |
| ------ | ---- | -------- | ---- |
| sku | str | 镜架 SKU | 是 |

请求示例

```
GET  api/get-eyeglassframe-detail?sku=123456
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
# 镜架SKU存在
{
    "status": 200,
    "data": {
        'code': 0,     # 状态码, 0:成功, -1:失败
        'data': {
            'sku': str,       # 镜架SKU
            'brand': str,     # 镜架品牌
            'model_type': str,# 镜架型号
            'price': float,     # 镜架价格
            'material': int,  # 镜架材质
            'color': int,     # 镜架颜色
            'shape': int,     # 镜架形状
            'isnosepad': int, # 是否有鼻托, 0:无, 1:有
            'lens_radian': float, # 撑片弧度
            'stock': int,     # 镜架库存
            'warehouse':int   # 仓库id
            'style': list[int], # 镜架风格类型列表
            'frontview': str,  # 镜架正视图相对地址
            'sideview': str,   # 镜架侧视图相对地址
            'topview': str,    # 镜架俯视图相对地址
            'frame_height': decimal(15,4), # 镜框高度
            'frame_width': decimal(15,4),  # 镜框宽度
            'pile_height_left': decimal(15,4),  # 左桩头高度
            'pile_height_right': decimal(15,4), # 右桩头高度
            'frame_top_width': decimal(15,4),   # 镜框顶部宽度
            'top_points': str,  # 镜框左右最高点坐标（两组）
            'frame_rects': str, # 镜框左右矩形坐标及宽高（两组）
            'lens_width_left': decimal(15,4),  # 左镜圈宽度
            'lens_width_right': decimal(15,4), # 右镜圈宽度
            'lens_height_left': decimal(15,4), # 左镜圈高度
            'lens_height_right': decimal(15,4),# 右镜圈高度
            'lens_diagonal_left': decimal(15,4), # 左镜圈对角线长度
            'lens_diagonal_right': decimal(15,4),# 右镜圈对角线长度
            'lens_area_left': decimal(15,4), # 左镜圈面积
            'lens_area_right': decimal(15,4),# 右镜圈面积
            'bridge_width': decimal(15,4),  # 鼻梁宽度
            'lens_center_points': str,  # 镜圈中心点坐标（两组）
            'lens_top_points': str,     # 镜圈顶部点坐标（两组）
            'vertical_angle': decimal(15,4), # 垂俯角
            'forward_angle': decimal(15,4),  # 前倾角
            'temple_angle': decimal(15,4),   # 镜腿角度
            'drop_length': decimal(15,4),    # 垂长
            'face_angle': decimal(15,4),     # 面弯
            'sagittal_angle_left': decimal(15,4),  # 左垂内角
            'sagittal_angle_right': decimal(15,4), # 右垂内角
            'temple_length_left': decimal(15,4),  # 左镜腿长度
            'temple_length_right': decimal(15,4), # 右镜腿长度
            'temporal_width': decimal(15,4),      # 颞距
            'spread_angle_left': decimal(15,4),   # 左镜腿外张角
            'spread_angle_right': decimal(15,4),  # 右镜腿外张角
            'pile_distance': decimal(15,4),       # 两个桩头之间的距离
            'weight': decimal(15,4),              # 重量
        },
        'msg': ''
    }
}
# 镜架SKU不存在
{
    "status": 200,
    "data": {
        'code': -1,
        'msg': '镜架SKU不存在'
    }
}
```

### 6.查询镜架列表

使用 vue-request 库发送请求，详细参数见 manage.vue 文件

请求 URL

```
GET  api/get-all-eyeglassframes_entrys
```

### 7.查询所有镜架品牌

请求 URL

```
GET  api/get-all-brands
```

请求参数

```
无
```

请求示例

```
GET  api/get-all-brands
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
{
    "status": 200,
    "data": {
        'code': 0,     # 状态码, 0:成功, -1:失败
        'data': [brand1, brand2, ...],  # 镜架品牌列表
        'msg': ''
    }
}
```

### 8.查询所有镜架型号

请求 URL

```
GET  api/get-all-model-types
```

请求参数

```
无
```

请求示例

```
GET  api/get-all-model-types
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
{
    "status": 200,
    "data": {
        'code': 0,     # 状态码, 0:成功, -1:失败
        'data': [model_type1, model_type2, ...],  # 镜架型号列表
        'msg': ''
    }
}
```

### 9.查询所有镜架材质

请求 URL

```
GET  api/get-all-materials
```

请求参数

```
无
```

请求示例

```
GET  api/get-all-materials
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
{
    "status": 200,
    "data": {
        'code': 0,     # 状态码, 0:成功, -1:失败
        'data': [{
            'id': int,         # 材质类型ID
            'material': str,      # 材质类型
        }, ...],  # 镜架材质类型列表
        'msg': ''
    }
}
```

### 10.查询所有镜架颜色

请求 URL

```
GET  api/get-all-colors
```

请求参数

```
无
```

请求示例

```
GET  api/get-all-colors
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
{
    "status": 200,
    "data": {
        'code': 0,     # 状态码, 0:成功, -1:失败
        'data': [{
            'id': int,         # 颜色类型ID
            'color': str,      # 颜色类型
        }, ...],  # 镜架颜色类型列表
        'msg': ''
    }
}
```

### 11.查询所有镜架形状

请求 URL

```
GET  api/get-all-shapes
```

请求参数

```
无
```

请求示例

```
GET  api/get-all-shapes
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
{
    "status": 200,
    "data": {
        'code': 0,     # 状态码, 0:成功, -1:失败
        'data': [{
            'id': int,         # 形状类型ID
            'shape': str,      # 形状类型
        }, ...],  # 镜架形状类型列表
        'msg': ''
    }
}
```

### 12.查询所有镜架风格类型

请求 URL

```
GET  api/get-all-styles
```

请求参数

```
无
```

请求示例

```
GET  api/get-all-styles
```

响应参数
| 参数名 | 类型 | 描述 |
| ------ | ------ | ---------------- |
| status | int | 状态码 |
| data | object | 返回数据（重要） |

响应示例

```
{
    "status": 200,
    "data": {
        'code': 0,     # 状态码, 0:成功, -1:失败
        'data': [{
            'id': int,         # 风格类型ID
            'style': str,      # 风格类型
        }, ...],  # 镜架风格类型列表
        'msg': ''
    }
}
```
