import cv2
import traceback
from functools import lru_cache
import os
import numpy as np

from .calculate.front_calculator import FrontCalculator
from .calculate.left_calculator import LeftCalculator
from .calculate.up_calculator import UpCalculator
from .calculate_shape.cal_data import DataCalculator
from .config import default_options, default_output
from .detect.left_detector import LeftDetector
from .detect.up_detector import UpDetector
from .preprocess.front_preprocessor import FrontPreprocessor
from .preprocess.left_preprocessor import LeftPreprocessor
from .preprocess.nose_preprocessor import NosePreprocessor
from .preprocess.up_preprocessor import UpPreprocessor
from .segment.frame_segmentor import FrameSegmentor
from .segment.templeWf_segmentor import TempleWfSegmentor
from .segment.lens_segmentor import LensSegmentor
from .segment.nose_segmentor import NoseSegmentor
from .utils.clean_mask import clean
from .utils.format_point import format_point
from .utils.get_front import get_front_mask
from .beautify.ps import ps
from .beautify.ps_temple import ps_temple
from .convert.params_converter import ParamsConverter


def get_capture_images(sku=""):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    up_image_path = os.path.join(current_dir, "image", "capture", sku + "_0.jpg")
    front_image_path = os.path.join(current_dir, "image", "capture", sku + "_1.jpg")
    left_image_path = os.path.join(current_dir, "image", "capture", sku + "_2.jpg")
    up_image = cv2.imread(f"{up_image_path}")
    front_image = cv2.imread(f"{front_image_path}")
    left_image = cv2.imread(f"{left_image_path}")
    return {"up": up_image, "front": front_image, "left": left_image}


@lru_cache(maxsize=1)
def get_models():
    # segment
    fs = FrameSegmentor(device="cuda")
    ls = LensSegmentor(device="cuda")
    ns = NoseSegmentor(device="cuda")
    tws = TempleWfSegmentor(device="cuda")
    # detect
    ud = UpDetector(device="cuda")
    ld = LeftDetector(device="cuda")

    return {
        "seg_frame": fs,
        "seg_lens": ls,
        "seg_nose": ns,
        "seg_templeWf": tws,
        "det_up": ud,
        "det_left": ld,
    }


def process(images: dict, models: dict, options: dict = default_options):
    output = default_output
    up_image, front_image, left_image = images["up"], images["front"], images["left"]

    fs, ls, ns, tws, ud, ld = (
        models["seg_frame"],
        models["seg_lens"],
        models["seg_nose"],
        models["seg_templeWf"],
        models["det_up"],
        models["det_left"],
    )

    # preprocess
    up, fp, lp, nep = (
        UpPreprocessor(),
        FrontPreprocessor(),
        LeftPreprocessor(),
        NosePreprocessor(),
    )

    # 裁剪版本
    crop_version = options['crop_version']
    # 临时通过图像尺寸判断裁剪版本
    shape_h = up_image.shape[0]
    if shape_h == 3496:
        crop_version = 0
    if shape_h == 3000:
        crop_version = 1

    if crop_version == 1:
        regions = options['regions']
        up_preprocess_image = up.preprocess(up_image, regions['up'])
        front_preprocess_image = fp.preprocess(front_image, regions['front'])
        left_preprocess_image = lp.preprocess(left_image, regions['left'])
        nose_preprocess_image = nep.preprocess(front_preprocess_image, regions['nose'])
    elif crop_version == 0:
        up_preprocess_image = up.preprocess(up_image)
        front_preprocess_image = fp.preprocess(front_image)
        left_preprocess_image = lp.preprocess(left_image)
        nose_preprocess_image = nep.preprocess(front_image)
        regions = {"nose": [426, 1450, 1100, 2124]}

    else:
        raise ValueError('crop_version should be 0 or 1')

    # segment
    try:
        frame_mask = fs.segment(front_preprocess_image, is_one=False)
        lens_mask = ls.segment(front_preprocess_image, is_one=False)
        nose_mask = ns.segment(nose_preprocess_image, is_one=False)
        templeWf_mask = tws.segment(left_preprocess_image, is_one=False)

        output["mask"]["state"] = 1
        output["mask"]["data"]["frame"] = frame_mask
        output["mask"]["data"]["lens"] = lens_mask
        output["mask"]["data"]["nose"] = nose_mask
        output["mask"]["data"]["templeWf"] = templeWf_mask
    except Exception as e:
        return output

    # ## 后处理（去除小的mask，只保留大的）
    try:
        frame_mask = clean(frame_mask, area=10000, k=1)
        lens_mask = clean(lens_mask, area=10000, k=2)
        templeWf_mask = clean(templeWf_mask, area=10000, k=1)

        output["mask"]["state"] = 1
        output["mask"]["data"]["frame"] = frame_mask
        output["mask"]["data"]["lens"] = lens_mask
        output["mask"]["data"]["nose"] = nose_mask
        output["mask"]["data"]["templeWf"] = templeWf_mask
    except Exception as e:
        return output

    # detect
    try:
        up_points = ud.detect(up_preprocess_image)
        left_points = ld.detect(left_preprocess_image)

        output["point"]["state"] = 1
        output["point"]["data"]["up"] = up_points
        output["point"]["data"]["left"] = left_points
    except Exception as e:
        return output

    # 计算参数
    try:
        fc = FrontCalculator(frame_image=frame_mask, lens_image=lens_mask)
        lc = LeftCalculator(keypoints=left_points)
        uc = UpCalculator(keypoints=up_points)
        front_points = format_point(fc.get_points())
        left_points = format_point(lc.get_points())
        up_points = format_point(uc.get_points())

        output["point"]["state"] = 1
        output["point"]["data"]["up"] = up_points
        output["point"]["data"]["left"] = left_points
        output["point"]["data"]["front"] = front_points

    except Exception as e:
        return output

    try:
        front_parameters = fc.get_parameters()
        left_parameters = lc.get_parameters()
        up_parameters = uc.get_parameters()
        parameters = {**front_parameters, **left_parameters, **up_parameters}

        output["parameter"]["state"] = 1
        output["parameter"]["data"] = parameters
    except Exception as e:
        return output

    # 旋转mask与图像
    try:
        frame_mask = fc.get_rotated_image(frame_mask, [0, None, 0, None])
        lens_mask = fc.get_rotated_image(lens_mask, [0, None, 0, None])

        nose_mask_expand = np.zeros_like(frame_mask)
        region_nose = regions["nose"]
        nose_mask_expand[region_nose[0] : region_nose[1], region_nose[2] : region_nose[3]] = nose_mask
        nose_mask_expand = fc.get_rotated_image(nose_mask_expand, [0, None, 0, None])
        nose_mask = nose_mask_expand[region_nose[0] : region_nose[1], region_nose[2] : region_nose[3]]

        front_preprocess_image = fc.get_rotated_image(front_preprocess_image, [0, None, 0, None])

        templeWf_mask = lc.get_rotated_image(templeWf_mask, [0, None, 0, None])
        left_preprocess_image = lc.get_rotated_image(left_preprocess_image, [0, None, 0, None])

        output["mask"]["data"]["frame"] = frame_mask
        output["mask"]["data"]["lens"] = lens_mask
        output["mask"]["data"]["nose"] = nose_mask
        output["mask"]["data"]["templeWf"] = templeWf_mask
    except Exception as e:
        print(e)
        print('旋转失败')

    ## 获取前景及美化
    try:
        types = options.get("types", {})
        front_mask = get_front_mask(
            frame_mask,
            lens_mask,
            frame_type=types["frame"],
        )  # front_mask
        foreground_front = front_preprocess_image.copy()
        foreground_front = cv2.cvtColor(foreground_front, cv2.COLOR_BGR2BGRA)
        foreground_front[front_mask == 0] = [0, 0, 0, 0]
        foreground_left = left_preprocess_image.copy()
        foreground_left = cv2.cvtColor(foreground_left, cv2.COLOR_BGR2BGRA)
        foreground_left[templeWf_mask == 0] = [0, 0, 0, 0]

        # 美化
        beauty_front = ps(
            image={
                "foreground": foreground_front,
                "mask": front_mask,
                "nose": nose_mask,
            },
            types=types,
        )
        beauty_left = ps_temple(
            image={
                "foreground": foreground_left,
                "mask": templeWf_mask,
                "front_foreground": beauty_front,
                "front_mask": front_mask,
            },
            types=types,
        )

        output["mask"]["state"] = 1
        output["image"]["state"] = 1
        output["mask"]["data"]["front"] = front_mask
        output["image"]["data"]["frontview_seg"] = foreground_front
        output["image"]["data"]["sideview_seg"] = foreground_left
        output["image"]["data"]["frontview_beautify"] = beauty_front
        output["image"]["data"]["sideview_beautify"] = beauty_left

    except Exception as e:
        print(traceback.format_exc())
        return output

    # 计算尺寸
    try:
        pc = ParamsConverter(parameters, standard_size=options.get("standard_size", []))
        sizes = pc.convert()
        output["size"]["state"] = 1
        output["size"]["data"] = sizes
    except Exception as e:
        return output

    try:
        dc = DataCalculator(
            frame_image=frame_mask,
            lens_image=lens_mask,
            front_points=front_points,
            is_balance=True,
        )
        shape_params = dc.get_parameters(param=sizes)
        output["shape"]["state"] = 1
        output["shape"]["data"] = shape_params
    except Exception as e:
        return output
    return output


if __name__ == "__main__":
    # from debug2 import convert_and_save_masks

    try:
        images = get_capture_images("test1")
        models = get_models()
        output = process(images, models, default_options)
        print(output)
    except Exception as e:
        print(traceback.format_exc())
    # test_lru_cache()
