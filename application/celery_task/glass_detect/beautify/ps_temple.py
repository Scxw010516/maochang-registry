import numpy as np


from .method.add_base_color import add_base_color
from .method.add_shadow import add_shadow
from .method.adjust_curve import adjust_curve

from .method.reduce_white_edge import reduce_white_edge
from .method.utils import brightness_adjust


def process_normal(image, mask):
    # 去除镜片白边 -> 自适应调整亮度 -> 调整曲线 -> 增加投影
    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_brightness = brightness_adjust(image_edge, 0.9)
    image_curve = adjust_curve(image_brightness, mode="none")
    image_shadow = add_shadow(image_curve, alpha=1.5)
    image_ps = image_shadow
    return image_ps


def process_metal(image, mask):
    # 去除镜片白边 -> 自适应调整亮度 -> 调整曲线 -> 增加投影
    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_brightness = brightness_adjust(image_edge, 0.9)
    image_curve = adjust_curve(image_brightness, mode="none")
    image_shadow = add_shadow(image_curve, mask, alpha=1.5)
    image_ps = image_curve
    return image_ps


def process_transparent_color(image, mask):
    # 自适应调整亮度 -> 自适应调整曲线 -> 去除镜片白边 -> 增加投影 -> 增加底色

    image_brightness = brightness_adjust(image, 0.9)
    image_curve = adjust_curve(image_brightness, mode="transparent")
    image_edge = reduce_white_edge(
        image_curve, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, mask, alpha=1)
    image_color = add_base_color(image, mask, image_base=image_shadow, alpha=0.5)
    return image_color


def process_transparent(image, mask):
    # 自适应调整亮度 -> 自适应调整曲线 -> 自适应调整亮度 -> 去除镜片白边 -> 增加投影

    image_brightness = brightness_adjust(image, 0.9)
    image_curve = adjust_curve(image_brightness, mode="transparent")
    image_brightness2 = brightness_adjust(image_curve, 0.6)
    image_edge = reduce_white_edge(
        image_brightness2, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, mask, alpha=1)
    image_ps = image_shadow
    return image_ps


def process_half_none(image, mask):
    # 去除镜片白边 -> 自适应调整亮度 -> 调整曲线 -> 增加投影

    image_edge = reduce_white_edge(image, mask)
    image_brightness = brightness_adjust(image_edge, 0.9)
    image_curve = adjust_curve(image_brightness, mode="none")
    image_shadow = add_shadow(image_curve, mask, alpha=0.5)
    image_ps = image_shadow
    return image_ps


def process_half_none_metal(image, mask):
    # 去除镜片白边 -> 自适应调整亮度 -> 调整曲线 -> 增加投影
    image_edge = reduce_white_edge(image, mask)
    image_brightness = brightness_adjust(image_edge, 0.9)
    image_curve = adjust_curve(image_brightness, mode="none")
    image_shadow = add_shadow(image_curve, mask, alpha=0.5)
    image_ps = image_shadow
    return image_ps


def process_normal_special(image, mask):

    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, alpha=1.5)

    image_ps = image_shadow
    return image_ps


def process_metal_special(image, mask):
    # 去除镜片白边 -> 增加投影
    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, mask, alpha=1.5)
    image_ps = image_shadow
    return image_ps


def process_transparent_color_special(image, mask):
    # 去除镜片白边 -> 增加投影 -> 增加底色

    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, mask, alpha=1)
    image_color = add_base_color(image, mask, image_base=image_shadow, alpha=0.5)
    image_ps = image_color
    return image_ps


def process_transparent_special(image, mask):
    # 去除镜片白边 -> 增加投影

    image_edge = reduce_white_edge(
        image, mask, color=(100, 100, 100), width=2, alpha=0.5
    )
    image_shadow = add_shadow(image_edge, mask, alpha=1)

    image_ps = image_shadow
    return image_ps


def process_half_none_special(image, mask):
    # 去除镜片白边 -> 增加投影

    image_edge = reduce_white_edge(image, mask)
    image_shadow = add_shadow(image_edge, mask, alpha=0.5)
    image_ps = image_shadow
    return image_ps


def process_half_none_metal_special(image, mask):
    # 去除镜片白边 -> 增加投影
    image_edge = reduce_white_edge(image, mask)
    image_shadow = add_shadow(image_edge, mask, alpha=0.5)
    image_ps = image_shadow
    return image_ps


def get_processor(t, special=False):
    # 根据眼镜框类型选择对应的处理方法
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


def ps_temple(image: dict, types: dict) -> np.ndarray:
    foreground = image["foreground"]
    mask = image["mask"]

    is_special = types["special"]

    processor = get_processor(types, special=is_special)
    image_ps = processor(foreground, mask)
    return image_ps
