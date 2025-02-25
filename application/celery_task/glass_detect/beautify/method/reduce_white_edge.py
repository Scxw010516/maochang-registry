import cv2
import numpy as np


def get_contours(mask):
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )  # 全部轮廓
    contours_inner = [
        contours[i] for i in range(len(contours)) if hierarchy[0][i][3] != -1
    ]  # 内部轮廓
    contours_outer = [
        contours[i] for i in range(len(contours)) if hierarchy[0][i][3] == -1
    ]
    contours_lens = sorted(contours_inner, key=cv2.contourArea, reverse=True)[
        :2
    ]  # 镜片轮廓
    contours_lens = sorted(contours_lens, key=lambda x: x[0][0][0])  # 左右排序
    contours_frame = sorted(contours_outer, key=cv2.contourArea, reverse=True)[:1]
    return contours_frame, contours_lens


def draw_contour(contours, image=None, size=(1600, 3200), width=1, inner=False):
    blank = np.zeros(size)
    mask = np.zeros(size)
    if not isinstance(contours, list):
        contours = [contours]
    cv2.fillPoly(mask, contours, 255)
    cv2.drawContours(blank, contours, -1, 255, width * 2)
    if inner:
        blank[mask == 0] = 0
    else:
        blank[mask != 0] = 0
    if image is None:
        return blank
    image[blank != 0] = 255
    return image


def reduce_white_edge(image, mask, color=(200, 200, 200), width=4, alpha=0.3):
    image_process = image.copy()
    _, countours_lens = get_contours(mask)
    edge_mask = draw_contour(
        countours_lens, size=image.shape[:2], width=width, inner=False
    )
    edge_mask = draw_contour(
        countours_lens, image=edge_mask, size=image.shape[:2], width=1, inner=True
    )
    # edeg_gray = np.zeros((*image.shape[:2], 4), dtype=np.uint8)
    image_process[edge_mask > 0] = [*(color), int(255 * alpha)]
    # cv2.imwrite("test.png", edge_mask)
    return image_process
