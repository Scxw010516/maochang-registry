# MySQL 数据库表设计

## 镜架端数据库表设计

### 1. BaseModel

| 字段名      | 类型        | 字段含义 | 非 Null | 非重复 | 备注              |
| ----------- | ----------- | -------- | ------- | ------ | ----------------- |
| id          | int         | 主键 ID  | true    | true   | 自增、主键        |
| create_user | int         | 创建人   | true    | false  |                   |
| create_time | datetime(6) | 创建时间 | false   | false  |                   |
| update_user | int         | 更新人   | true    | false  |                   |
| update_time | datetime(6) | 更新时间 | false   | false  |                   |
| is_delete   | tinyint(1)  | 逻辑删除 | true    | false  | 0:未删除 1:已删除 |

### 2. 镜架基本信息表

#### 表名: maochang_eyeglassframeentry

| 字段名      | 类型          | 字段含义   | 非 Null | 非重复 | 备注               |
| ----------- | ------------- | ---------- | ------- | ------ | ------------------ |
| sku         | varchar(255)  | 镜架 SKU   | true    | true   |                    |
| brand       | varchar(255)  | 镜架品牌   | true    | false  |                    |
| model_type  | varchar(255)  | 镜架型号   | true    | false  |                    |
| price       | decimal(15,2) | 镜架价格   | true    | false  |                    |
| material    | int           | 镜架材质   | true    | false  | 外键关联镜架材质表 |
| color       | int           | 镜架颜色   | true    | false  | 外键关联镜架颜色表 |
| shape       | int           | 镜架形状   | true    | false  | 外键关联镜架形状表 |
| isnosepad   | tinyint(1)    | 是否有鼻托 | true    | false  | 0:无 1:有          |
| lens_radian | decimal(15,4) | 镜片弧度   | true    | false  |                    |
| stock       | int           | 镜架库存   | false   | false  |                    |
| warehouse   | int           | 仓库 ID    | false   | false  | 外键关联镜架仓库表 |

### 3. 镜架扫描结果记录表

#### 表名：maochang_eyeglassframedetectionresult

包括：1 个 entry_id(外键关联镜架基本信息表)、3 个视图图像相对路径、30 个镜架计算参数、1 个鼻托识别参数、1 个重量参数

| 字段名               | 类型          | 字段含义                       | 非 Null | 非重复 | 备注                   |
| -------------------- | ------------- | ------------------------------ | ------- | ------ | ---------------------- |
| entry                | int           | 镜架 ID                        | true    | true   | 外键关联镜架基本信息表 |
| frontview            | varchar(100)  | 镜架正视图                     | true    | false  | ImageField 类型        |
| sideview             | varchar(100)  | 镜架侧视图                     | true    | false  | ImageField 类型        |
| topview              | varchar(100)  | 镜架俯视图                     | true    | false  | ImageField 类型        |
| frontview_bg         | varchar(100)  | 镜架正视图背景                 | true    | false  | ImageField 类型        |
| sideview_bg          | varchar(100)  | 镜架侧视图背景                 | true    | false  | ImageField 类型        |
| topview_bg           | varchar(100)  | 镜架俯视图背景                 | true    | false  | ImageField 类型        |
| frame_height         | decimal(15,4) | 镜框高度                       | true    | false  | 正视图                 |
| frame_width          | decimal(15,4) | 镜框宽度                       | true    | false  | 正视图                 |
| pile_height_left     | decimal(15,4) | 左桩头高度                     | true    | false  | 正视图                 |
| pile_height_right    | decimal(15,4) | 右桩头高度                     | true    | false  | 正视图                 |
| frame_top_width      | decimal(15,4) | 镜框顶部宽度                   | true    | false  | 正视图                 |
| top_points           | varchar(255)  | 镜框左右最高点坐标（两组）     | true    | false  | 正视图、需要应用层解析 |
| frame_rects          | varchar(255)  | 镜框左右矩形坐标及宽高（两组） | true    | false  | 正视图、需要应用层解析 |
| lens_width_left      | decimal(15,4) | 左镜圈宽度                     | true    | false  | 正视图                 |
| lens_width_right     | decimal(15,4) | 右镜圈宽度                     | true    | false  | 正视图                 |
| lens_height_left     | decimal(15,4) | 左镜圈高度                     | true    | false  | 正视图                 |
| lens_height_right    | decimal(15,4) | 右镜圈高度                     | true    | false  | 正视图                 |
| lens_diagonal_left   | decimal(15,4) | 左镜圈对角线长度               | true    | false  | 正视图                 |
| lens_diagonal_right  | decimal(15,4) | 右镜圈对角线长度               | true    | false  | 正视图                 |
| lens_area_left       | decimal(15,4) | 左镜圈面积                     | true    | false  | 正视图                 |
| lens_area_right      | decimal(15,4) | 右镜圈面积                     | true    | false  | 正视图                 |
| bridge_width         | decimal(15,4) | 鼻梁宽度                       | true    | false  | 正视图                 |
| lens_center_points   | varchar(255)  | 镜圈中心点坐标（两组）         | true    | false  | 正视图、需要应用层解析 |
| lens_top_points      | varchar(255)  | 镜圈顶部点坐标（两组）         | true    | false  | 正视图、需要应用层解析 |
| vertical_angle       | decimal(15,4) | 垂俯角                         | true    | false  | 侧视图                 |
| forward_angle        | decimal(15,4) | 前倾角                         | true    | false  | 侧视图                 |
| temple_angle         | decimal(15,4) | 镜腿角度                       | true    | false  | 侧视图                 |
| drop_length          | decimal(15,4) | 垂长                           | true    | false  | 侧视图                 |
| face_angle           | decimal(15,4) | 面弯                           | true    | false  | 俯视图                 |
| sagittal_angle_left  | decimal(15,4) | 左垂内角                       | true    | false  | 俯视图                 |
| sagittal_angle_right | decimal(15,4) | 右垂内角                       | true    | false  | 俯视图                 |
| temple_length_left   | decimal(15,4) | 左镜腿长度                     | true    | false  | 俯视图                 |
| temple_length_right  | decimal(15,4) | 右镜腿长度                     | true    | false  | 俯视图                 |
| temporal_width       | decimal(15,4) | 颞距                           | true    | false  | 俯视图                 |
| spread_angle_left    | decimal(15,4) | 左镜腿外张角                   | true    | false  | 俯视图                 |
| spread_angle_right   | decimal(15,4) | 右镜腿外张角                   | true    | false  | 俯视图                 |
| pile_distance        | decimal(15,4) | 桩头距离                       | true    | false  | 正视图                 |
| weight               | decimal(15,4) | 重量                           | true    | false  |                        |

### 4. 镜架风格类型表

#### 表名：maochang_eyeglassframestyletype

| 字段名 | 类型         | 字段含义 | 非 Null | 非重复 | 备注 |
| ------ | ------------ | -------- | ------- | ------ | ---- |
| style  | varchar(255) | 风格类型 | true    | true   |      |

### 5. 镜架风格关联表

#### 表名：maochang_eyeglassframeentrystyle

| 字段名 | 类型 | 字段含义 | 非 Null | 非重复 | 备注                   |
| ------ | ---- | -------- | ------- | ------ | ---------------------- |
| entry  | int  | 镜架 ID  | true    | false  | 外键关联镜架基本信息表 |
| style  | int  | 风格 ID  | true    | false  | 外键关联镜架风格表     |

### 6. 镜架材质类型表

#### 表名：maochang_eyeglassframematerialtype

| 字段名   | 类型         | 字段含义 | 非 Null | 非重复 | 备注 |
| -------- | ------------ | -------- | ------- | ------ | ---- |
| material | varchar(255) | 材质类型 | true    | true   |      |

### 7. 镜架颜色类型表

#### 表名：maochang_eyeglassframecolortype

| 字段名 | 类型         | 字段含义 | 非 Null | 非重复 | 备注 |
| ------ | ------------ | -------- | ------- | ------ | ---- |
| color  | varchar(255) | 颜色类型 | true    | true   |      |

### 8. 镜架形状类型表

#### 表名：maochang_eyeglassframeshapetype

| 字段名 | 类型         | 字段含义 | 非 Null | 非重复 | 备注 |
| ------ | ------------ | -------- | ------- | ------ | ---- |
| shape  | varchar(255) | 形状类型 | true    | true   |      |

## 推荐系统数据库表设计

### 1. 推荐客户端用户表

#### 表名：maochang_recommendationuser

| 字段名   | 类型         | 字段含义   | 非 Null | 非重复 | 备注 |
| -------- | ------------ | ---------- | ------- | ------ | ---- |
| username | varchar(255) | 用户识别码 | true    | true   | 唯一 |

### 2. 推荐客户端用户基础信息表

#### 表名：maochang_recommendationuserbaseinfo

| 字段名    | 类型     | 字段含义 | 非 Null | 非重复 | 备注                                                                                         |
| --------- | -------- | -------- | ------- | ------ | -------------------------------------------------------------------------------------------- |
| user      | int      | 用户 ID  | true    | false  | 外键关联用户表                                                                               |
| gender    | smallint | 性别     | true    | false  | 0:保密 1:男 2:女 (暂不启用 0 选项)                                                           |
| age_range | smallint | 年龄段   | true    | false  | 0:保密 1:14 岁以下 2:15-25 岁 3:26-35 岁 4:36-45 岁 5:46-60 岁 6:61 岁以上 (暂不启用 0 选项) |
| age       | int      | 年龄     | true    | false  |                                                                                              |

### 3. 推荐客户端用户人脸图像表

#### 表名：maochang_recommendationuserfacialimage

| 字段名    | 类型         | 字段含义 | 非 Null | 非重复 | 备注            |
| --------- | ------------ | -------- | ------- | ------ | --------------- |
| user      | int          | 用户 ID  | true    | false  | 外键关联用户表  |
| frontview | varchar(100) | 正视图   | true    | false  | ImageField 类型 |
| leftview  | varchar(100) | 左视图   | true    | false  | ImageField 类型 |
| rightview | varchar(100) | 右视图   | true    | false  | ImageField 类型 |

### 4. 推荐客户端用户验光信息表

#### 表名：maochang_recommandationuseroptometry

| 字段名                 | 类型          | 字段含义      | 非 Null | 非重复 | 备注           |
| ---------------------- | ------------- | ------------- | ------- | ------ | -------------- |
| user                   | int           | 用户 ID       | true    | false  | 外键关联用户表 |
| pupil_distance         | decimal(15,4) | 瞳距          | true    | false  |                |
| myopia_hyperopia_left  | decimal(15,4) | 左眼近视/远视 | true    | false  |                |
| myopia_hyperopia_right | decimal(15,4) | 右眼近视/远视 | true    | false  |                |
| astigmatism_left       | decimal(15,4) | 左眼散光度    | true    | false  |                |
| astigmatism_right      | decimal(15,4) | 右眼散光度    | true    | false  |                |

### 5. 推荐客户端用户镜片需求表

#### 表名：maochang_recommandationuserlens

| 字段名           | 类型          | 字段含义   | 非 Null | 非重复 | 备注           |
| ---------------- | ------------- | ---------- | ------- | ------ | -------------- |
| user             | int           | 用户 ID    | true    | false  | 外键关联用户表 |
| refractive_index | decimal(15,4) | 镜片折射率 | true    | false  |                |
| diameter         | decimal(15,4) | 镜片直径   | true    | false  |                |
| density          | decimal(15,4) | 镜片密度   | true    | false  |                |

### 6. 推荐客户端用户人脸扫描数据表

#### 表名：maochang_recommandationuserfacialscanresult

| 字段名                  | 类型          | 字段含义     | 非 Null | 非重复 | 备注                                            |
| ----------------------- | ------------- | ------------ | ------- | ------ | ----------------------------------------------- |
| user                    | int           | 用户 ID      | true    | false  | 外键关联用户表                                  |
| outer_canthic_diameter  | decimal(15,4) | 外眼角间距   | true    | false  |                                                 |
| inner_canthic_diameter  | decimal(15,4) | 内眼角间距   | true    | false  |                                                 |
| eye_width_left          | decimal(15,4) | 左眼宽       | true    | false  |                                                 |
| eye_width_right         | decimal(15,4) | 右眼宽       | true    | false  |                                                 |
| eye_height_left         | decimal(15,4) | 左眼高       | true    | false  |                                                 |
| eye_height_right        | decimal(15,4) | 右眼高       | true    | false  |                                                 |
| ala_nasi_width          | decimal(15,4) | 鼻翼宽       | true    | false  |                                                 |
| nasion_width            | decimal(15,4) | 鼻根宽       | true    | false  |                                                 |
| nose_height             | decimal(15,4) | 鼻高         | true    | false  |                                                 |
| nose_pivot_angle        | decimal(15,4) | 鼻基准角     | true    | false  |                                                 |
| head_width              | decimal(15,4) | 头宽         | true    | false  |                                                 |
| side_face_length_left   | decimal(15,4) | 左侧面长     | true    | false  |                                                 |
| side_face_length_right  | decimal(15,4) | 右侧面长     | true    | false  |                                                 |
| outer_canthic_ear_left  | decimal(15,4) | 左外眼角耳距 | true    | false  |                                                 |
| outer_canthic_ear_right | decimal(15,4) | 右外眼角耳距 | true    | false  |                                                 |
| eyebrow_center_width    | decimal(15,4) | 眉上顶点距   | true    | false  |                                                 |
| face_height             | decimal(15,4) | 脸高         | true    | false  |                                                 |
| lip_width               | decimal(15,4) | 嘴唇宽       | true    | false  |                                                 |
| lip_height              | decimal(15,4) | 嘴唇高       | true    | false  |                                                 |
| face_type               | smallint      | 脸型         | true    | false  | 0:菱形脸 1:圆脸 2:方脸 3:长脸 4:心形脸 5:鹅蛋脸 |
| skin_color_type         | smallint      | 肤色         | true    | false  | 0:偏黑 1:适中 2:偏白                            |

## 仓库管理数据库表设计

### 1. 镜架仓库表

#### 表名：maochang_warehouse

| 字段名    | 类型         | 字段含义 | 非 Null | 非重复 | 备注 |
| --------- | ------------ | -------- | ------- | ------ | ---- |
| warehouse | varchar(255) | 仓库名称 | true    | true   |      |
| address   | varchar(255) | 仓库地址 | true    | false  |      |
