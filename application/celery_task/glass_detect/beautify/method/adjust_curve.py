import os
from typing import List, Optional

import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline, interp1d

from .utils import brightness_adjust


def show(image: np.ndarray):
    temp = image.copy()
    if len(image.shape) == 3 and image.shape[2] == 4:
        temp = temp[:, :, :3]
    elif len(image.shape) == 2:
        temp = temp * 255 if np.max(temp) <= 1 else temp
    temp = temp.astype(np.uint8)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", temp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_adaptive_curve_points(image: np.ndarray):
    assert len(image.shape) == 3, "image must be in H,W,C"
    if image.shape[2] == 4:
        mask = image[:, :, 3]
        image_new = image[:, :, :3]
        image_new[mask == 0] = [0, 0, 0]
    else:
        mask = None
        image_new = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 灰度分布（去掉0）
    hist = cv2.calcHist([gray], [0], None, [256], [1, 256])
    # 根据最高值归一化到255
    max_height = min(30000, max(hist))
    # print(max_height)
    hist = np.clip(hist, 0, max_height)
    y = (hist / max_height * 255).reshape(256)
    # 根据顶点分为左右两部分
    peek = np.argmax(hist)
    # print(peek)
    left, right = y[:peek], y[peek:]
    # print(left.shape, right.shape)
    # 插值
    x_left = np.linspace(0, peek - 1, peek)
    x_right = np.linspace(peek, 255, 256 - peek)
    f_left, f_right = interp1d(left, x_left), interp1d(right, x_right)

    # 求出 左1/4点和右3/4点
    point_left, point_right = [(f_left(63)), 63], [int(f_right(191)), 191]

    return point_left, point_right


def get_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 画出灰度直方图
    plt.hist(gray.ravel(), 255, [1, 256])
    plt.show()


def adjust_curve(image, curve_points: Optional[List[List[int]]] = None, mode="none"):
    assert len(image.shape) == 3, "image must be in H,W,C"

    if curve_points is not None:
        curve_points = np.array(curve_points)
    else:
        if mode == "none":
            curve_points = np.array([[0, 0], [100, 80], [255, 255]])
        elif mode == "metal":
            curve_points = np.array([[0, 0], [100, 36], [255, 255]])
        elif mode == "transparent":
            curve_points = np.array(
                [[0, 0], *get_adaptive_curve_points(image), [255, 255]]
            )
    # 曲线
    x_points = curve_points[:, 0]
    y_points = curve_points[:, 1]
    cs = CubicSpline(x_points, y_points)
    x_new = np.linspace(0, 255, 2550)
    y_new = cs(x_new)
    curve = np.clip(y_new, 0, 255)

    mask = image[:, :, 3] if image.shape[2] == 4 else None
    # 分离RGB通道
    r_channel = image[:, :, 2]
    g_channel = image[:, :, 1]
    b_channel = image[:, :, 0]

    r_channel = np.interp(r_channel, x_new, curve)
    g_channel = np.interp(g_channel, x_new, curve)
    b_channel = np.interp(b_channel, x_new, curve)

    adjusted_image = np.stack((b_channel, g_channel, r_channel), axis=-1).astype(
        np.uint8
    )
    if mask is not None:
        adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2BGRA)
        adjusted_image[:, :, 3] = mask
    return adjusted_image


def main():
    # 示例用法
    # 加载图像
    sku = "201300673000230409"
    glasses_base_path = "D:/Project/glasses_ps/foreground/"
    mask_base_path = "D:/Project/glasses/standard4973/mask/front/"
    nose_base_path = "D:/Project/glasses/standard4973/mask/nose/"
    image = cv2.imread(
        os.path.join(glasses_base_path, f"{sku}_1.png"), cv2.IMREAD_UNCHANGED
    )
    mask = cv2.imread(
        os.path.join(mask_base_path, f"{sku}_1.png"), cv2.IMREAD_GRAYSCALE
    )
    # curve = [[0, 0], *get_adaptive_curve_points(image), [255, 255]]
    # image_edge = reduce_white_edge(
    #     image, mask, color=(100, 100, 100), width=2, alpha=0.5
    # )
    image_brightness = brightness_adjust(image, 0.9)
    # get_gray(image_brightness)
    image_new = adjust_curve(image_brightness, mode="transparent")
    # print(image_new)
    cv2.imwrite("test_curve.png", image_new)


if __name__ == "__main__":
    main()
