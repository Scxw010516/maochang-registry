import numpy as np

default_options = {
    "types": {
        "frame": 0,  # 对应EyeglassFrameEntry表的frame_type
        "material": 2,  # 对应EyeglassFrameEntry表的material
        "transparent": 0,  # 对应EyeglassFrameEntry表的is_transparent
        "special": False,  # 默认为False
    },
    # List[float]类型，对应EyeglassFrameEntry表的lens_width_st、bridge_width_st、temple_length_st。严格按顺序
    "standard_size": [53, 16, 145],
}

default_front_points = {
    "frame_bounding_points": [[-1, -1], [-1, -1]],
    "pile_points": [[-1, -1], [-1, -1]],
    "lens_center_points": [[-1, -1], [-1, -1]],
    "lens_bounding_points": [[[-1, -1], [-1, -1]], [[-1, -1], [-1, -1]]],
    "lens_diagonal_points": [[[-1, -1], [-1, -1]], [[-1, -1], [-1, -1]]],
    "lens_top_points": [[-1, -1], [-1, -1]],
    "top_points": [[-1, -1], [-1, -1]],
    "bottom_points": [[-1, -1], [-1, -1]],
    "lens_bottom_points": [[-1, -1], [-1, -1]],
    "lens_side_points": [[[-1, -1], [-1, -1]], [[-1, -1], [-1, -1]]],
}
default_left_points = {
    "head_point": [-1, -1],
    "down_point": [-1, -1],
    "turning_point": [-1, -1],
    "tail_point": [-1, -1],
}
default_up_points = {
    "pile_points": [[-1, -1], [-1, -1]],
    "temporal_points": [[-1, -1], [-1, -1]],
    "turning_points": [[-1, -1], [-1, -1]],
    "tail_points": [[-1, -1], [-1, -1]],
    "bridge_point": [-1, -1],
}
default_parameters = {
    "lens_width_left": -1,
    "lens_width_right": -1,
    "bridge_width": -1,
    "pile_height_left": -1,
    "pile_height_right": -1,
    "frame_height": -1,
    "frame_width": -1,
    "lens_height_left": -1,
    "lens_height_right": -1,
    "lens_diagonal_left": -1,
    "lens_diagonal_right": -1,
    "lens_area_left": -1,
    "lens_area_right": -1,
    "frame_top_width": -1,
    "vertical_angle": -1,
    "forward_angle": -1,
    "temple_angle": -1,
    "drop_length": -1,
    "face_angle": -1,
    "sagittal_angle_left": -1,
    "sagittal_angle_right": -1,
    "temple_length_left": -1,
    "temple_length_right": -1,
    "temporal_width": -1,
    "spread_angle_left": -1,
    "spread_angle_right": -1,
    "pile_distance": -1,
}
default_sizes = {
    "lens_width_left": -1,
    "lens_width_right": -1,
    "bridge_width": -1,
    "pile_height_left": -1,
    "pile_height_right": -1,
    "frame_height": -1,
    "frame_width": -1,
    "lens_height_left": -1,
    "lens_height_right": -1,
    "lens_diagonal_left": -1,
    "lens_diagonal_right": -1,
    "lens_area_left": -1,
    "lens_area_right": -1,
    "frame_top_width": -1,
    "vertical_angle": -1,
    "forward_angle": -1,
    "temple_angle": -1,
    "drop_length": -1,
    "face_angle": -1,
    "sagittal_angle_left": -1,
    "sagittal_angle_right": -1,
    "temple_length_left": -1,
    "temple_length_right": -1,
    "temporal_width": -1,
    "spread_angle_left": -1,
    "spread_angle_right": -1,
    "pile_distance": -1,
}


default_output = {
    "mask": {
        "state": 0,
        "data": {
            "frame": None,
            "lens": None,
            "templeWf": None,
            "nose": None,
            "front": None,
        },
    },
    "image": {
        "state": 0,
        "data": {
            "frontview_seg": None,
            "sideview_seg": None,
            "frontview_beautify": None,
            "sideview_beautify": None,
        },
    },
    "point": {
        "state": 0,
        "data": {
            "front": default_front_points,
            "up": default_up_points,
            "left": default_left_points,
        },
    },
    "parameter": {"state": 0, "data": default_parameters},
    "size": {"state": 0, "data": default_sizes},
    "shape": {
        "state": 0,
        "data": {
            "frame_size": 0,
            "left_curvature": -1,
            "right_curvature": -1,
            "left_factors": -1,
            "right_factors": -1,
            "height_width_proportion": -1,
        },
    },
}
