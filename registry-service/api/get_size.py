from .configs import measure

params_class = {
    "x": [
        "lens_width_left",
        "lens_width_right",
        "lens_diagonal_left",
        "lens_diagonal_right",
        "bridge_width",
        "frame_width",
        "drop_length",
        "temple_length_left",
        "temple_length_right",
    ],
    "y": [
        "lens_height_left",
        "lens_height_right",
        "pile_height_left",
        "pile_height_right",
        "frame_top_width",
        "frame_height",
        "pile_distance",
        "temporal_width",
    ],
    "angle": [
        "face_angle",
        "sagittal_angle_left",
        "sagittal_angle_right",
        "spread_angle_left",
        "spread_angle_right",
        "vertical_angle",
        "forward_angle",
        "temple_angle",
    ],
    "area": ["lens_area_left", "lens_area_right"],
    "coord": ["frame_rects", "lens_center_points", "lens_top_points", "top_points"],
}

params_belong = {
    "front": [
        "frame_rects",  # 镜圈轮廓对应的边界框坐标（x,y,w,h）
        "lens_width_left",  # 左镜圈宽度
        "lens_width_right",  # 右镜圈宽度
        "lens_height_left",  # 左镜圈高度
        "lens_height_right",  # 右镜圈高度
        "lens_diagonal_left",  # 左镜圈对角线长度
        "lens_diagonal_right",  # 右镜圈对角线长度
        "lens_area_left",  # 左镜圈面积
        "lens_area_right",  # 右镜圈面积
        "bridge_width",  # 鼻梁长度
        "lens_center_points",  # 镜圈中心点坐标
        "lens_top_points",  # 镜圈顶部点坐标
        "frame_height",  # 镜框高度
        "frame_width",  # 镜框宽度
        "pile_height_left",  # 左桩头高度
        "pile_height_right",  # 右桩头高度
        "frame_top_width",  # 镜框上边厚度
        "top_points",  # 镜框左右最高点坐标
    ],
    "up": [
        "face_angle",  # 面弯
        "sagittal_angle_left",  # 左垂内角
        "sagittal_angle_right",  # 右垂内角
        "temple_length_left",  # 左镜腿长度
        "temple_length_right",  # 右镜腿长度
        "temporal_width",  # 颞距
        "spread_angle_left",  # 左镜腿外张角
        "spread_angle_right",  # 右镜腿外张角
        "pile_distance",  # 桩头距离
    ],
    "left": [
        "vertical_angle",  # 垂俯角
        "forward_angle",  # 前倾角
        "temple_angle",  # 镜腿角
        "drop_length",  # 垂长
    ],
}

calibration = measure["calibration"]
ratio = measure["ratio"]


def get_size(parameters: dict, distances: dict):
    # print(distances)
    size = {}
    belong = "front"
    for key in params_belong:
        if list(parameters.keys())[0] in params_belong[key]:
            belong = key
            break
    distance = distances[f"distance_{belong}"]
    scale = {
        "x": calibration[belong]["x"]["slope"] * distance
        + calibration[belong]["x"]["intercept"],
        "y": calibration[belong]["y"]["slope"] * distance
        + calibration[belong]["y"]["intercept"],
    }
    print(f"{belong}:{distance}")

    for key in parameters:
        # 计算尺寸
        if key in params_class["x"]:
            size[key] = round(parameters[key] / scale["x"], 4)
        elif key in params_class["y"]:
            size[key] = round(parameters[key] / scale["y"], 4)
        elif key in params_class["area"]:
            size[key] = round(parameters[key] / (scale["x"] * scale["y"]), 4)
        else:
            size[key] = parameters[key]

        # 特殊比例
        if key in ratio:
            size[key] = round(size[key] * ratio[key], 4)

    return size
