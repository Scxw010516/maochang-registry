import random
import json
from typing import List
from django.http import JsonResponse
from application.maochang.models import EyeglassFrameDetectionResult, EyeglassFrameEntry, EyeglassFrameEntryStyle, EyeglassFrameStyleType

"""
生成测试用的24副镜架的基本信息
"""
def generate_testing_data_for_customer_ui_v2(request):
    random.seed(42)

    # 一共4个风格
    styles: List[EyeglassFrameEntry] = []
    style_names = ['学生', '通勤', '长者', '运动']
    for name in style_names:
        style = EyeglassFrameStyleType()
        style.style = name
        style.save()
        styles.append(style)
    prices = [200, 800, 1200, 1800, 2200, 2800]
    materials = ['钢', '钛合金']
    brands = ['Montblanc', 'SEIKO', 'HELEN KELLR']
    # 24个镜架，3（品牌） x 2（型号） x 2（材质）x 2 (售价)  每个镜架随机1种风格 每个镜架随机一个售价 [200-2000]

    eyeglass_frames: List[EyeglassFrameEntry] = []
    eyeglass_frames_styles: List[EyeglassFrameEntry] = []
    for brand in brands:
        for model_type_idx in range(0, 2):
            for material in materials:
                for i in range(2):
                    entry = EyeglassFrameEntry()
                    entry.brand = brand
                    entry.model_type = f'{brand}-XXX{model_type_idx+1}'
                    entry.price = random.choice(prices)
                    entry.material = material
                    eyeglass_frames.append(entry)
                    eyeglass_frames_styles.append(random.choice(styles))

    assert len(eyeglass_frames) == 24, len(eyeglass_frames)
    random.shuffle(eyeglass_frames)
    for eyeglass_frame in eyeglass_frames:
        eyeglass_frame.save()

    for i, style in enumerate(eyeglass_frames_styles):
        link = EyeglassFrameEntryStyle()
        link.entry = eyeglass_frames[i]
        link.style = style
        link.save()

    return JsonResponse(data={"result": 'ok'})

"""
为测试用的镜架绑定上黄晨同学之前提供的24副镜架参数，以进行人脸匹配
"""
def generate_testing_data_for_registry_ui(request):
    frames = EyeglassFrameEntry.objects.all()
    for i in range(len(frames)):
        params = json.loads(open(f'samples/glasses_new_processed/{str(i+1)}/parameters.json').read())
        detection = EyeglassFrameDetectionResult()
        detection.entry = frames[i]
        detection.foreview = f'face/glasses/glass{str(i+1)}.png'
        detection.lens_width = params["lens_width"]
        detection.lens_height = params["lens_height"]
        detection.width = params["width"]
        detection.bridge_width = params["bridge_width"]
        detection.temple_length = params["temple_length"]
        detection.weight = 8.0
        detection.nosepad = 0
        detection.diagonal = params["diagonal"]
        detection.framework_width = params["framework_width"]
        detection.temporal_width = params["temporal_width"]
        detection.glasses_length = params["glasses_length"]
        detection.pile_height = params["pile_height"]
        detection.save()
    return JsonResponse(data={"result": 'ok'})
# 
# samples\glasses_new_processed\1\parameters.json