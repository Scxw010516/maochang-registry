import math

import cv2
import numpy as np
from matplotlib import pyplot as plt
from typing import Sequence, Union, Tuple, Optional, List

IMAGE = np.ndarray


#####
# 显示
#####


def cv_show(title: str, img: IMAGE) -> None:
    """
    使用opencv显示图像。

    parameters：
        title (str): 图像窗口的标题。
        img (numpy.ndarray): 要显示的图像。

    return：
        无
    """
    # 创建一个图像窗口
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    # 显示图像
    cv2.imshow(title, img)
    # 等待用户按下任意键
    cv2.waitKey()
    # 销毁所有窗口
    cv2.destroyAllWindows()


def show(
    img: Union[IMAGE, Sequence[IMAGE]],
    title: Union[str, Sequence] = None,
    size: Optional[Tuple] = None,
    save_path: Optional[str] = None,
):
    """
    使用matplotlib显示图像。

    parameters：
        img (numpy.ndarray): 要显示的图像。可以是2D或3D数组。
        title (str, 可选): 图像的标题。默认为空字符串。
        size (tuple, 可选): 图像的大小，以英寸为单位。默认为None。
        path (str, 可选): 保存图像的路径。默认为None。

    return：
        无
    """
    if isinstance(img, (list, tuple)):
        show_more(img, title)
        return

    # 如果指定了图片大小，则设置图片大小
    if size:
        plt.figure(figsize=size)
    # 如果指定了标题，则设置图片标题
    if title:
        plt.title(title, y=-0.5)

    # 如果图片是3维的，则显示彩色图片
    if len(img.shape) == 3:
        plt.imshow(img[:, :, ::-1])
    # 如果图片是2维的，则显示灰度图片
    elif len(img.shape) == 2:
        plt.imshow(img, cmap="gray")
    # 如果指定了保存路径，则保存图片
    if save_path:
        plt.savefig(save_path)
    # 关闭坐标轴
    plt.axis("off")
    # 显示图片
    plt.show()


def show_more(images: Sequence[IMAGE], titles: Optional[Sequence] = None) -> None:
    """
    使用matplotlib显示多个图像。

    parameters：
        images (numpy.ndarray): 要显示的图像。可以是2D或3D数组。
        titles (str, 可选): 图像的标题。默认为空字符串。

    return：
        无
    """
    if titles is None:
        titles = []
    num_col = 3
    num_row = math.ceil(len(images) / num_col)

    plt.figure(figsize=(num_col * 5, num_row * 3))

    for i in range(len(images)):
        plt.subplot(num_row, num_col, i + 1)
        # 如果图片是3维的，则显示彩色图片
        if len(images[i].shape) == 3:
            plt.imshow(images[i][:, :, ::-1])
        # 如果图片是2维的，则显示灰度图片
        elif len(images[i].shape) == 2:
            plt.imshow(images[i], cmap="gray")
        # 如果指定了标题，则设置图片标题
        if len(titles) > i:
            plt.title(titles[i], y=-0.5)
        plt.axis("off")

    # 显示图片
    plt.show()


def show_point(image: IMAGE, points, radius=20, color=(0, 0, 255), if_show=True):
    if len(image.shape) == 2:
        res = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        res = image.copy()
    try:
        for point in points:
            cv2.circle(res, point, radius=radius, color=color, thickness=-1)
    except cv2.error:
        cv2.circle(res, points, radius=radius, color=color, thickness=-1)
    if if_show:
        show(res)
    return res


def show_rect(image: IMAGE, points, line_width=5, color=(0, 0, 255)):
    try:
        res = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    except cv2.error:
        res = image
    cv2.rectangle(res, points[0], points[1], color, line_width)
    show(res)


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


def get_first_no_zero(data: np.ndarray, axis: int = 0) -> int:
    """
    获取data中第一个不为0的元素。

    params：
        data (numpy.ndarray): 输入的数组。
        axis (int): 指定轴，默认为0。

    return：
        int: 第一个不为0的元素。
    """
    index = get_first_no_zero_index(data, axis)
    if len(index) == 1:
        return data[index]
    else:
        return data[index[0], index[1]]


def get_first_no_zero_index(data: np.ndarray, axis: int = 0) -> Union[int, List, None]:
    """
    获取data中第一个不为0的元素的索引。

    params：
        data (numpy.ndarray): 输入的二维维数组。
        axis (int): 指定轴，默认为0。

    return：
        int: 第一个不为0的元素的索引。
    """
    nonzero = np.array(np.nonzero(data))
    if nonzero.size == 0:
        return None
    order = np.lexsort((nonzero[axis, :],))
    nonzero = nonzero[:, order]
    if nonzero.shape[0] == 1:
        return nonzero[0, 0]
    else:
        # xy
        return [nonzero[1, 0], nonzero[0, 0]]


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


def get_intersection_angle(pointA, pointB, pointC):
    # 计算∠ABC
    A = np.array(pointA)
    B = np.array(pointB)
    C = np.array(pointC)

    # 向量BA和BC
    BA = A - B
    BC = C - B

    # 点积
    dot_product = np.dot(BA, BC)

    # 模长
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)

    # 夹角的余弦值
    cos_theta = dot_product / (norm_BA * norm_BC)

    # 弧度转角度
    angle = np.arccos(cos_theta)

    return angle


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


# def rotate_point(point1, point2, angle) -> List[int]:
#     x1, y1 = point1
#     x2, y2 = point2
#     cos = np.cos
#     sin = np.sin
#     x = int((x1 - x2) * cos(angle) - (y1 - y2) * sin(angle) + x2)
#     y = int((x1 - x2) * sin(angle) + (y1 - y2) * cos(angle) + y2)
#
#     return [x, y]


def rotate_point(point1, point2, angle):
    """
    计算点A绕点B旋转 theta 弧度后的新坐标。

    :param point1: 点A的xy坐标
    :param point2: 点B的xy坐标
    :param y1: 点A的y坐标
    :param x2: 点B的x坐标
    :param y2: 点B的y坐标
    :param angle: 旋转的角度（弧度）
    :return: 旋转后点A的新坐标 (new_x, new_y)
    """
    x1, y1 = point1
    x2, y2 = point2
    # 将点A移动到原点附近
    x_shift = x1 - x2
    y_shift = y1 - y2

    # 旋转
    new_x = int(x_shift * math.cos(angle) - y_shift * math.sin(angle))
    new_y = int(x_shift * math.sin(angle) + y_shift * math.cos(angle))

    # 移回点B附近
    new_x += x2
    new_y += y2

    return new_x, new_y


def add(array1: Sequence, array2: Sequence) -> List:
    """
    将两个数组对应元素相加
    """
    return [a + b for a, b in zip(array1, array2)]


def euclidean_distance(point1, point2) -> float:
    # 使用 numpy.linalg.norm 计算欧氏距离
    return np.linalg.norm(np.array(point1) - point2)
