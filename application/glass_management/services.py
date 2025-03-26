import json
import decimal
from utils import R, regular
from utils import utils
from django.db import transaction
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, HttpRequest

from application.glass_management import models
from application.glass_management import forms

from application.celery_task import tasks
from application.celery_task.services import search_calc_task


# 镜架采集端
def SearchModeltypeOrSKU(request: HttpRequest):
    """
    查询型号SKU

    参数：
        request: HttpRequest 请求对象
        modeltype: str 镜架型号
        sku: str 镜架SKU

    返回：
        HttpResponse: JSON格式的响应对象，{code,data,msg}
    """

    # 获取镜架型号和SKU
    searchtype = request.POST.get("skuormodeltype", "")
    searchstring = request.POST.get("searchString", "")

    # 参数为空判断
    if not searchtype or not searchstring:
        return R.failed(msg="请求表单错误")

    # 查询镜架型号或SKU是否存在，其中sku是唯一的
    if searchtype == "1":
        entrys = models.EyeglassFramePreloadData.objects.filter(
            model_type__icontains=searchstring
        )
    elif searchtype == "2":
        entrys = models.EyeglassFramePreloadData.objects.filter(
            sku__icontains=searchstring
        )

    # 通过sku字段，过滤已经存在于EyeglassFrameEntry表中的数据
    entrys = entrys.exclude(
        sku__in=[entry.sku for entry in models.EyeglassFrameEntry.objects.all()]
    )

    # 限制返回结果数量最多为50条
    entrys = entrys[:50]

    # 判断查询结果是否为空
    if not entrys:
        return R.ok(msg="未找到该镜架型号或SKU")

    # 先将字典列表转换为元组列表，便于去重
    tuple_search_result = [
        (
            entry.sku,
            entry.brand,
            entry.model_type,
            entry.price,
            entry.lens_width_st,
            entry.bridge_width_st,
            entry.temple_length_st,
            entry.model_type if searchtype == "1" else entry.sku,
        )
        for entry in entrys
    ]

    # 去重
    tuple_search_result = list(set(tuple_search_result))

    # 再将元组列表转换为字典列表
    search_result = [
        {
            "sku": entry[0],  # 镜架SKU，唯一
            "brand": entry[1],
            "model_type": entry[2],
            "price": entry[3],
            "lens_width_st": entry[4],
            "bridge_width_st": entry[5],
            "temple_length_st": entry[6],
            "value": entry[7],
        }
        for entry in tuple_search_result
    ]

    # # 构建查询结果
    # search_result = [
    #     {
    #         "sku": entry.sku,  # 镜架SKU，唯一
    #         "brand": entry.brand,
    #         "model_type": entry.model_type,
    #         "price": entry.price,
    #         "stock": entry.stock,
    #         "lens_width_st": entry.lens_width_st,
    #         "bridge_width_st": entry.bridge_width_st,
    #         "temple_length_st": entry.temple_length_st,
    #         "value": entry.model_type if searchtype == "1" else entry.sku,
    #     }
    #     for entry in entrys
    # ]

    # 返回查询结果
    return R.ok(data=search_result)


def SearchSKU(request: HttpRequest):
    """
    查询镜架SKU

    参数：
        request: HttpRequest 请求对象
        sku: str 镜架SKU

    返回：
        HttpResponse: JSON格式的响应对象，{code,data,msg}
    """

    # 获取镜架SKU
    sku = request.GET.get("sku", "")
    # print(sku)
    # 参数为空判断
    if not sku:
        return R.failed(msg="请输入镜架SKU")

    # 查询镜架SKU是否存在，其中sku是唯一的
    entry = models.EyeglassFrameEntry.objects.filter(sku=sku).first()

    # 判断查询结果是否为空
    if not entry:
        # 从EyeglassFrameDataFromExcel表中查询
        entry_fromexcel = models.EyeglassFramePreloadData.objects.filter(
            sku=sku
        ).first()
        if entry_fromexcel:
            if not entry_fromexcel.price:
                price = 1
            else:
                price = entry_fromexcel.price
            # 构建查询结果
            search_result = {
                "sku": entry_fromexcel.sku,  # 镜架SKU，唯一
                "brand": entry_fromexcel.brand,
                "model_type": entry_fromexcel.model_type,
                "price": price,
                "stock": entry_fromexcel.stock,
                "lens_width_st": entry_fromexcel.lens_width_st,
                "bridge_width_st": entry_fromexcel.bridge_width_st,
                "temple_length_st": entry_fromexcel.temple_length_st,
            }
            # 返回查询结果
            return R.ok(msg="镜架信息载入成功", data=search_result)
        else:
            return R.ok(msg="未能找到该SKU的镜架信息，请检查SKU或手动填写镜架信息")

    # 构建查询结果
    search_result = {
        "id": entry.id,  # 镜架ID,主键
        "sku": entry.sku,  # 镜架SKU，唯一
        "brand": entry.brand,
        "model_type": entry.model_type,
        "price": entry.price,
        "material": entry.get_material_display(),
        "color": entry.get_color_display(),
        "shape": entry.get_shape_display(),
        "isnosepad": entry.isnosepad,
        "lens_radian": entry.lens_radian,
        "stock": entry.stock,
        "warehouse": entry.warehouse.id,
        "create_time": entry.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        "update_time": entry.update_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # 返回查询结果
    return R.failed(msg="镜架已入库", data=search_result)


def DeleteEyeglassFrameEntrys(request: HttpRequest):
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

def UploadNewEyeglassFrame(request: HttpRequest):
    """
    保存新镜架：基本信息，三视图；生成计算任务
    
    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}

    """
    # 接收请求参数,前端提交的是formdata，所以从request.POST中获取数据。如果前端提交的是json数据，则从request.body中获取数据。
    if not request.POST:
        return R.failed(msg="参数错误")
    try:
        # 数据库事务处理
        with transaction.atomic():
            """
            镜架基本信息表处理
            """
            # 创建镜架扫描结果表实例
            form_EyeglassFrameEntry = (
                forms.EyeglassFrameEntryForm(request.POST)
            )
            # 验证镜架基本信息表表单
            if form_EyeglassFrameEntry.is_valid():
                # 保存镜架基本信息表实例
                EyeglassFrameEntry_instance = form_EyeglassFrameEntry.save(commit=False)
                # 保存镜架计算状态为0待计算
                EyeglassFrameEntry_instance.pixel_measurement_state = 0
                EyeglassFrameEntry_instance.millimeter_measurement_state = 0
                EyeglassFrameEntry_instance.calculation_state = 0
                EyeglassFrameEntry_instance.coordinate_state = 0
                EyeglassFrameEntry_instance.image_mask_state = 0
                EyeglassFrameEntry_instance.image_seg_state = 0
                EyeglassFrameEntry_instance.image_beautify_state = 0
                EyeglassFrameEntry_instance.save()
                """
                镜架图片数据表处理
                """
                # 构建并保存镜架图片数据表的数据库实例，关联镜架基本信息表外键，储存图像
                EyeglassFrameImage_instance = models.EyeglassFrameImage.objects.create(entry = EyeglassFrameEntry_instance)
                # 获取三视图图片文件
                frontview = request.FILES.get("frontview")
                sideview = request.FILES.get("sideview")
                topview = request.FILES.get("topview")
                # 获取三视图图片背景文件
                # frontview_bg = request.FILES.get("frontview_bg")
                # sideview_bg = request.FILES.get("sideview_bg")
                # topview_bg = request.FILES.get("topview_bg")
                # 获取三视图图片错误处理
                if (
                    not frontview
                    or not sideview
                    or not topview
                    # or not frontview_bg
                    # or not sideview_bg
                    # or not topview_bg
                ):
                    # 抛出异常
                    raise ValueError("三视图图片不能为空")
                # 保存三视图图片文件
                EyeglassFrameImage_instance.frontview = frontview
                EyeglassFrameImage_instance.sideview = sideview
                EyeglassFrameImage_instance.topview = topview
                # 保存镜架扫描结果表实例，并传入SKU，用于构建镜架三视图保存路径
                EyeglassFrameImage_instance.save()
                print("GenerateCalculateTask:",id)
            """
            生成celery计算任务：传递镜架基础信息表的sku值
            """
            sku = request.POST.get("sku")
            task_id = tasks.calc.delay(sku)
            return R.ok(msg="生成计算任务成功："+str(task_id))
            # return R.ok(msg="保存成功")
            # else:
            #     # 处理镜架基本信息表表单验证失败的情况
            #     err_msg = regular.get_err(form_EyeglassFrameEntry)
            #     # 抛出异常
            #     raise ValueError(err_msg)
    except ValueError as ve:
        return R.failed(msg=str(ve))
    except Exception as e:
        return R.failed(msg=str(e))
   
def GenerateCalculateTask(request: HttpRequest):
    """
    生成计算任务

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
    EyeglassFrameEntry_instance = models.EyeglassFrameEntry.objects.filter(
        id=id
    ).first()
    # 镜架基本信息表实例为空判断
    if not EyeglassFrameEntry_instance:
        return R.failed(msg="镜架ID不存在")
    # 判断镜架已经在计算队列中
    if search_calc_task(EyeglassFrameEntry_instance.sku):
        return R.failed(msg="镜架已在计算队列中")
    # 判断镜架是否正在计算中
    if EyeglassFrameEntry_instance.pixel_measurement_state == 1 or EyeglassFrameEntry_instance.millimeter_measurement_state == 1 or EyeglassFrameEntry_instance.calculation_state == 1 or EyeglassFrameEntry_instance.coordinate_state == 1 or EyeglassFrameEntry_instance.image_mask_state == 1 or EyeglassFrameEntry_instance.image_seg_state == 1 or EyeglassFrameEntry_instance.image_beautify_state == 1 :
        return R.failed(msg="镜架正在计算中")
    # 添加镜架到计算队列中
    try:
        # 数据库事务处理
        with transaction.atomic():
            # 更改计算状态为待计算
            EyeglassFrameEntry_instance.pixel_measurement_state = 0
            EyeglassFrameEntry_instance.millimeter_measurement_state = 0
            EyeglassFrameEntry_instance.calculation_state = 0
            EyeglassFrameEntry_instance.coordinate_state = 0
            EyeglassFrameEntry_instance.image_mask_state = 0
            EyeglassFrameEntry_instance.image_seg_state = 0
            EyeglassFrameEntry_instance.image_beautify_state = 0
            """
            生成celery计算任务：传递镜架基础信息表的sku值
            """
            sku = EyeglassFrameEntry_instance.sku
            task_id = tasks.calc.delay(sku) 
            print("GenerateCalculateTask:", task_id)
            EyeglassFrameEntry_instance.save()
    except Exception as e:
        return R.failed(msg=str(e))
    return R.ok(msg="生成计算任务成功："+str(task_id))
#todo:该函数好像没用了，待删除
def SaveNewEyeglassFrame(request: HttpRequest):
    """
    保存新镜架，创建新的数据库实例：镜架基本信息表、镜架图片数据

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 接收请求参数,前端提交的是formdata，所以从request.POST中获取数据。如果前端提交的是json数据，则从request.body中获取数据。
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
                镜架图片数据：三视图
                """
                # 创建镜架扫描结果表实例
                form_EyeglassFrameImage = (
                    forms.EyeglassFrameImageForm(request.POST)
                )
                # 验证镜架扫描结果表表单
                if form_EyeglassFrameImage.is_valid():
                    # 构建并保存镜架扫描结果表的数据库实例
                    EyeglassFrameImage_instance = (
                        form_EyeglassFrameImage.save(commit=False)
                    )
                    # 关联镜架基本信息表外键
                    EyeglassFrameImage_instance.entry = (
                        EyeglassFrameEntry_instance
                    )
                    # 获取三视图图片文件
                    frontview = request.FILES.get("frontview")
                    sideview = request.FILES.get("sideview")
                    topview = request.FILES.get("topview")
                    # 获取三视图图片背景文件
                    # frontview_bg = request.FILES.get("frontview_bg")
                    # sideview_bg = request.FILES.get("sideview_bg")
                    # topview_bg = request.FILES.get("topview_bg")
                    # 获取三视图图片错误处理
                    if (
                        not frontview
                        or not sideview
                        or not topview
                        # or not frontview_bg
                        # or not sideview_bg
                        # or not topview_bg
                    ):
                        # 抛出异常
                        raise ValueError("三视图图片不能为空")
                    # 保存三视图图片文件
                    EyeglassFrameImage_instance.frontview = frontview
                    EyeglassFrameImage_instance.sideview = sideview
                    EyeglassFrameImage_instance.topview = topview
                    # # 保存三视图图片背景文件
                    # EyeglassFrameDetectionResult_instance.frontview_bg = frontview_bg
                    # EyeglassFrameDetectionResult_instance.sideview_bg = sideview_bg
                    # EyeglassFrameDetectionResult_instance.topview_bg = topview_bg
                    # 保存镜架扫描结果表实例，并传入SKU，用于构建镜架三视图保存路径
                    EyeglassFrameImage_instance.save()
                else:
                    # 处理镜架扫描结果表表单验证失败的情况
                    err_msg = regular.get_err(form_EyeglassFrameImage)
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


def SaveEditEyeglassFrame(request: HttpRequest):
    """
    编辑镜架，更新数据库实例：镜架基本信息表、镜架毫米测量数据

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
    EyeglassFrameEntry_instance = models.EyeglassFrameEntry.objects.filter(
        id=id
    ).first()
    # 镜架基本信息表实例为空判断
    if not EyeglassFrameEntry_instance:
        return R.failed(msg="镜架ID不存在")

    # 判断镜架正在计算中
    if EyeglassFrameEntry_instance.pixel_measurement_state == 1 or EyeglassFrameEntry_instance.millimeter_measurement_state == 1 or EyeglassFrameEntry_instance.calculation_state == 1 or EyeglassFrameEntry_instance.coordinate_state == 1 or EyeglassFrameEntry_instance.image_mask_state == 1 or EyeglassFrameEntry_instance.image_seg_state == 1 or EyeglassFrameEntry_instance.image_beautify_state == 1 :
        return R.failed(msg="镜架正在计算中")

    try:
        # 数据库事务处理
        with transaction.atomic():
            # 判断保存类型为基础信息
            if request.POST.get("save_type") == "basic":
                """
                镜架基本信息表处理
                """
                # 验证镜架基本信息表表单
                form_EyeglassFrameEntry = forms.EyeglassFrameEntryForm(
                    request.POST, instance=EyeglassFrameEntry_instance
                )
                if form_EyeglassFrameEntry.is_valid():
                    # 保存镜架基本信息表实例
                    EyeglassFrameEntry_instance = form_EyeglassFrameEntry.save()
                    # 返回成功信息
                    return R.ok(msg="镜架编辑成功")
                else:
                    # 处理镜架基本信息表表单验证失败的情况
                    err_msg = regular.get_err(form_EyeglassFrameEntry)
                    # 抛出异常
                    raise ValueError(err_msg)
                
            # 判断保存类型为详细信息（保存到毫米测量数据表）
            elif request.POST.get("save_type") == "explicit":
                """
                镜架毫米测量数据处理
                """
                print(request.POST)
                # 查询镜架毫米测量数据表实例
                EyeglassFrameMillimeterMeasurement_instance = (
                    models.EyeglassFrameMillimeterMeasurement.objects.filter(
                        entry=EyeglassFrameEntry_instance
                    ).first()
                )
                # 镜架毫米测量数据表实例为空判断
                if not EyeglassFrameMillimeterMeasurement_instance:
                    # 抛出异常
                    # raise ValueError("镜架毫米测量数据实例为空")
                    # 不存在镜架毫米测量数据表实例，则创建
                    form_EyeglassFrameMillimeterMeasurement = (
                        forms.EyeglassFrameMillimeterMeasurementForm(
                            request.POST
                        )
                    )
                else:
                    # 根据原有数据，创建镜架毫米测量数据表实例
                    form_EyeglassFrameMillimeterMeasurement = (
                        forms.EyeglassFrameMillimeterMeasurementForm(
                            request.POST, instance=EyeglassFrameMillimeterMeasurement_instance
                        )
                    )
                # 验证镜架毫米测量数据表表单
                if form_EyeglassFrameMillimeterMeasurement.is_valid():
                    # 保存镜架毫米测量数据表实例
                    EyeglassFrameMillimeterMeasurement_instance = (
                        form_EyeglassFrameMillimeterMeasurement.save(commit=False)
                    )
                    # 关联镜架基本信息表外键
                    EyeglassFrameMillimeterMeasurement_instance.entry = EyeglassFrameEntry_instance
                    EyeglassFrameMillimeterMeasurement_instance.save()
                else:
                    # 处理镜架毫米测量数据表表单验证失败的情况
                    err_msg = regular.get_err(form_EyeglassFrameMillimeterMeasurement)
                    # 抛出异常
                    raise ValueError(err_msg)

                # 返回成功信息
                return R.ok(msg="镜架编辑成功")
            else:
                raise ValueError("保存类型错误")
    except ValueError as ve:
        return R.failed(msg=str(ve))
    except Exception as e:
        return R.failed(msg=str(e))

def GetEyeglassFrameDetail(request: HttpRequest):
    """
    查询镜架详情: 镜架基本信息表 镜架毫米测量数据 镜架三视图1

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
    # 构建查询结果
    search_result = {
        # 镜架基本信息表
        "sku": eyeglassframeentry_result.sku,  # 镜架SKU，唯一
        "brand": eyeglassframeentry_result.brand,
        "model_type": eyeglassframeentry_result.model_type,
        "price": eyeglassframeentry_result.price,
        "material": eyeglassframeentry_result.material,
        "color": eyeglassframeentry_result.color,
        "shape": eyeglassframeentry_result.shape,
        "isnosepad": eyeglassframeentry_result.isnosepad,
        "is_transparent": eyeglassframeentry_result.is_transparent,
        "frame_type": eyeglassframeentry_result.frame_type,
        "lens_radian": eyeglassframeentry_result.lens_radian,
        "lens_width_st": eyeglassframeentry_result.lens_width_st,
        "bridge_width_st": eyeglassframeentry_result.bridge_width_st,
        "temple_length_st": eyeglassframeentry_result.temple_length_st,
        "weight": eyeglassframeentry_result.weight,
        "stock": eyeglassframeentry_result.stock,
        "warehouse": eyeglassframeentry_result.warehouse.id,
        # 计算状态
        "pixel_measurement_state":eyeglassframeentry_result.pixel_measurement_state,
        "millimeter_measurement_state":eyeglassframeentry_result.millimeter_measurement_state,
        "calculation_state":eyeglassframeentry_result.calculation_state,
        "coordinate_state":eyeglassframeentry_result.coordinate_state,
        "image_mask_state":eyeglassframeentry_result.image_mask_state,
        "image_seg_state":eyeglassframeentry_result.image_seg_state,
        "image_beautify_state":eyeglassframeentry_result.image_beautify_state,
    }
    # 查询镜架图片表
    EyeglassFrameImage_result = (
        models.EyeglassFrameImage.objects.filter(
            entry=eyeglassframeentry_result
        ).first()
    )

    if EyeglassFrameImage_result:
        # 镜架图片表
        search_result = dict(
            search_result,
            **{
                "frontview": utils.getImageURL(
                    str(EyeglassFrameImage_result.frontview)
                ),
                "sideview": utils.getImageURL(
                    str(EyeglassFrameImage_result.sideview)
                ),
                "topview": utils.getImageURL(str(EyeglassFrameImage_result.topview)),
            }
        )
    # 查询镜架扫描结果表
    EyeglassFrameMillimeterMeasurement_result = (
        models.EyeglassFrameMillimeterMeasurement.objects.filter(
            entry=eyeglassframeentry_result
        ).first()
    )
    if EyeglassFrameMillimeterMeasurement_result:
        measurment_result={
            # 镜架毫米测量数据
            "frame_height": EyeglassFrameMillimeterMeasurement_result.frame_height,
            "frame_width": EyeglassFrameMillimeterMeasurement_result.frame_width,
            "pile_height_left": EyeglassFrameMillimeterMeasurement_result.pile_height_left,
            "pile_height_right": EyeglassFrameMillimeterMeasurement_result.pile_height_right,
            "frame_top_width": EyeglassFrameMillimeterMeasurement_result.frame_top_width,
            "lens_width_left": EyeglassFrameMillimeterMeasurement_result.lens_width_left,
            "lens_width_right": EyeglassFrameMillimeterMeasurement_result.lens_width_right,
            "lens_height_left": EyeglassFrameMillimeterMeasurement_result.lens_height_left,
            "lens_height_right": EyeglassFrameMillimeterMeasurement_result.lens_height_right,
            "lens_diagonal_left": EyeglassFrameMillimeterMeasurement_result.lens_diagonal_left,
            "lens_diagonal_right": EyeglassFrameMillimeterMeasurement_result.lens_diagonal_right,
            "lens_area_left": EyeglassFrameMillimeterMeasurement_result.lens_area_left,
            "lens_area_right": EyeglassFrameMillimeterMeasurement_result.lens_area_right,
            "bridge_width": EyeglassFrameMillimeterMeasurement_result.bridge_width,
            # 侧视图
            "vertical_angle": EyeglassFrameMillimeterMeasurement_result.vertical_angle,
            "forward_angle": EyeglassFrameMillimeterMeasurement_result.forward_angle,
            "temple_angle": EyeglassFrameMillimeterMeasurement_result.temple_angle,
            "drop_length": EyeglassFrameMillimeterMeasurement_result.drop_length,
            # 俯视图
            "face_angle": EyeglassFrameMillimeterMeasurement_result.face_angle,
            "sagittal_angle_left": EyeglassFrameMillimeterMeasurement_result.sagittal_angle_left,
            "sagittal_angle_right": EyeglassFrameMillimeterMeasurement_result.sagittal_angle_right,
            "temple_length_left": EyeglassFrameMillimeterMeasurement_result.temple_length_left,
            "temple_length_right": EyeglassFrameMillimeterMeasurement_result.temple_length_right,
            "temporal_width": EyeglassFrameMillimeterMeasurement_result.temporal_width,
            "spread_angle_left": EyeglassFrameMillimeterMeasurement_result.spread_angle_left,
            "spread_angle_right": EyeglassFrameMillimeterMeasurement_result.spread_angle_right,
            "pile_distance": EyeglassFrameMillimeterMeasurement_result.pile_distance,
        }
        search_result=dict(search_result,**measurment_result)
    # 返回查询结果
    return R.ok(data=search_result)


def GetAllEyeglassFrameEntrys(request: HttpRequest):
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
    # search_key_warehouse = request.GET.get("warehouse") # 仓库ID
    search_key_sku = request.GET.get("sku")  # 镜架SKU
    search_key_brand = request.GET.get("brand")  # 镜架品牌
    search_key_model_type = request.GET.get("model_type")  # 镜架型号
    search_key_min_price = request.GET.get("searchMinPrice")  # 镜架最低价格
    search_key_min_price = (
        decimal.Decimal(search_key_min_price) if search_key_min_price else None
    )
    search_key_max_price = request.GET.get("searchMaxPrice")  # 镜架最高价格
    search_key_max_price = (
        decimal.Decimal(search_key_max_price) if search_key_max_price else None
    )
    search_key_material = request.GET.getlist("material[]")  # 镜架材质id列表

    # 查询所有镜架基本信息表
    entrys = models.EyeglassFrameEntry.objects.all()

    # 判断查询结果是否为空
    if not entrys:
        return R.failed(msg="镜架基本信息为空")

    # 根据查询关键字筛选
    # if search_key_warehouse:
    #     entrys = entrys.filter(warehouse__id=search_key_warehouse)
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
        search_result = [
            {
                "id": entry.id,  # 镜架ID,主键
                "sku": entry.sku,  # 镜架SKU，唯一
                "brand": entry.brand,
                "model_type": entry.model_type,
                "price": entry.price,
                "material": entry.material,
                "color": entry.color,
                "shape": entry.shape,
                "isnosepad": entry.isnosepad,
                "lens_radian": entry.lens_radian,
                "stock": entry.stock,
                "warehouse": entry.warehouse.id,
                  # 计算状态
                "pixel_measurement_state":entry.pixel_measurement_state,
                "millimeter_measurement_state":entry.millimeter_measurement_state,
                "calculation_state":entry.calculation_state,
                "coordinate_state":entry.coordinate_state,
                "image_mask_state":entry.image_mask_state,
                "image_seg_state":entry.image_seg_state,
                "image_beautify_state":entry.image_beautify_state,
                "create_time": entry.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "update_time": entry.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for entry in entry_list
        ]

    # 返回查询结果
    return R.ok(data=search_result, count=count)

def GetAllCalculateStates(request: HttpRequest):
    """
    获取指定 ID 列表的镜架计算状态
    
    Args:
        request: HTTP 请求对象，包含 ids 参数
        
    Returns:
        JSON响应：包含计算状态的列表
    """
    try:
        # 获取 ID 列表
        ids = request.GET.get("ids", "")
        if not ids:
            return R.failed(msg="未指定镜架 ID")
        # 将字符串转换为列表
        try:
            ids = [int(id) for id in ids.split(",")]
        except ValueError:
            return R.failed(msg="无效的镜架 ID")
            
        # 查询指定 ID 的镜架
        entries = models.EyeglassFrameEntry.objects.filter(id__in=ids)
        
        # 构建返回数据
        if len(entries) > 0:
            search_result = [{
            "id": entry.id,
            "pixel_measurement_state": entry.pixel_measurement_state,
            "millimeter_measurement_state": entry.millimeter_measurement_state, 
            "calculation_state": entry.calculation_state,
            "coordinate_state": entry.coordinate_state,
            "image_mask_state": entry.image_mask_state,
            "image_seg_state": entry.image_seg_state,
            "image_beautify_state": entry.image_beautify_state
            } for entry in entries]
        
        return R.ok(data=search_result)
        
    except Exception as e:
        return R.failed(msg=f"获取计算状态失败: {str(e)}")

def GetAllBrands(request: HttpRequest):
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


def GetAllModelTypes(request: HttpRequest):
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


def GetAllMaterials(request: HttpRequest):
    """
    获取所有镜架材质

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """

    # 查询所有镜架材质
    material_types = models.EyeglassFrameEntry.MATERIAL_CHOICES
   
    # 判断查询结果是否为空
    if not material_types:
        return R.failed(msg="镜架材质为空")
    
    # 构建查询结果
    search_result = [
        {"id": material_type[0], "material": material_type[1]}
        for material_type in material_types
    ]

    # 返回查询结果
    return R.ok(data=search_result)


def GetAllColors(request: HttpRequest):
    """
    获取所有镜架颜色

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """
    # 查询所有镜架颜色
    color_types = models.EyeglassFrameEntry.COLOR_CHOICES

    # 判断查询结果是否为空
    if not color_types:
        return R.failed(msg="镜架颜色为空")

    # 构建查询结果
    search_result = [
        {"id": color_type[0], "color": color_type[1]} for color_type in color_types
    ]

    # 返回查询结果
    return R.ok(data=search_result)


def GetAllShapes(request: HttpRequest):
    """
    获取所有镜架形状

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """

    # 查询所有镜架形状
    shape_types = models.EyeglassFrameEntry.SHAPE_CHOICES

    # 判断查询结果是否为空
    if not shape_types:
        return R.failed(msg="镜架形状为空")

    # 构建查询结果
    search_result = [
        {"id": shape_type[0], "shape": shape_type[1]} for shape_type in shape_types
    ]

    # 返回查询结果
    return R.ok(data=search_result)

def GetAllIsTransparent(request: HttpRequest):
    """
    获取所有镜架透明度

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """

    # 查询所有镜架形状
    is_transparent_types = models.EyeglassFrameEntry.IS_TRANSPARENT_CHOICES

    # 判断查询结果是否为空
    if not is_transparent_types:
        return R.failed(msg="镜架透明度为空")

    # 构建查询结果
    search_result = [
        {"id": is_transparent_type[0], "is_transparent": is_transparent_type[1]} for is_transparent_type in is_transparent_types
    ]

    # 返回查询结果
    return R.ok(data=search_result)

def GetAllFrameTypes(request: HttpRequest):
    """
    获取所有镜框类型

    参数：
        request: HttpRequest 请求对象

    返回：
        HttpResponse: JSON格式的响应对象, {code,data,msg}
    """

    # 查询所有镜架形状
    frame_types = models.EyeglassFrameEntry.FRAME_TYPE_CHOICES

    # 判断查询结果是否为空
    if not frame_types:
        return R.failed(msg="镜架透明度为空")

    # 构建查询结果
    search_result = [
        {"id": frame_type[0], "frame_type": frame_type[1]} for frame_type in frame_types
    ]

    # 返回查询结果
    return R.ok(data=search_result)
