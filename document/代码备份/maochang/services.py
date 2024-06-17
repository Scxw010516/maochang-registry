import json
import decimal
from utils import R, regular
from utils import utils
from django.db import transaction
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, HttpRequest

from application.maochang import models
from application.maochang import forms

# 镜架采集端

def SearchSKU(request:HttpRequest, sku:str):
    """
    查询镜架SKU

    参数：
        request: HttpRequest 请求对象
        sku: str 镜架SKU

    返回：
        HttpResponse: JSON格式的响应对象，{code,data,msg}
    """

    # 参数为空判断
    if not sku:
        return R.failed(msg="查询参数为空")
    
    # 查询镜架SKU是否存在，其中sku是唯一的
    entry = models.EyeglassFrameEntry.objects.filter(sku=sku).first()

    # 判断查询结果是否为空
    if not entry:
        return R.ok(msg="镜架SKU不存在")
    
    # 构建查询结果
    search_result = {
        'id': entry.id,  # 镜架ID,主键
        'sku': entry.sku,  # 镜架SKU，唯一
        'brand': entry.brand,
        'model_type': entry.model_type,
        'price': entry.price,
        'material': entry.material.id,
        'color':entry.color.id,
        'shape':entry.shape.id,
        'isnosepad': entry.isnosepad,
        'stock': entry.stock,
        'style': [style.style.id for style in models.EyeglassFrameEntryStyle.objects.filter(entry=entry).all()],  # 镜架风格关联表，多对多关系
        'create_time': entry.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': entry.update_time.strftime('%Y-%m-%d %H:%M:%S')
    }

    # 返回查询结果
    return R.ok(data=search_result)

def DeleteEyeglassFrameEntrys(request:HttpRequest):
    """
    删除镜架SKU，其外键关联表会自动删除该SKU镜架对应的数据

    参数：
        request: HttpRequest 请求对象
        sku: str 镜架SKU

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数
    ids = request.POST.get("ids")
    ids = json.loads(ids)

    # 参数为空判断
    if len(ids) == 0:
        return R.failed(msg="删除参数为空")
    
    # 查询镜架SKU是否存在，其中sku是唯一的
    search_result = models.EyeglassFrameEntry.objects.filter(id__in=ids)

    # 判断查询结果是否为空
    if not search_result:
        return R.failed(msg="待删除镜架不存在")
    
    # 删除镜架SKU
    search_result.delete()

    # 返回成功信息
    return R.ok(msg="镜架删除成功")

def SaveNewEyeglassFrame(request:HttpRequest):
    """
    保存新镜架，创建新的数据库实例：镜架基本信息表、镜架扫描结果表、镜架风格关联表

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数
    if not request.POST:
        return R.failed(msg="参数错误")
    
    try:
        # 数据库事务处理
        with transaction.atomic():
            """
            镜架基本信息表处理
            """
            # 验证镜架基本信息表表单
            form_EyeglassFrameEntry = forms.EyeglassFrameEntryForm(request.POST)
            if form_EyeglassFrameEntry.is_valid():
                # 保存镜架基本信息表实例
                EyeglassFrameEntry_instance = form_EyeglassFrameEntry.save()

                """
                镜架扫描结果表处理
                """
                # 创建镜架扫描结果表实例
                form_EyeglassFrameDetectionResult = forms.EyeglassFrameDetectionResultForm(request.POST)
                # 验证镜架扫描结果表表单
                if form_EyeglassFrameDetectionResult.is_valid():
                    # 构建并保存镜架扫描结果表的数据库实例
                    EyeglassFrameDetectionResult_instance = form_EyeglassFrameDetectionResult.save(commit=False)
                    # 关联镜架基本信息表外键
                    EyeglassFrameDetectionResult_instance.entry = EyeglassFrameEntry_instance
                    # 获取三视图图片文件
                    frontview = request.FILES.get("frontview")
                    sideview = request.FILES.get("sideview")
                    topview = request.FILES.get("topview")
                    # 获取三视图图片背景文件
                    frontview_bg = request.FILES.get("frontview_bg")
                    sideview_bg = request.FILES.get("sideview_bg")
                    topview_bg = request.FILES.get("topview_bg")
                    # 获取三视图图片错误处理
                    if not frontview or not sideview or not topview or not frontview_bg or not sideview_bg or not topview_bg:
                        # 抛出异常
                        raise ValueError("三视图图片不能为空")
                    # 保存三视图图片文件
                    EyeglassFrameDetectionResult_instance.frontview = frontview
                    EyeglassFrameDetectionResult_instance.sideview = sideview
                    EyeglassFrameDetectionResult_instance.topview = topview
                    # 保存三视图图片背景文件
                    EyeglassFrameDetectionResult_instance.frontview_bg = frontview_bg
                    EyeglassFrameDetectionResult_instance.sideview_bg = sideview_bg
                    EyeglassFrameDetectionResult_instance.topview_bg = topview_bg
                    # 保存镜架扫描结果表实例，并传入SKU，用于构建镜架三视图保存路径
                    EyeglassFrameDetectionResult_instance.save()
                else:
                    # 处理镜架扫描结果表表单验证失败的情况
                    err_msg = regular.get_err(form_EyeglassFrameDetectionResult)
                    # 抛出异常
                    raise ValueError(err_msg)
                
                """ 
                镜架风格关联表处理
                """
                # 提取镜架风格类型ID列表
                style_ids = request.POST.get("style")
                style_ids = json.loads(style_ids)
                for style_id in style_ids:
                    # 验证镜架风格关联表表单
                    form_EyeglassFrameEntryStyle = forms.EyeglassFrameEntryStyleForm({"entry": EyeglassFrameEntry_instance, "style": style_id})
                    if form_EyeglassFrameEntryStyle.is_valid():
                        # 构建并保存镜架风格关联表的数据库实例
                        EyeglassFrameEntryStyle_instance = form_EyeglassFrameEntryStyle.save(commit=False)
                        # 关联镜架基本信息表外键
                        EyeglassFrameEntryStyle_instance.entry = EyeglassFrameEntry_instance
                        # 保存镜架风格关联表实例
                        EyeglassFrameEntryStyle_instance.save()
                    else:
                        # 处理镜架风格关联表表单验证失败的情况
                        err_msg = regular.get_err(form_EyeglassFrameEntryStyle)
                        # 抛出异常
                        raise ValueError(err_msg)

                # 返回成功信息
                return R.ok(msg="新镜架创建成功")
            else:
                # 处理镜架基本信息表表单验证失败的情况
                err_msg = regular.get_err(form_EyeglassFrameEntry)
                # 抛出异常
                raise ValueError(err_msg)
    except ValueError as ve:
        return R.failed(msg=str(ve))
    except Exception as e:
        return R.failed(msg=str(e))
    
def SaveEditEyeglassFrame(request:HttpRequest):
    """
    编辑镜架，更新数据库实例：镜架基本信息表、镜架扫描结果表、镜架风格关联表

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数
    if not request.POST:
        return R.failed(msg="参数错误")
    # 获取修改镜架ID
    id = request.POST.get("id")
    # 镜架ID为空判断
    if not id:
        return R.failed(msg="镜架ID为空")

    # 查询镜架基本信息表实例
    EyeglassFrameEntry_instance = models.EyeglassFrameEntry.objects.filter(id=id).first()
    # 镜架基本信息表实例为空判断
    if not EyeglassFrameEntry_instance:
        return R.failed(msg="镜架ID不存在")
    
    try:
        # 数据库事务处理
        with transaction.atomic():
            """
            镜架基本信息表处理
            """
            # 验证镜架基本信息表表单
            form_EyeglassFrameEntry = forms.EyeglassFrameEntryForm(request.POST, instance=EyeglassFrameEntry_instance)
            if form_EyeglassFrameEntry.is_valid():
                # 删除镜架风格关联表实例
                models.EyeglassFrameEntryStyle.objects.filter(entry=EyeglassFrameEntry_instance).delete()
                # 保存镜架基本信息表实例
                EyeglassFrameEntry_instance = form_EyeglassFrameEntry.save()
                    
                """
                镜架扫描结果表处理
                """
                # 查询镜架扫描结果表实例
                EyeglassFrameDetectionResult_instance = models.EyeglassFrameDetectionResult.objects.filter(entry=EyeglassFrameEntry_instance).first()
                # 镜架扫描结果表实例为空判断
                if not EyeglassFrameDetectionResult_instance:
                    # 抛出异常
                    raise ValueError("镜架扫描结果表实例为空")
                # 创建镜架扫描结果表实例
                form_EyeglassFrameDetectionResult = forms.EyeglassFrameDetectionResultForm(request.POST, instance=EyeglassFrameDetectionResult_instance)
                # 验证镜架扫描结果表表单
                if form_EyeglassFrameDetectionResult.is_valid():
                    # 保存镜架扫描结果表实例
                    EyeglassFrameDetectionResult_instance = form_EyeglassFrameDetectionResult.save()
                else:
                    # 处理镜架扫描结果表表单验证失败的情况
                    err_msg = regular.get_err(form_EyeglassFrameDetectionResult)
                    # 抛出异常
                    raise ValueError(err_msg)

                """
                镜架风格关联表处理
                """
                # 提取镜架风格类型ID列表
                style_ids = request.POST.get("style")
                style_ids = json.loads(style_ids)
                for style_id in style_ids:
                    # 验证镜架风格关联表表单
                    form_EyeglassFrameEntryStyle = forms.EyeglassFrameEntryStyleForm({"entry": EyeglassFrameEntry_instance, "style": style_id})
                    if form_EyeglassFrameEntryStyle.is_valid():
                        # 构建并保存镜架风格关联表的数据库实例
                        EyeglassFrameEntryStyle_instance = form_EyeglassFrameEntryStyle.save(commit=False)
                        # 关联镜架基本信息表外键
                        EyeglassFrameEntryStyle_instance.entry = EyeglassFrameEntry_instance
                        # 保存镜架风格关联表实例
                        EyeglassFrameEntryStyle_instance.save()
                    else:
                        # 处理镜架风格关联表表单验证失败的情况
                        err_msg = regular.get_err(form_EyeglassFrameEntryStyle)
                        # 抛出异常
                        raise ValueError(err_msg)
                    
                # 返回成功信息
                return R.ok(msg="镜架编辑成功")
            else:
                # 处理镜架基本信息表表单验证失败的情况
                err_msg = regular.get_err(form_EyeglassFrameEntry)
                # 抛出异常
                raise ValueError(err_msg)
    except ValueError as ve:
        return R.failed(msg=str(ve))
    except Exception as e:
        return R.failed(msg=str(e))

def GetEyeglassFrameDetail(request:HttpRequest):
    """
    查询镜架详情

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数
    id = request.GET.get("id")

    # 参数为空判断
    if not id:
        return R.failed(msg="查询参数为空")
    
    # 查询镜架基本信息表
    eyeglassframeentry_result = models.EyeglassFrameEntry.objects.filter(id=id).first()
    # 判断查询结果是否为空
    if not eyeglassframeentry_result:
        return R.failed(msg="镜架不存在")
    # 查询镜架扫描结果表
    eyeglassframedetectionresult_result = models.EyeglassFrameDetectionResult.objects.filter(entry=eyeglassframeentry_result).first()
    # 查询镜架风格关联表
    eyeglassframeentrystyle_result = models.EyeglassFrameEntryStyle.objects.filter(entry=eyeglassframeentry_result)
    # 构建查询结果
    search_result = {
        # 镜架基本信息表
        'sku': eyeglassframeentry_result.sku,  # 镜架SKU，唯一
        'brand': eyeglassframeentry_result.brand,
        'model_type': eyeglassframeentry_result.model_type,
        'price': eyeglassframeentry_result.price,
        'material': eyeglassframeentry_result.material.id,
        'color': eyeglassframeentry_result.color.id,
        'shape': eyeglassframeentry_result.shape.id,
        'isnosepad': eyeglassframeentry_result.isnosepad,
        'stock': eyeglassframeentry_result.stock,
        'lens_radian': eyeglassframeentry_result.lens_radian,
        # 镜架风格关联表
        'style': [style.style.id for style in eyeglassframeentrystyle_result],
        # 镜架扫描结果表
        # 正视图
        'frontview': utils.getImageURL(str(eyeglassframedetectionresult_result.frontview)),
        'sideview': utils.getImageURL(str(eyeglassframedetectionresult_result.sideview)),
        'topview': utils.getImageURL(str(eyeglassframedetectionresult_result.topview)),
        'frame_height': eyeglassframedetectionresult_result.frame_height,
        'frame_width': eyeglassframedetectionresult_result.frame_width,
        'pile_height_left': eyeglassframedetectionresult_result.pile_height_left,
        'pile_height_right': eyeglassframedetectionresult_result.pile_height_right,
        'frame_top_width' : eyeglassframedetectionresult_result.frame_top_width,
        'top_points': eyeglassframedetectionresult_result.top_points, # 需要解析
        'frame_rects': eyeglassframedetectionresult_result.frame_rects, # 需要解析
        'lens_width_left': eyeglassframedetectionresult_result.lens_width_left,
        'lens_width_right': eyeglassframedetectionresult_result.lens_width_right,
        'lens_height_left': eyeglassframedetectionresult_result.lens_height_left,
        'lens_height_right': eyeglassframedetectionresult_result.lens_height_right,
        'lens_diagonal_left': eyeglassframedetectionresult_result.lens_diagonal_left,
        'lens_diagonal_right': eyeglassframedetectionresult_result.lens_diagonal_right,
        'lens_area_left': eyeglassframedetectionresult_result.lens_area_left,
        'lens_area_right': eyeglassframedetectionresult_result.lens_area_right,
        'bridge_width': eyeglassframedetectionresult_result.bridge_width,
        'lens_center_points': eyeglassframedetectionresult_result.lens_center_points, # 需要解析
        'lens_top_points': eyeglassframedetectionresult_result.lens_top_points, # 需要解析
        'pile_distance': eyeglassframedetectionresult_result.pile_distance,
        # 侧视图
        'vertical_angle': eyeglassframedetectionresult_result.vertical_angle,
        'forward_angle': eyeglassframedetectionresult_result.forward_angle,
        'temple_angle': eyeglassframedetectionresult_result.temple_angle,
        'drop_length': eyeglassframedetectionresult_result.drop_length,
        # 俯视图
        'face_angle': eyeglassframedetectionresult_result.face_angle,
        'sagittal_angle_left': eyeglassframedetectionresult_result.sagittal_angle_left,
        'sagittal_angle_right': eyeglassframedetectionresult_result.sagittal_angle_right,
        'temple_length_left': eyeglassframedetectionresult_result.temple_length_left,
        'temple_length_right': eyeglassframedetectionresult_result.temple_length_right,
        'temporal_width': eyeglassframedetectionresult_result.temporal_width,
        'spread_angle_left': eyeglassframedetectionresult_result.spread_angle_left,
        'spread_angle_right': eyeglassframedetectionresult_result.spread_angle_right,
        # 重量
        'weight': eyeglassframedetectionresult_result.weight,
    }

    # 返回查询结果
    return R.ok(data=search_result)

def GetAllEyeglassFrameEntrys(request:HttpRequest):
    """
    获取所有镜架的基本信息

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 获取页码，若无则默认为1
    page = int(request.GET.get("page", 1))
    # 获取每页显示数量，若无则默认为10
    page_size = int(request.GET.get("pageSize", 10))
    # 获取排序字段，默认为更新时间
    sort_field = request.GET.get("sortField", "update_time")
    # 获取排序方式，默认为降序
    sort_order = request.GET.get("sortOrder", "descend")
    # 获取查询关键字
    search_key_sku = request.GET.get("sku") # 镜架SKU
    search_key_brand = request.GET.get("brand") # 镜架品牌
    search_key_model_type = request.GET.get("model_type") # 镜架型号
    search_key_min_price = request.GET.get("searchMinPrice") # 镜架最低价格
    search_key_min_price = decimal.Decimal(search_key_min_price) if search_key_min_price else None
    search_key_max_price = request.GET.get("searchMaxPrice") # 镜架最高价格
    search_key_max_price = decimal.Decimal(search_key_max_price) if search_key_max_price else None
    search_key_material = request.GET.getlist("material[]") # 镜架材质id列表

    # 查询所有镜架基本信息表
    entrys = models.EyeglassFrameEntry.objects.all()

    # 判断查询结果是否为空
    if not entrys:
        return R.failed(msg="镜架基本信息为空")
    
    # 根据查询关键字筛选
    if search_key_sku:
        entrys = entrys.filter(sku__contains=search_key_sku)
    if search_key_brand:
        entrys = entrys.filter(brand__contains=search_key_brand)
    if search_key_model_type:
        entrys = entrys.filter(model_type__contains=search_key_model_type)
    if search_key_min_price:
        entrys = entrys.filter(price__gte=search_key_min_price)
    if search_key_max_price:
        entrys = entrys.filter(price__lte=search_key_max_price)
    if search_key_material:
        entrys = entrys.filter(material__in=search_key_material)

    # 排序
    if sort_order == "descend":
        entrys = entrys.order_by(f"-{sort_field}")
    else:
        entrys = entrys.order_by(sort_field)

    # 设置分页
    paginator = Paginator(entrys, page_size)
    # 记录总数
    count = paginator.count
    # 分页查询
    entry_list = paginator.page(page)
    # 实例化查询结果
    search_result = []
    # 构建查询结果
    if len(entry_list) > 0:
        search_result = [{
            'id': entry.id,  # 镜架ID,主键
            'sku': entry.sku,  # 镜架SKU，唯一
            'brand': entry.brand,
            'model_type': entry.model_type,
            'price': entry.price,
            'material': entry.material.id,
            'color': entry.color.id,
            'shape': entry.shape.id,
            'isnosepad': entry.isnosepad,
            'stock': entry.stock,
            'lens_radian': entry.lens_radian,
            'style': [style.style.id for style in models.EyeglassFrameEntryStyle.objects.filter(entry=entry).all()],  # 镜架风格关联表，多对多关系
            'create_time': entry.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': entry.update_time.strftime('%Y-%m-%d %H:%M:%S')
        } for entry in entry_list]

    # 返回查询结果
    return R.ok(data=search_result, count=count)

def GetAllBrands(request:HttpRequest):
    """
    获取所有镜架品牌

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """

    # 查询所有镜架品牌
    entrys = models.EyeglassFrameEntry.objects.all()

    # 判断查询结果是否为空
    if not entrys:
        return R.failed(msg="镜架基本信息为空")

    # 构建查询结果
    search_result = list(set([entry.brand for entry in entrys]))

    # 返回查询结果
    return R.ok(data=search_result)

def GetAllModelTypes(request:HttpRequest):
    """
    获取所有镜架型号

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """

    # 查询所有镜架型号
    entrys = models.EyeglassFrameEntry.objects.all()

    # 判断查询结果是否为空
    if not entrys:
        return R.failed(msg="镜架基本信息为空")

    # 构建查询结果
    search_result = list(set([entry.model_type for entry in entrys]))

    # 返回查询结果
    return R.ok(data=search_result)

def GetAllMaterials(request:HttpRequest):
    """
    获取所有镜架材质

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """

    # 查询所有镜架材质
    material_types = models.EyeglassFrameMaterialType.objects.all()

    # 判断查询结果是否为空
    if not material_types:
        return R.failed(msg="镜架材质为空")

    # 构建查询结果
    search_result = [{
        'id': material_type.id,
        'material': material_type.material
    } for material_type in material_types]

    # 返回查询结果
    return R.ok(data=search_result)

def GetAllColors(request:HttpRequest):
    """
    获取所有镜架颜色

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 查询所有镜架颜色
    color_types = models.EyeglassFrameColorType.objects.all()

    # 判断查询结果是否为空
    if not color_types:
        return R.failed(msg="镜架颜色为空")

    # 构建查询结果
    search_result = [{
        'id': color_type.id,
        'color': color_type.color
    }for color_type in color_types]

    # 返回查询结果
    return R.ok(data=search_result)

def GetAllShapes(request:HttpRequest):
    """
    获取所有镜架形状

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """

    # 查询所有镜架形状
    shape_types = models.EyeglassFrameShapeType.objects.all()

    # 判断查询结果是否为空
    if not shape_types:
        return R.failed(msg="镜架形状为空")

    # 构建查询结果
    search_result = [{
        'id': shape_type.id,
        'shape': shape_type.shape
    }for shape_type in shape_types]

    # 返回查询结果
    return R.ok(data=search_result)

def GetAllStyles(request:HttpRequest):
    """
    获取所有镜架风格

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """

    # 查询所有镜架风格
    style_types = models.EyeglassFrameStyleType.objects.all()

    # 判断查询结果是否为空
    if not style_types:
        return R.failed(msg="镜架风格为空")

    # 构建查询结果
    search_result = [{
        'id': style_type.id,
        'style': style_type.style
    }for style_type in style_types]

    # 返回查询结果
    return R.ok(data=search_result)

# 推荐客户端

def RegisterRecommendationUser(request:HttpRequest):
    """
    查询推荐客户端用户

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数
    username = request.POST.get("username")

    # 参数为空或空字符串判断
    if not username.strip():
        return R.failed(msg="查询参数为空")
    
    try:
        # 直接使用get()方法进行查询，提高效率
        user = models.RecommendationUser.objects.get(username=username)
        return R.failed(msg="用户已存在")
    except models.RecommendationUser.DoesNotExist:
        pass
    
    # 验证推荐客户端用户表表单
    form_RecommendationUser = forms.RecommendationUserForm(request.POST)
    # 验证推荐客户端用户表表单
    if form_RecommendationUser.is_valid():
        # 构建并保存推荐客户端用户表的数据库实例
        RecommendationUser_instance = form_RecommendationUser.save()
        # 返回成功信息
        return R.ok(msg="用户注册成功")
    else:
        # 处理推荐客户端用户表表单验证失败的情况
        return R.failed(msg="用户名格式错误")

def SaveNewRecommendationUserFacialImageAndFacialScanResult(request:HttpRequest):
    """
    保存新推荐客户端用户人脸图片和人脸扫描数据，创建新的数据库实例：推荐客户端用户人脸图像表、推荐客户端用户人脸扫描数据表

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数
    if not request.POST:
        return R.failed(msg="参数错误")
    
    # 获取用户识别码
    username = request.POST.get("username")
    # 用户识别码为空判断
    if not username:
        return R.failed(msg="用户ID为空")
    
    # 查询推荐客户端用户是否存在
    user = models.RecommendationUser.objects.filter(username=username).first()
    # 推荐客户端用户为空判断
    if not user:
        return R.failed(msg="用户不存在")
    
    try:
        # 数据库事务处理
        with transaction.atomic():
            """
            推荐客户端用户人脸图像表处理
            """
            # 创建推荐客户端用户人脸图像表实例
            form_RecommendationUserFacialImage = forms.RecommendationUserFacialImageForm(request.POST)
            # 验证推荐客户端用户人脸图像表表单
            if form_RecommendationUserFacialImage.is_valid():
                # 构建并保存推荐客户端用户人脸图像表的数据库实例
                RecommendationUserFacialImage_instance = form_RecommendationUserFacialImage.save(commit=False)
                # 关联推荐客户端用户基础信息表外键
                RecommendationUserFacialImage_instance.user = user
                # 获取人脸图像文件
                frontview = request.FILES.get("frontview")
                leftview = request.FILES.get("leftview")
                rightview = request.FILES.get("rightview")
                # 获取人脸图像文件错误处理
                if not frontview or not leftview or not rightview:
                    # 抛出异常
                    raise ValueError("人脸图像不能为空")
                # 保存人脸图像文件
                RecommendationUserFacialImage_instance.frontview = frontview
                RecommendationUserFacialImage_instance.leftview = leftview
                RecommendationUserFacialImage_instance.rightview = rightview
                # 保存推荐客户端用户人脸图像表实例
                RecommendationUserFacialImage_instance.save()
            else:
                # 处理推荐客户端用户人脸图像表表单验证失败的情况
                err_msg = regular.get_err(form_RecommendationUserFacialImage)
                # 抛出异常
                raise ValueError(err_msg)
            
            """
            推荐客户端用户人脸扫描数据表处理
            """
            # 创建推荐客户端用户人脸扫描数据表实例
            form_RecommendationUserFacialScanResult = forms.RecommendationUserFacialScanResultForm(request.POST)
            # 验证推荐客户端用户人脸扫描数据表表单
            if form_RecommendationUserFacialScanResult.is_valid():
                # 构建并保存推荐客户端用户人脸扫描数据表的数据库实例
                RecommendationUserFacialScanResult_instance = form_RecommendationUserFacialScanResult.save(commit=False)
                # 关联推荐客户端用户基础信息表外键
                RecommendationUserFacialScanResult_instance.user = user
                # 保存推荐客户端用户人脸扫描数据表实例
                RecommendationUserFacialScanResult_instance.save()
            else:
                # 处理推荐客户端用户人脸扫描数据表表单验证失败的情况
                err_msg = regular.get_err(form_RecommendationUserFacialScanResult)
                # 抛出异常
                raise ValueError(err_msg)
            
            # 返回成功信息
            return R.ok(msg="人脸图片保存成功")
    except ValueError as ve:
        return R.failed(msg=str(ve))
    except Exception as e:
        return R.failed(msg=str(e))
    
def SaveNewRecommendationUserBaseInfoAndOptometryAndLens(request:HttpRequest):
    """
    保存新推荐客户端用户基础信息、验光信息和镜片需求，创建新的数据库实例：推荐客户端用户基础信息表、推荐客户端用户验光信息表、推荐客户端用户镜片需求表

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数
    if not request.POST:
        return R.failed(msg="参数错误")
    
    # 获取用户识别码
    username = request.POST.get("username")
    # 用户识别码为空判断
    if not username:
        return R.failed(msg="用户ID为空")
    
    # 查询推荐客户端用户是否存在
    user = models.RecommendationUser.objects.filter(username=username).first()
    # 推荐客户端用户为空判断
    if not user:
        return R.failed(msg="用户不存在")
    
    try:
        # 数据库事务处理
        with transaction.atomic():
            """
            推荐客户端用户基础信息表处理
            """
            # 创建推荐客户端用户基础信息表实例
            form_RecommendationUserBaseInfo = forms.RecommendationUserBaseInfoForm(request.POST)
            # 验证推荐客户端用户基础信息表表单
            if form_RecommendationUserBaseInfo.is_valid():
                # 保存推荐客户端用户基础信息表实例
                RecommendationUserBaseInfo_instance = form_RecommendationUserBaseInfo.save(commit=False)
                # 关联推荐客户端用户基础信息表外键
                RecommendationUserBaseInfo_instance.user = user
                # 保存推荐客户端用户基础信息表实例
                RecommendationUserBaseInfo_instance.save()
            else:
                # 处理推荐客户端用户基础信息表表单验证失败的情况
                err_msg = regular.get_err(form_RecommendationUserBaseInfo)
                # 抛出异常
                raise ValueError(err_msg)
            
            """
            推荐客户端用户验光信息表处理
            """
            # 创建推荐客户端用户验光信息表实例
            form_RecommendationUserOptometry = forms.RecommendationUserOptometryForm(request.POST)
            # 验证推荐客户端用户验光信息表表单
            if form_RecommendationUserOptometry.is_valid():
                # 构建并保存推荐客户端用户验光信息表的数据库实例
                RecommendationUserOptometry_instance = form_RecommendationUserOptometry.save(commit=False)
                # 关联推荐客户端用户基础信息表外键
                RecommendationUserOptometry_instance.user = user
                # 保存推荐客户端用户验光信息表实例
                RecommendationUserOptometry_instance.save()
            else:
                # 处理推荐客户端用户验光信息表表单验证失败的情况
                err_msg = regular.get_err(form_RecommendationUserOptometry)
                # 抛出异常
                raise ValueError(err_msg)
            
            """
            推荐客户端用户镜片需求表处理
            """
            # 创建推荐客户端用户镜片需求表实例
            form_RecommendationUserLens = forms.RecommendationUserLensForm(request.POST)
            # 验证推荐客户端用户镜片需求表表单
            if form_RecommendationUserLens.is_valid():
                # 构建并保存推荐客户端用户镜片需求表的数据库实例
                RecommendationUserLens_instance = form_RecommendationUserLens.save(commit=False)
                # 关联推荐客户端用户基础信息表外键
                RecommendationUserLens_instance.user = user
                # 保存推荐客户端用户镜片需求表实例
                RecommendationUserLens_instance.save()
            else:
                # 处理推荐客户端用户镜片需求表表单验证失败的情况
                err_msg = regular.get_err(form_RecommendationUserLens)
                # 抛出异常
                raise ValueError(err_msg)
            
            # 返回成功信息
            return R.ok(msg="用户信息保存成功")
    except ValueError as ve:
        return R.failed(msg=str(ve))
    except Exception as e:
        return R.failed(msg=str(e))



# # 查询推荐客户端用户验光信息表
# optometry = models.RecommendationUserOptometry.objects.filter(user=user).first()
# # 查询推荐客户端用户镜片需求表
# lens = models.RecommendationUserLens.objects.filter(user=user).first()
# # 查询推荐客户端用户人脸扫描数据表
# facial_scan_result = models.RecommendationUserFacialScanResult.objects.filter(user=user).first()

# # 判断查询结果是否为空
# if not optometry or not lens or not facial_scan_result:
#     return R.failed(msg="用户数据不完整")

# # 构建查询结果
# search_result = {
#     # 推荐客户端用户基础信息表
#     'id': user.id,  # 用户ID,主键
#     'username': user.username,  # 用户名，唯一
#     'gender': user.gender,
#     'age_range': user.age_range,
#     # 推荐客户端用户验光信息表
#     'pupil_distance': optometry.pupil_distance,
#     'myopia_hyperopia_left': optometry.myopia_hyperopia_left,
#     'myopia_hyperopia_right': optometry.myopia_hyperopia_right,
#     'astigmatism_left': optometry.astigmatism_left,
#     'astigmatism_right': optometry.astigmatism_right,
#     # 推荐客户端用户镜片需求表
#     'refractive_index': lens.refractive_index,
#     'diameter': lens.diameter,
#     'density': lens.density,
#     # 推荐客户端用户人脸扫描数据表
#     'outer_canthic_diameter': facial_scan_result.outer_canthic_diameter,
#     'inner_canthic_diameter': facial_scan_result.inner_canthic_diameter,
#     'eye_width_left': facial_scan_result.eye_width_left,
#     'eye_width_right': facial_scan_result.eye_width_right,
#     'eye_height_left': facial_scan_result.eye_height_left,
#     'eye_height_right': facial_scan_result.eye_height_right,
#     'ala_nasi_width': facial_scan_result.ala_nasi_width,
#     'nasion_width': facial_scan_result.nasion_width,
#     'nose_height': facial_scan_result.nose_height,
#     'nose_pivot_angle': facial_scan_result.nose_pivot_angle,
#     'head_width': facial_scan_result.head_width,
#     'side_face_length_left': facial_scan_result.side_face_length_left,
#     'side_face_length_right': facial_scan_result.side_face_length_right,
#     'outer_canthic_ear_left': facial_scan_result.outer_canthic_ear_left,
#     'outer_canthic_ear_right': facial_scan_result.outer_canthic_ear_right,
#     'eyebrow_center_width': facial_scan_result.eyebrow_center_width,
#     'face_height': facial_scan_result.face_height,
#     'lip_width': facial_scan_result.lip_width,
#     'lip_height': facial_scan_result.lip_height,
#     'face_type': facial_scan_result.face_type,
#     'skin_color_type': facial_scan_result.skin_color_type,
# }








