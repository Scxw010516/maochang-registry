import math
from typing import *

import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import medfilt

# types
IMAGE = np.ndarray
CONTOUR = np.ndarray
CONTOURS = Sequence[Union[cv2.Mat, np.ndarray]]

# colors
RED = [0, 0, 255]
GREEN = [0, 255, 0]
BLUE = [255, 0, 0]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
TRANSPARENT = [0, 0, 0, 0]


def load(image_path: str, mode: Optional[int] = 0) -> IMAGE:
    """
    加载图像。

    params：
        img_path (str): 图像的路径。

    return：
        img (numpy.ndarray): 加载的图像。
    """
    # 读取图像
    if mode:
        img = cv2.imread(image_path, mode)
    else:
        img = cv2.imread(image_path)
    # img = cv2.imread(image_path)
    # if mode:
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img


def circle(image, points, radius=20, color=(0, 0, 255)):
    try:
        res = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    except:
        res = image
    try:
        for point in points:
            cv2.circle(res, point, 20, (0, 0, 255), -1)
    except:
        cv2.circle(res, points, 20, (0, 0, 255), -1)

    show(res)


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


def remove_reflect(
    image: IMAGE, threshold: int = 250, alpha: float = 1, beta: float = 0.1
) -> IMAGE:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # kernel = np.ones(kernel_size, np.uint8)
    temp = gray.copy()
    temp[temp < threshold] = 0
    temp[temp >= threshold] = 255
    # cv2.dilate(temp, kernel, iterations=2)
    contours, hierarchy = cv2.findContours(temp, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    mask = np.zeros(temp.shape, np.uint8)
    for contour in contours:
        rect = cv2.boundingRect(contour)
        cv2.rectangle(mask, rect, 255, -1)
    # cv2.fillPoly(blank,contours,255)
    dst = cv2.illuminationChange(image, mask, alpha, beta)

    return dst


def get_contour_center(contour) -> tuple:
    """
    获取轮廓的中心点坐标

    params:
        -contour (ndarray): 输入的轮廓数组

    return:
        -center: tuple - 轮廓的中心点坐标
    """
    center = np.mean(contour, axis=0).reshape(
        2,
    )
    center = center.astype(np.int32)
    return center


def xy2yx(points: np.ndarray) -> np.ndarray:
    """
    将输入的点集的 x 坐标和 y 坐标交换。

    parameters：
        points (numpy.ndarray): 一个二维数组，表示点的坐标。每一行包含两个元素，分别表示 x 坐标和 y 坐标。

    return：
        numpy.ndarray: 一个二维数组，表示交换后的点集。每一行包含两个元素，分别表示交换后的 y 坐标和 x 坐标。
    """
    # 复制输入的点集，以免修改原始数据
    temp = points.copy()
    # 将点的 x 坐标和 y 坐标交换
    points[:, 0] = temp[:, 1]
    points[:, 1] = temp[:, 0]
    # 返回交换后的点集
    return points


def yx2xy(points: np.ndarray) -> np.ndarray:
    return xy2yx(points)


def remove_small(image: IMAGE, threshold: float = 1000) -> IMAGE:
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    small_contours = [
        contour for contour in contours if cv2.contourArea(contour) < threshold
    ]
    clean = cv2.fillPoly(image, small_contours, 0)

    return clean


def fill_small(image: IMAGE, threshold: float = 10000) -> IMAGE:
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    small2_contours = [
        contour for contour in contours if cv2.contourArea(contour) < threshold
    ]
    filled = cv2.fillPoly(image, small2_contours, 255)

    return filled


def gaussian_blur(image: IMAGE, num_gaussian: int = 3) -> IMAGE:
    blur = image.copy()

    for _ in range(num_gaussian):
        blur = cv2.GaussianBlur(blur, (3, 3), 0)

    return blur


def reduce_contours(
    contours: CONTOURS, area_ratio: Sequence[float], ratio: float
) -> CONTOURS:
    """
    根据给定的面积比例和高宽比例值筛选出满足条件的连续两个轮廓，并返回筛选后的轮廓列表。
    params:
        -contours: CONTOURS - 轮廓列表
        -area_ratio: Sequence[float] - 面积比例
        -ratio: float - 高宽比例

    return:
        -contours: CONTOURS - 符合条件的连续两个轮廓
    """
    # 遍历面积比例列表
    for i in range(len(area_ratio)):
        # 符合面积比例
        if area_ratio[i] < ratio**2:
            # 获取两个轮廓的边界矩形
            bounding_rects = [
                cv2.boundingRect(contour) for contour in contours[i : i + 2]
            ]
            # 高宽比
            width_ratio = bounding_rects[0][2] / bounding_rects[1][2]
            height_ratio = bounding_rects[0][3] / bounding_rects[1][3]

            # 依据高宽比找到镜片的轮廓
            if 1 / ratio < width_ratio < ratio and 1 / ratio < height_ratio < ratio:
                contours = contours[i : i + 2]
                break

    return contours


def contour_morphology(
    contour: CONTOUR,
    shape: tuple,
    mode: int = 1,
    iteration: int = 1,
    kernel_size: tuple = (3, 3),
) -> CONTOUR:
    """
    对轮廓进行形态学操作

    params：
        -contour: CONTOUR - 输入的轮廓
        -shape: tuple - 输出图像的形状
        -mode: int - 形态学操作的模式，默认为1，表示膨胀操作
        -iteration: int - 迭代次数，默认为1
        -kernel_size: tuple - 卷积核的大小，默认为(3, 3)

    return：
        -contours[0] - 形态学操作后的轮廓
    """
    blank = np.zeros(shape, np.uint8)  # 创建一个全零的图像
    kernel = np.ones(kernel_size, np.uint8)  # 3*3的卷积核
    cv2.fillPoly(blank, [contour], 255)  # 在空白图像中填充轮廓

    if mode == 1:
        blank = cv2.dilate(blank, kernel, iterations=iteration)  # 进行膨胀操作
    elif mode == 0:
        blank = cv2.erode(blank, kernel, iterations=iteration)  # 进行腐蚀操作
    contours, hierarchy = cv2.findContours(
        blank, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )  # 查找轮廓

    # 返回第一个轮廓
    return contours[0]


def get_contours(image: IMAGE, threshold: float = 50000) -> Tuple[CONTOURS, List]:
    """
    提取并筛选图像中的轮廓

    params：
        -image: IMAGE - 输入的图像数据
        -threshold: float - 面积阈值，默认为50000，用于筛选出面积大于该值的轮廓

    return：
        -contours: CONTOURS - 筛选出的轮廓集合
        -areas: List[float] - 轮廓对应的面积列表，已按面积从大到小排序
    """
    # 使用OpenCV查找图像的轮廓
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # 计算轮廓的面积并排序
    areas = np.array([cv2.contourArea(c) for c in contours])
    areas_index = areas.argsort()[::-1]
    areas = areas[areas_index]
    # 对轮廓根据面积进行排序
    contours = [contours[i] for i in areas_index]

    # 过滤掉面积小于阈值的轮廓
    areas = areas[areas > threshold]
    contours = contours[: len(areas)]

    return contours, areas


def get_lens_incomplete(contours: CONTOURS, areas: List, ratio: float) -> CONTOURS:
    """
    对轮廓按照给定面积比例进行筛选操作
    params：
        - contours: CONTOURS - 输入的一系列轮廓，每个轮廓表示一个可能的目标区域
        - areas: List[float] - 提供的对应轮廓的面积列表，相邻两个元素用于计算面积比例
        - ratio: float - 初始面积比例阈值，用于决定哪些轮廓会被保留下来

    return：
        - contours: CONTOURS - 经过筛选后保留下来的轮廓集合
    """
    area_ratio = [areas[i] / areas[i + 1] for i in range(len(areas) - 1)]

    while True:
        contours = reduce_contours(contours, area_ratio, ratio)
        if ratio > 1.5:
            break
        if len(contours) == 2:
            break
        else:
            ratio += 0.1
    if len(contours) != 2:
        raise ValueError("The lens is incomplete.")
    return contours


def remove_legs(
    contours: CONTOURS, shape: Tuple, num_morphology: int = 100
) -> CONTOURS:
    """
    对输入轮廓进行形态学操作以去除内部缺陷并恢复原始大小

    params：
        - contours: CONTOURS - 输入的一组轮廓数据
        - shape: Tuple - 用于定义形态学操作的结构元素形状或图像尺寸
        - num_morphology: int - 进行形态学迭代操作的次数，默认为100次

    return：
        - lens: CONTOURS - 经过形态学处理后去除内部缺陷的新轮廓列表
    """

    lens = []
    margin = 1000
    for contour in contours:
        blank = np.zeros(shape, np.uint8)
        cv2.fillPoly(blank, [contour], 255)
        # 填充边缘防止膨胀出边界
        blank = cv2.copyMakeBorder(
            blank, margin, margin, margin, margin, cv2.BORDER_CONSTANT
        )
        blank = cv2.dilate(blank, np.ones((3, 3), np.uint8), iterations=num_morphology)
        blank = cv2.erode(blank, np.ones((3, 3), np.uint8), iterations=num_morphology)
        blank = blank[margin:-margin, margin:-margin]
        contour = cv2.findContours(blank, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0][0]
        lens.append(contour)

    return lens


def remove_label(image: IMAGE, contours: CONTOURS, margin_scale=0.1) -> IMAGE:
    temp = []
    # 保留左轮廓右边部分
    left = np.min(contours[0], axis=0)[0][0]
    right = np.max(contours[0], axis=0)[0][0]
    # print(left, right)
    temp.append(
        contours[0][contours[0][:, 0, 0] < right - (right - left) * margin_scale]
    )

    # 保留右边轮廓左边部分
    left = np.min(contours[1], axis=0)[0][0]

    right = np.max(contours[1], axis=0)[0][0]
    temp.append(
        contours[1][contours[1][:, 0, 0] > left + (right - left) * margin_scale]
    )

    cv2.fillPoly(image, temp, 0)

    return image


def calc_num(arr, value, scale):
    arr1 = arr - value * (1 - scale)
    arr1 = arr1 < 0

    low = sum(arr1)

    arr2 = arr - value * (1 + scale)
    arr2 = arr2 > 0
    # print(arr2)
    high = sum(arr2)
    # print(arr1, arr2)

    arr3 = ~arr1 & ~arr2
    median = sum(arr3)
    # high = len(arr1) - sum(arr1)

    return low, median, high


def find_threshold(gray, length: int = 10, scale: float = 1) -> int:
    # hist = plt.hist(gray.ravel(), bins=256)
    hist = cv2.calcHist([gray], [0], None, [256], (0, 256))
    hist = np.reshape(hist, (-1,))
    # x, y = hist[1][:-1], hist[0]

    y = medfilt(hist, 5)
    thresholds = []
    for i in range(length, len(y) - length - 1):
        median = calc_num(y[i - length : i], y[i], scale)[1]

        high = calc_num(y[i + 1 : i + length + 1], y[i], scale)[2]
        # print(median, high)

        if (median > length * 0.7) and (high > length * 0.7):
            thresholds.append(i)

    peak = np.argmax(y)
    if len(thresholds) > 0:
        index = np.argmax(thresholds - peak)
        return int(thresholds[index])
    else:
        return -1


def get_line(x0, y0, x1, y1):
    """
    根据给定的两个点 (x0, y0) 和 (x1, y1),计算直线的参数。

    params：
        x0 (float): 第一个点的 x 坐标
        y0 (float): 第一个点的 y 坐标
        x1 (float): 第二个点的 x 坐标
        y1 (float): 第二个点的 y 坐标

    return：
        tuple: 包含直线的斜率和截距的元组 (a, b, c)
    """
    # 计算delta y
    a = y0 - y1
    # 计算delta x
    b = x1 - x0
    # 计算直线的常数项
    c = x0 * y1 - x1 * y0
    return a, b, c


def get_cross_point(line1, line2):
    """
    计算两条直线的交点坐标。

    params：
        line1 (tuple/list): 第一条直线的参数方程系数，格式为 (a1, b1, c1)。
        line2 (tuple/list): 第二条直线的参数方程系数，格式为 (a2, b2, c2)。

    return：
        list: 交点的坐标，格式为 [y, x]。如果两条直线平行或无交点，则返回 None。
    """
    # 获取直线1的参数方程系数
    a0, b0, c0 = get_line(*line1)
    # 获取直线2的参数方程系数
    a1, b1, c1 = get_line(*line2)
    # 计算两条直线的行列式值
    D = a0 * b1 - a1 * b0
    # 如果行列式值为0,则两条直线平行，无交点
    if D == 0:
        return None
    # 计算交点的坐标
    x = (b0 * c1 - b1 * c0) / D
    y = (a1 * c0 - a0 * c1) / D
    # 返回交点的坐标
    return [x, y]


def smooth_contour(contour, alpha=0.5, beta=0.5):
    """
    对轮廓进行平滑处理，去除噪点。

    params：
        contour (ndarray): 轮廓的点集，形状为 (N, 2)或（N,1,2）。

    return：
        ndarray: 平滑处理后的轮廓，形状为 (N*3,1,2)。
    """
    bezier = []
    convex = cv2.convexHull(contour)
    convex = np.reshape(convex, (-1, 2))
    # contour = list(contour)
    for i in range(len(convex)):
        p = [
            convex[i - 1],
            convex[i],
            convex[(i + 1) % len(convex)],
            convex[(i + 2) % len(convex)],
        ]

        o = np.array(get_cross_point([*p[0], *p[1]], [*p[2], *p[3]]))
        bezier.append(p[1])
        try:
            b = [alpha * p[1] + (1 - alpha) * o, beta * p[2] + (1 - beta) * o]
        except TypeError:
            continue
        bezier.extend(b)

    bezier = np.array(bezier)
    bezier = np.reshape(bezier, (-1, 1, 2))
    bezier = bezier.astype(np.int32)
    return bezier


def get_angle(point1, point2) -> float:
    if point2[0] == point1[0]:
        return np.pi / 2
    return np.arctan((point2[1] - point1[1]) / (point2[0] - point1[0]))


def rotate_image(image: IMAGE, angle: float, point: Sequence[int]) -> IMAGE:
    # print(point[0], point[1])
    rotation_matrix = cv2.getRotationMatrix2D(
        (int(point[0]), int(point[1])), angle * 180 / np.pi, 1
    )
    shape = image.shape[:2]
    image = cv2.warpAffine(image, rotation_matrix, shape[::-1])

    return image


def get_corrector(img1: IMAGE, img2: IMAGE, mode: int = 0) -> float:
    if not mode:
        img2 = cv2.resize(
            img2, (img1.shape[1], img1.shape[0])
        )  # resize img2 to the same size of img1
    else:
        h, w = img1.shape[:2]
        hm, wm = min(h, w), max(h, w)
        img2 = cv2.resize(img2, (hm, hm))
        img2 = cv2.copyMakeBorder(
            img2,
            0,
            0,
            int((wm - hm) / 2),
            wm - hm - int((wm - hm) / 2),
            borderType=cv2.BORDER_CONSTANT,
            value=0,
        )
        # show([img1, img2])
    # print(img1.shape, img2.shape)
    # show([img1, img2])
    # 计算两幅图像之间的相关系数
    assert img2.shape == img1.shape
    corrector = np.corrcoef(img1.flatten(), img2.flatten())[0, 1]

    return corrector


def get_first_no_zero(data: np.ndarray, axis: int = 0) -> int:
    """
    获取data中第一个不为0的元素的索引。

    params：
        data (numpy.ndarray): 输入的二维维数组。
        axis (int): 指定轴，默认为0。

    return：
        int: 第一个不为0的元素的索引。
    """
    args = (data != 0).argmax(axis=axis)
    args = args[args != 0]
    if len(args) > 0:
        return int(np.mean(args))
    else:
        return 0


def sort_coord(points: CONTOUR) -> CONTOUR:
    """
    对给定的点集按照其与中心点的相对位置进行排序。

    params：
        points (numpy.ndarray): 一个包含4个二维点的数组，每个点表示为一个长度为2的一维数组。

    return：
        numpy.ndarray: 一个包含4个已排序点的数组，每个点表示为一个长度为2的一维数组。
    """
    # 如果输入的点的数量不等于4,则直接返回原点集
    # print(points)
    if len(points) != 4:
        raise ValueError("points length must be 4")
    # 将输入的点集reshape成4行2列的矩阵形式
    points = points.reshape(4, 2)

    # 计算所有点的平均值，得到中心点坐标
    center = np.mean(points, axis=0)
    # 初始化左上、右上、左下、右下四个点的变量
    ul, ur, dl, dr = points
    # TODO: 四个点组成凹多边形时会出错
    for point in points:
        if point[0] <= center[0] and point[1] <= center[1]:
            ul = point
        elif point[0] >= center[0] and point[1] <= center[1]:
            ur = point
        elif point[0] >= center[0] and point[1] >= center[1]:
            dr = point
        elif point[0] <= center[0] and point[1] >= center[1]:
            dl = point
    # 将分类后的四个点重新组合成一个数组并返回
    points = np.array([ul, ur, dl, dr])
    return points


def contour2image(contour: CONTOUR) -> IMAGE:
    rect = cv2.boundingRect(contour)
    x, y, w, h = rect
    contour -= ((x, y),)
    image = np.ones((h, w), np.uint8)
    cv2.fillPoly(image, [contour], 255)

    return image


def contour2polygon(
    contour: CONTOUR, poly: int = 4, max_epsilon: float = 100
) -> CONTOUR:
    last_epsilon = max_epsilon
    epsilon = max_epsilon / 2
    epoch = 0
    while True:
        approx_polygon = cv2.approxPolyDP(contour, epsilon, True)
        num = approx_polygon.shape[0]
        if num == poly:
            return approx_polygon
        elif num > poly:
            epsilon, last_epsilon = (epsilon + last_epsilon) / 2, epsilon
        else:
            epsilon, last_epsilon = epsilon / 2, epsilon
        if epoch > 20:
            return approx_polygon
        epoch += 1


def rotate_point(point1, point2, angle) -> List:
    x1, y1 = point1
    x2, y2 = point2
    cos = np.cos
    sin = np.sin
    x = int((x1 - x2) * cos(angle) - (y1 - y2) * sin(angle) + x2)
    y = int((x1 - x2) * sin(angle) + (y1 - y2) * cos(angle) + y2)

    return [x, y]


def get_top_point(image: IMAGE) -> List:
    height, width = image.shape[:2]
    y_indices = (image != 0).argmax(axis=0)
    y_indices[y_indices == 0] = height
    x = y_indices.argmin(axis=0)
    top_point = [x, y_indices[x]]

    return top_point


def get_nearst_point(contour, point):
    contour = np.reshape(contour, (-1, 2))
    dists = np.linalg.norm(contour - point, axis=1)
    index = np.argmin(dists)
    return contour[index]


def crop_images(
    images: Sequence[IMAGE],
    y1: int,
    x1: int,
    y2: Optional[int] = None,
    x2: Optional[int] = None,
) -> Sequence[IMAGE]:
    if isinstance(images, (tuple, list)):
        temp = []
        for image in images:
            temp.append(image[y1:y2, x1:x2])
    else:
        temp = images[y1:y2, x1:x2]
    return temp


def draw_dash_line(
    img, pt1, pt2, color=(0, 0, 255), thickness=1, style="dotted", gap=20
):
    dist = ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5
    pts = []
    for i in np.arange(0, dist, gap):
        r = i / dist
        x = int((pt1[0] * (1 - r) + pt2[0] * r) + 0.5)
        y = int((pt1[1] * (1 - r) + pt2[1] * r) + 0.5)
        p = (x, y)
        pts.append(p)
    if style == "dotted":
        for p in pts:
            cv2.circle(img, p, thickness, color, -1)
    else:
        for i in range(0, len(pts) - 1, 2):
            cv2.line(img, pts[i], pts[i + 1], color, thickness)
    return img


if __name__ == "__main__":
    pass
