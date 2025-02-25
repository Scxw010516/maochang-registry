import cv2
import numpy as np
from .clean_mask import remove_small, keep_topk, clean


def split_contour(contours, hierarchy, min_area=10000):
    # 获取外部和内部轮廓
    external_contours = []
    internal_contours = []
    for i in range(len(contours)):
        if hierarchy[0][i][3] == -1:
            external_contours.append(contours[i])
        else:
            internal_contours.append(contours[i])

    external_contours = [
        sorted(external_contours, key=cv2.contourArea, reverse=True)[0]
    ]

    internal_contours = [
        contour for contour in internal_contours if cv2.contourArea(contour) > min_area
    ]

    return external_contours, internal_contours


def get_contour_center(contour):
    # 计算轮廓的中心 (x,y)
    return contour.reshape(-1, 2).mean(axis=0).astype(np.int32)


def split_contour_with_point(contour, point, margin=5):
    # 以给定点将轮廓分为上下两部分

    contour_points = contour.reshape(-1, 2)
    # 左右margin内的点
    contour_points = contour_points[
        np.where(
            (contour_points[:, 0] < point[0] + margin)
            & (contour_points[:, 0] > point[0] - margin)
        )
    ]
    # 上下划分
    contour_top_points = contour_points[np.where(contour_points[:, 1] < point[1])]
    contour_bottom_points = contour_points[np.where(contour_points[:, 1] >= point[1])]

    return contour_top_points, contour_bottom_points


def get_front(mask_frame, mask_lens, threshold=10, margin=5):
    mask_frame = mask_frame.copy()
    mask_lens = mask_lens.copy()

    mask_front = mask_frame.copy()
    mask_front[mask_lens != 0] = 0
    mask_front = clean(mask_front, 10000, 1)
    # 获取轮廓
    contours_frame, hierarchy_frame = cv2.findContours(
        mask_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )
    contour_frame, contour_bg = split_contour(contours_frame, hierarchy_frame, 10000)
    contour_frame = contour_frame[0]

    contour_lens, hierarchy_lens = cv2.findContours(
        mask_lens, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    contour_lens = sorted(contour_lens, key=lambda x: cv2.contourArea(x), reverse=True)[
        :2
    ]
    contour_lens = sorted(contour_lens, key=lambda x: get_contour_center(x)[0])
    # 获取类型
    # 计算lens中心点
    centers = [get_contour_center(cnt) for cnt in contour_lens]

    # left_point, left_bottom, right_top, right_bottom
    frame_points = [
        p
        for i in range(2)
        for p in split_contour_with_point(contour_frame, centers[i], margin=margin)
    ]
    lens_points = [
        p
        for i in range(2)
        for p in split_contour_with_point(contour_lens[i], centers[i], margin=margin)
    ]

    # 异常处理 检查空列表
    for i in range(4):
        if len(frame_points[i]) == 0 or len(lens_points[i]) == 0:
            frame_points[i] = np.array([[1, 1]] * (2 * margin + 1), dtype=np.int32)
            lens_points[i] = np.array([[1, 1]] * (2 * margin + 1), dtype=np.int32)

    # 获取均高
    frame_height = np.array([np.mean(points[:, 1]) for points in frame_points])
    lens_height = np.array([np.mean(points[:, 1]) for points in lens_points])

    # 高度差
    height_diff = frame_height - lens_height
    num_close = np.sum(np.abs(height_diff) < threshold)

    frame_type = 0
    if num_close >= 3:
        frame_type = 2

    elif num_close >= 2:
        frame_type = 1
    else:
        frame_type = 0

    # 镜框补上轮廓
    max_value = int(np.max(mask_front))
    if frame_type != 0:
        cv2.drawContours(mask_front, contour_lens, -1, max_value, 3)
    else:
        cv2.drawContours(mask_front, contour_lens, -1, max_value, 1)
    return mask_front, frame_type


def get_front_mask(mask_frame, mask_lens, frame_type=0):
    # 在镜框中补上镜片轮廓，防止不连续
    mask_frame = mask_frame.copy()
    mask_lens = mask_lens.copy()

    mask_front = mask_frame.copy()
    mask_front[mask_lens != 0] = 0
    mask_front = clean(mask_front, 10000, 1)

    # 获取镜片轮廓
    contour_lens, hierarchy_lens = cv2.findContours(
        mask_lens, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    contour_lens = sorted(contour_lens, key=lambda x: cv2.contourArea(x), reverse=True)[
        :2
    ]
    contour_lens = sorted(contour_lens, key=lambda x: get_contour_center(x)[0])

    # 镜框补上轮廓
    max_value = int(np.max(mask_front))
    thickness = 3 if frame_type != 0 else 1
    cv2.drawContours(mask_front, contour_lens, -1, max_value, thickness)

    return mask_front
