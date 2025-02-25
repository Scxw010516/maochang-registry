import math

import cv2
import numpy as np
from matplotlib import pyplot as plt
from typing import Sequence, Union, Tuple, Optional, List

IMAGE = np.ndarray


#####
# 功能
#####


def default_dump(obj):
    """Convert numpy classes to JSON serializable objects."""
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def get_contour_center(contour: np.ndarray) -> tuple:
    """
    获取轮廓的中心点坐标

    params:
        -contour (ndarray): 输入的轮廓数组

    return:
        -center: tuple - 轮廓的中心点坐标
    """

    moments = cv2.moments(contour)

    # 检查m00是否为零以避免除以零错误
    if moments["m00"] != 0:
        # 计算中心点坐标
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])

        return cx, cy
    else:
        center = np.mean(contour, axis=0).reshape(
            2,
        )
        center = center.astype(np.int32)
        return center


def get_angle(
    point1: Union[tuple, list, np.ndarray], point2: Union[tuple, list, np.ndarray]
) -> float:
    if point2[0] == point1[0]:
        return np.pi / 2
    return np.arctan((point2[1] - point1[1]) / (point2[0] - point1[0]))



def rotate_image(image: IMAGE, angle: float, point: Sequence[int]) -> IMAGE:
    """

    图片按照给定点旋转给定角度
    """
    rotation_matrix = cv2.getRotationMatrix2D(
        (int(point[0]), int(point[1])), angle * 180 / np.pi, 1
    )
    shape = image.shape[:2]
    image = cv2.warpAffine(image, rotation_matrix, shape[::-1])

    return image


def cal_frame_size(frame_width: int) -> str:
    if frame_width >= 128:
        return 0 # 大框
    elif frame_width >= 111:
        return 1 # 中框
    else:
        return 2 # 小框

def cal_curvature(points) -> float:
    """计算平均曲率"""
    dxdt = np.gradient(points[:, 0])
    dydt = np.gradient(points[:, 1])
    r_prime = np.array([dxdt, dydt]).T

    d2xdt2 = np.gradient(np.gradient(points[:, 0]))
    d2ydt2 = np.gradient(np.gradient(points[:, 1]))
    r_double_prime = np.array([d2xdt2, d2ydt2]).T

    # 计算叉积
    cross_product = np.cross(r_prime, r_double_prime)

    norm_cross = np.linalg.norm(cross_product)
    norm_prime = np.linalg.norm(r_prime, axis=1)

    valid_mask = norm_prime != 0
    valid_indices = np.where(valid_mask)[0]
    valid_norm_prime = norm_prime[valid_indices]

    if valid_norm_prime.size > 0:
        curvature = np.mean(norm_cross / (valid_norm_prime ** 3))
    else:
        curvature = 0.0

    return curvature


def cal_shape_factor(contour) -> float:
    """计算形状因子"""
    area = cv2.contourArea(contour)  # 面积
    perimeter = cv2.arcLength(contour, True)  # 周长
    if area == 0:
        return 1.2  # 避免除以零
    shape_factor = (perimeter ** 2) / (4 * np.pi * area)  # 形状因子公式
    return shape_factor