import cv2
import traceback
from functools import lru_cache
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
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    up_image_path = os.path.join(current_dir, "image", "capture",sku+"_0.jpg")
    front_image_path = os.path.join(current_dir, "image", "capture",sku+"_1.jpg")
    left_image_path = os.path.join(current_dir, "image", "capture",sku+"_2.jpg")
    up_image = cv2.imread(f"{up_image_path}")
    front_image = cv2.imread(f"{front_image_path}")
    left_image = cv2.imread(f"{left_image_path}")

    # up_image = cv2.imread(f"./image/capture/{sku}_0.jpg")
    # front_image = cv2.imread(f"./image/capture/{sku}_1.jpg")
    # left_image = cv2.imread(f"./image/capture/{sku}_2.jpg")

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


def process(images: dict, models: dict, options: dict=default_options):
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
    up_preprocess_image = up.preprocess(up_image)
    front_preprocess_image = fp.preprocess(front_image)
    left_preprocess_image = lp.preprocess(left_image)
    nose_preprocess_image = nep.preprocess(front_image)

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

    ## 获取前景和美化
    try:
        types = options["types"]
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

    # 计算尺寸
    try:
        pc = ParamsConverter(parameters)
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
    images = get_capture_images("201300053024730500")
    models = get_models()
    output = process(images, models, default_options)
    print(output)
