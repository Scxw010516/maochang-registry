import os
import json

import numpy as np
from tqdm import tqdm
import cv2

from calculate.front_calculator import FrontCalculator
from calculate.left_calculator import LeftCalculator
from calculate.up_calculator import UpCalculator
from calculate_shape.cal_data import DataCalculator
from config import default_output
from detect.left_detector import LeftDetector
from detect.up_detector import UpDetector
from utils.format_point import format_point
from convert.params_converter import ParamsConverter


def get_capture_images(paths: dict, sku=""):
    path_up = paths["up"]
    path_front = paths["front"]
    path_left = paths["left"]
    up_image = cv2.imread(os.path.join(path_up, f"{sku}_0.jpg"))
    front_image = cv2.imread(os.path.join(path_front, f"{sku}_1.png"))
    left_image = cv2.imread(os.path.join(path_left, f"{sku}_2.png"))

    return {"up": up_image, "front": front_image, "left": left_image}


def get_masks(paths: dict, sku=""):
    path_frame = paths["frame"]
    path_lens = paths["lens"]
    frame_mask = cv2.imread(
        os.path.join(path_frame, f"{sku}_1.png"), cv2.IMREAD_GRAYSCALE
    )
    lens_mask = cv2.imread(
        os.path.join(path_lens, f"{sku}_1.png"), cv2.IMREAD_GRAYSCALE
    )

    return {"frame": frame_mask, "lens": lens_mask}


def get_models():
    # detect
    ud = UpDetector(device="cuda")
    ld = LeftDetector(device="cuda")

    return {
        "det_up": ud,
        "det_left": ld,
    }


def process(images: dict, masks: dict, models: dict):
    output = default_output
    up_image, left_image = images["up"], images["left"]

    ud, ld = (
        models["det_up"],
        models["det_left"],
    )

    # preprocess
    # up, lp = (UpPreprocessor(), LeftPreprocessor())
    up_preprocess_image = up_image
    left_preprocess_image = left_image

    frame_mask = masks["frame"]
    lens_mask = masks["lens"]

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


def get_files(path, ext=None):
    if isinstance(ext, str):
        ext = (ext,)
    files = []

    for root, dirs, fs in os.walk(path):
        for filename in fs:
            files.append(os.path.join(root, filename))
    if ext is not None:
        files = [f for f in files if os.path.splitext(f)[1] in ext]
    return files


def get_sku(file_path):
    # 返回sku
    sku = os.path.basename(file_path).split("_")[0]
    return sku


def default_dump(obj):
    """Convert numpy classes to JSON serializable objects."""
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


if __name__ == "__main__":
    image_paths = {
        "up": r"D:\Project\glasses\standard4973\image\up",
        "front": r"D:\Project\glasses\standard4973\image\front",
        "left": r"D:\Project\glasses\standard4973\image\left",
    }
    mask_paths = {
        "frame": r"D:\Project\glasses\standard4973\mask\frame",
        "lens": r"D:\Project\glasses\standard4973\mask\lens",
    }

    skus = [get_sku(f) for f in get_files(image_paths["up"], ext=".jpg")]
    loop = tqdm(skus)
    outputs = {}
    for sku in loop:
        loop.set_description(f"Processing {sku}")
        try:
            images = get_capture_images(image_paths, sku)
            masks = get_masks(mask_paths, sku)
            models = get_models()
            output = process(images, masks, models)
            outputs[sku] = output
        except Exception as e:
            print(e)
    with open("output.json", "w") as f:
        json.dump(outputs, f, indent=4, default=default_dump)
