import sys
import os
from skimage import morphology

# sys.path.append('./EfficientSAM')
from .segment_onnx import segment_onnx
from .utils import *


def sort_contours(contours, center):
    centers = np.array([get_contour_center(contour) for contour in contours])
    distances = np.linalg.norm(centers - center, axis=1)
    # 使用argsort获取按距离排序的索引
    sorted_indices = np.argsort(distances)
    contours = [contours[i] for i in sorted_indices]
    return contours


def get_by_lc(
    image: IMAGE,
    num_gaussian: int = 3,
    thresholds: Sequence[float] = (20, 10000, 10000),
    thresh: int = 30,
    num_iter: Sequence[int] = (10, 5),
):
    kernel = np.ones((3, 3), np.uint8)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = gaussian_blur(gray, num_gaussian)

    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyMap) = saliency.computeSaliency(blur)
    saliencyMap = (saliencyMap * 255).astype("uint8")
    _, th = cv2.threshold(saliencyMap, thresh, 255, cv2.THRESH_BINARY)
    show(th)
    # 去除小的前景（噪声，细小颗粒）
    clean_1 = remove_small(th, thresholds[0])

    # 膨胀
    img_dilate = cv2.dilate(clean_1, kernel, iterations=num_iter[0])
    # 去除小的前景（噪声，细小颗粒）
    clean_2 = remove_small(img_dilate, thresholds[1])

    # 填补前景中空洞
    filled = fill_small(clean_2, thresholds[2])

    # 腐蚀
    img_erode = cv2.erode(filled, kernel, iterations=num_iter[0] + num_iter[1])
    # 去除小的前景（噪声，挡板）
    clean_3 = remove_small(img_erode, thresholds[3])

    img = cv2.dilate(clean_3, kernel, iterations=num_iter[1])
    return img


def get_by_threshold(
    image: IMAGE,
    num_gaussian: int = 3,
    thresholds: Sequence[float] = (20, 10000),
    num_iter: Sequence[int] = (10, 5),
):
    kernel = np.ones((3, 3), np.uint8)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = gaussian_blur(gray, num_gaussian)

    threshold = find_threshold(blur, length=20, scale=1.5)
    if threshold != -1:
        ret, th = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY_INV)
    else:
        ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    show(th)
    # 去除小的前景（噪声，细小颗粒）
    clean_1 = remove_small(th, thresholds[1])

    filled = fill_small(clean_1, thresholds[1])
    show(filled)
    img_erode = cv2.erode(filled, kernel, iterations=num_iter[1])
    img_dilate = cv2.dilate(img_erode, kernel, iterations=num_iter[1])
    show(img_dilate)
    img = remove_small(img_dilate, thresholds[2])
    show(img)

    # img = filled
    return img


def get_by_morphology(
    image: IMAGE,
    num_gaussian: int = 3,
    block_size: int = 15,
    C: int = 3,
    thresholds: Sequence[float] = (20, 10000, 10000, 10000),
    num_iter: Sequence[int] = (8, 4),
    mask: Optional[IMAGE] = None,
) -> IMAGE:
    """
    对图像进行形态学预处理以提取和优化轮廓

    params：
        - image: IMAGE - 输入的彩色或灰度图像数据
        - num_gaussian: int - 应用于图像的高斯模糊次数，默认为3次，用以降噪
        - block_size: int - 自适应阈值二值化时的邻域大小
        - C: int - 自适应阈值二值化时的常数因子
        - thresholds: Sequence[float] - 一系列面积阈值，用于在不同阶段移除小物体（噪声）或填充空洞
        - num_iter: Sequence[int] - 膨胀与腐蚀操作迭代次数的列表
        - mask: Optional[IMAGE] - 可选的掩模图像，若提供则会在特定区域应用操作

    return：
        - img: IMAGE - 经过一系列形态学操作后的图像，包含优化后的前景对象轮廓
    """
    # 形态学处理卷积核
    kernel = np.ones((3, 3), np.uint8)
    # 灰度化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊num_gaussian次,去噪
    blur = gaussian_blur(gray, num_gaussian)

    # 自适应阈值二值化
    adaptive = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C
    )
    _, adaptive = cv2.threshold(adaptive, 150, 255, cv2.THRESH_BINARY_INV)
    show(adaptive, "adaptive")
    # print(mask)
    # show(adaptive)
    # 将掩膜出变为背景
    if mask is not None:
        adaptive[mask == 255] = 0

    # 去除小的前景（噪声，细小颗粒）
    clean_1 = remove_small(adaptive, thresholds[0])
    # show(clean_1, "clean1")

    # 膨胀
    img_dilate = cv2.dilate(clean_1, kernel, iterations=num_iter[0])
    # 去除小的前景（噪声，细小颗粒）
    clean_2 = remove_small(img_dilate, thresholds[1])
    # show(clean_2, "clean2")

    # 填补前景中空洞
    filled = fill_small(clean_2, thresholds[2])
    # show(filled, "filled")

    # 腐蚀
    img_erode = cv2.erode(filled, kernel, iterations=num_iter[0] + num_iter[1])
    # 去除小的前景（噪声，挡板）
    clean_3 = remove_small(img_erode, thresholds[3])

    img = cv2.dilate(clean_3, kernel, iterations=num_iter[1])

    return img


def get_by_bs(
    image: IMAGE,
    background: IMAGE,
    thresholds: Sequence[int] = (20, 30),
    num_gaussian: int = 3,
) -> IMAGE:
    gray_background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    gray_glasses = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_background = gaussian_blur(gray_background, num_gaussian)
    gray_glasses = gaussian_blur(gray_glasses, num_gaussian)

    gray_background = gray_background.astype(np.int32)
    gray_glasses = gray_glasses.astype(np.int32)

    gray_subtraction = gray_glasses - gray_background
    gray_subtraction[np.abs(gray_subtraction) < thresholds[0]] = 255

    gray_subtraction = (255 - gray_subtraction).astype(np.uint8)

    # show(gray_subtraction, "subtraction")

    _, th = cv2.threshold(gray_subtraction, thresholds[1], 255, cv2.THRESH_BINARY)

    th = remove_small(th, 10000)
    th = fill_small(th, 10000)

    # show(th, "th")

    return th


def get_by_sam(
    image: IMAGE,
    gray: IMAGE,
    edge_width: int = 10,
    onnx_path: str = "efficient_sam_vits.onnx",
) -> Tuple[IMAGE, CONTOURS, int]:
    height, width = image.shape[:2]
    combine = gray.copy()
    # 去除镜片边缘
    combine = cv2.erode(combine, np.ones((5, 5), np.uint8), iterations=2)
    combine = cv2.dilate(combine, np.ones((5, 5), np.uint8), iterations=2)
    combine = remove_small(combine, combine.shape[0] * combine.shape[1] * 0.001)
    combine = fill_small(combine, combine.shape[0] * combine.shape[1] * 0.001)

    # 获取镜架轮廓
    contours_gray, _ = cv2.findContours(combine, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_gray = sort_contours(contours_gray, (width // 2, height // 2))[0]
    rect = cv2.boundingRect(contour_gray)
    x, y, w, h = rect
    print(w, width, w / width)
    if w / width >= 0.6:
        glasses_type = 1
        splits = [x + w // 2 - w // 8, x + w // 2, x + w // 2 + w // 8]
    else:
        glasses_type = 2
        splits = [x, x + w // 2, x + w]

    # 骨骼化
    skeleton = morphology.skeletonize(combine)

    # 分为四部分
    skeleton_parts = [skeleton[y : y + h, splits[i] : splits[i + 1]] for i in range(2)]
    # 寻找中间两部分最下方的点
    points = [get_top_point(part[::-1]) for part in skeleton_parts]
    points = [[p[0] + splits[i], h - p[1] + y] for i, p in enumerate(points)]

    # sam找出边缘
    margin = 10
    x1 = margin
    y1 = margin
    x2 = width - margin
    y2 = height - margin
    # sam边框
    sam_points = [[x1, y1], [x2, y2]]
    sam_labels = [1, 2]

    # sam分割
    masks = segment_onnx(image, sam_points, sam_labels, onnx_path)
    masks = [mask.astype(np.uint8) * 255 for mask in masks]
    # 与bs结果相似度
    correctors = [get_corrector(gray, mask) for mask in masks]
    mask = masks[np.argmax(correctors)]
    # 去除小物体，填补空白
    mask = remove_small(mask, height * width * 0.001)
    mask = fill_small(mask, height * width * 0.001)
    contours_big, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_big = sorted(contours_big, key=lambda x: cv2.contourArea(x), reverse=True)[
        0
    ]
    # 腐蚀
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=5)

    # sam 轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)[0]
    cv2.drawContours(combine, [contour], 0, 255, edge_width)
    combine = fill_small(combine, combine.shape[0] * combine.shape[1] * 0.01)

    # 找出sam下边缘
    sorted_ids = np.argsort(contour[:, 0, 0], axis=0)
    if sorted_ids[0] < sorted_ids[-1]:
        contour_down = contour[sorted_ids[0] : sorted_ids[-1]]
    else:
        contour_down = np.concatenate(
            (contour[sorted_ids[0] :], contour[: sorted_ids[-1]]), axis=0
        )

    # 将下边缘按点分为左右两部分
    contour_down_left = contour_down[
        np.logical_and(
            contour_down[:, 0, 0] < points[0][0], contour_down[:, 0, 1] > points[0][1]
        )
    ]
    contour_down_right = contour_down[
        np.logical_and(
            contour_down[:, 0, 0] > points[1][0], contour_down[:, 0, 1] > points[0][1]
        )
    ]

    # sam下边缘与镜架鼻托处下方最近点
    nearst_points = [
        get_nearst_point(contour_down_left, points[0]),
        get_nearst_point(contour_down_right, points[1]),
    ]

    # 将sam边缘与镜架边缘连接
    for i in range(2):
        cv2.line(combine, tuple(points[i]), tuple(nearst_points[i]), 255, edge_width)

    combine = fill_small(combine, combine.shape[0] * combine.shape[1] * 0.01)
    cv2.drawContours(
        combine, [contour_big], 0, 0, edge_width - 10 if edge_width - 10 > 0 else 0
    )
    combine = fill_small(combine, combine.shape[0] * combine.shape[1] * 0.005)

    contours, areas = get_contours(combine, combine.shape[0] * combine.shape[1] * 0.05)
    lens_incomplete_temp = get_lens_incomplete(contours, areas, 1.1)

    lens = remove_legs(lens_incomplete_temp, combine.shape, 200)

    return combine, lens, glasses_type


def get_lens(
    image: IMAGE,
    background: Optional[IMAGE] = None,
    thresholds: Sequence[int] = (20, 30),
    num_gaussian: int = 3,
    area_threshold: float = 50000,
    ratio: float = 1.1,
) -> Tuple[IMAGE, CONTOURS, int]:
    glasses_type = 0
    if background is None:
        raise ValueError("background must not be None")
    img_morphology = get_by_bs(
        image,
        background,
        thresholds=thresholds,
        num_gaussian=num_gaussian,
    )

    # 按照面积大小获取前部轮廓
    contours, areas = get_contours(img_morphology, area_threshold)

    # 获取镜片轮廓(有镜腿)
    try:  # 全框
        lens_incomplete = get_lens_incomplete(contours, areas, ratio)
    except ValueError:  # 半框和无框
        print("Using SAM.")
        module_path = os.path.dirname(__file__)
        onnx_path = os.path.join(module_path, "efficient_sam_vits.onnx")
        img_morphology, lens_incomplete, glasses_type = get_by_sam(
            image, img_morphology, onnx_path=onnx_path
        )

    lens = remove_legs(lens_incomplete, img_morphology.shape, 200)

    lens.sort(key=lambda x: get_contour_center(x)[0])

    return img_morphology, lens, glasses_type
