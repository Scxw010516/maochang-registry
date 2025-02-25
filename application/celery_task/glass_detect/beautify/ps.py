import numpy as np


from .method.add_base_color import add_base_color
from .method.add_lens import add_lens
from .method.add_shadow import add_shadow
from .method.adjust_curve import adjust_curve
from .method.enhance_depth import enhance_depth
from .method.nose_transparent import nose_transparent
from .method.reduce_white_edge import reduce_white_edge
from .method.utils import brightness_adjust


def process_normal(image, mask, nose):
    # 去除镜片白边 -> 自适应调整亮度 -> 调整曲线 -> 增加投影 -> 添加镜片 -> 增加立体感 -> 透明鼻托
    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_brightness = brightness_adjust(image_edge, 0.9)
    image_curve = adjust_curve(image_brightness, mode="none")
    image_shadow = add_shadow(image_curve, alpha=1.5)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)
    image_depth = enhance_depth(image_lens, mask)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_metal(image, mask, nose):
    # 去除镜片白边 -> 自适应调整亮度 -> 调整曲线 -> 增加投影 -> 添加镜片 -> 增加立体感 -> 透明鼻托
    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_brightness = brightness_adjust(image_edge, 0.9)
    image_curve = adjust_curve(image_brightness, mode="none")
    image_shadow = add_shadow(image_curve, mask, alpha=1.5)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)
    image_depth = enhance_depth(image_lens, mask)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_transparent_color(image, mask, nose):
    # 自适应调整亮度 -> 自适应调整曲线 -> 去除镜片白边 -> 增加投影 -> 添加镜片 -> 增加底色 -> 增加立体感 -> 透明鼻托

    image_brightness = brightness_adjust(image, 0.9)
    image_curve = adjust_curve(image_brightness, mode="transparent")
    image_edge = reduce_white_edge(
        image_curve, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, mask, alpha=1)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)
    image_color = add_base_color(image, mask, image_base=image_lens, alpha=0.5)
    image_depth = enhance_depth(image_color, mask)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_transparent(image, mask, nose):
    # 自适应调整亮度 -> 自适应调整曲线 -> 自适应调整亮度 -> 去除镜片白边 -> 增加投影 -> 添加镜片 -> 增加立体感 -> 透明鼻托

    image_brightness = brightness_adjust(image, 0.9)
    image_curve = adjust_curve(image_brightness, mode="transparent")
    image_brightness2 = brightness_adjust(image_curve, 0.6)
    image_edge = reduce_white_edge(
        image_brightness2, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, mask, alpha=1)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)

    image_depth = enhance_depth(image_lens, mask)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_half_none(image, mask, nose):
    # 去除镜片白边 -> 自适应调整亮度 -> 调整曲线 -> 增加投影 -> 添加镜片 -> 增加立体感 -> 透明鼻托

    image_edge = reduce_white_edge(image, mask)
    image_brightness = brightness_adjust(image_edge, 0.9)
    image_curve = adjust_curve(image_brightness, mode="none")
    image_shadow = add_shadow(image_curve, mask, alpha=0.5)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)
    image_depth = enhance_depth(image_lens, mask, frame_opacity=0)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_half_none_metal(image, mask, nose):
    # 去除镜片白边 -> 自适应调整亮度 -> 调整曲线  -> 增加投影 -> 添加镜片 -> 增加立体感 -> 透明鼻托
    image_edge = reduce_white_edge(image, mask)
    image_brightness = brightness_adjust(image_edge, 0.9)
    image_curve = adjust_curve(image_brightness, mode="none")
    image_shadow = add_shadow(image_curve, mask, alpha=0.5)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)
    image_depth = enhance_depth(image_lens, mask, frame_opacity=0)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_normal_special(image, mask, nose):
    # 去除镜片白边 -> 增加投影 -> 添加镜片 -> 增加立体感 -> 透明鼻托
    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, alpha=1.5)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)
    image_depth = enhance_depth(image_lens, mask)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_metal_special(image, mask, nose):
    # 去除镜片白边 -> 增加投影 -> 添加镜片 -> 增加立体感 -> 透明鼻托
    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, mask, alpha=1.5)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)
    image_depth = enhance_depth(image_lens, mask)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_transparent_color_special(image, mask, nose):
    # 去除镜片白边 -> 增加投影 -> 添加镜片 -> 增加底色 -> 增加立体感 -> 透明鼻托

    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, mask, alpha=1)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)
    image_color = add_base_color(image, mask, image_base=image_lens, alpha=0.5)
    image_depth = enhance_depth(image_color, mask)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_transparent_special(image, mask, nose):
    # 去除镜片白边 -> 增加投影 -> 添加镜片 -> 增加立体感 -> 透明鼻托

    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, mask, alpha=1)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)

    image_depth = enhance_depth(image_lens, mask)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_half_none_special(image, mask, nose):
    # 去除镜片白边 -> 增加投影 -> 添加镜片 -> 增加立体感 -> 透明鼻托

    image_edge = reduce_white_edge(image, mask)
    image_shadow = add_shadow(image_edge, mask, alpha=0.5)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)
    image_depth = enhance_depth(image_lens, mask, frame_opacity=0)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def process_half_none_metal_special(image, mask, nose):
    # 去除镜片白边 -> 增加投影 -> 添加镜片 -> 增加立体感 -> 透明鼻托
    image_edge = reduce_white_edge(image, mask)
    image_shadow = add_shadow(image_edge, mask, alpha=0.5)
    image_lens = add_lens(image_shadow, mask, alpha=2, ratio=0.2)
    image_depth = enhance_depth(image_lens, mask, frame_opacity=0)
    image_nose = nose_transparent(image_depth, nose)
    image_ps = image_nose
    return image_ps


def get_processor(t, special=False):
    frame_type, material_type, transparent_type = (
        t["frame"],
        t["material"],
        t["transparent"],
    )

    if special:
        if transparent_type == 2:  # 半透明
            processor = process_transparent_color_special
        elif transparent_type == 1:  # 全透明
            processor = process_transparent_special
        else:
            if frame_type != 0:
                if material_type in [2, 4, 6]:  # 金属
                    processor = process_half_none_metal_special
                else:
                    processor = process_half_none_special
            elif material_type in [2, 4, 6]:
                processor = process_metal_special
            else:
                processor = process_normal_special
        return processor

    if transparent_type == 2:  # 半透明
        processor = process_transparent_color
    elif transparent_type == 1:  # 全透明
        processor = process_transparent
    else:
        if frame_type != 0:
            if material_type in [2, 4, 6]:  # 金属
                processor = process_half_none_metal
            else:
                processor = process_half_none
        elif material_type in [2, 4, 6]:
            processor = process_metal
        else:
            processor = process_normal
    return processor


def ps(image: dict, types: dict) -> np.ndarray:
    foreground = image["foreground"]
    mask = image["mask"]
    nose = image["nose"]

    is_special = types["special"]
    processor = get_processor(types, special=is_special)
    image_ps = processor(foreground, mask, nose)
    return image_ps
