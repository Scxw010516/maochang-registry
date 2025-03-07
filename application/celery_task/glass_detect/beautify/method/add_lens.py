import random

import cv2
import numpy as np

from .blend import normal


def test():
    mask_path = "./mask.png"
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    mask *= 255

    cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    cv2.imshow("mask", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_contours(contours):
    if not isinstance(contours, list):
        contours = [contours]
    blank = np.zeros((1600, 3200, 3), dtype=np.uint8)
    cv2.drawContours(blank, contours, -1, (255, 255, 255), 10)
    # cv2.fillPoly(blank, contours, 255)
    cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    cv2.imshow("mask", blank)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def contour2mask(contour, align=True, size=None):
    # height = np.max(contour)
    if not align:
        if size is None:
            raise ValueError("size must be specified when align=False")
        blank = np.zeros((size), dtype=np.uint8)
        cv2.fillPoly(blank, [contour], 255)
        return blank
    else:
        x, y, w, h = cv2.boundingRect(contour)
        contour -= [x, y]
        blank = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(blank, [contour], 255)
        return blank


def get_lens_contours(mask):
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )  # 全部轮廓
    contours = [
        contours[i] for i in range(len(contours)) if hierarchy[0][i][3] != -1
    ]  # 内部轮廓
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]  # 镜片轮廓
    contours = sorted(contours, key=lambda x: x[0][0][0])  # 左右排序

    return contours


def get_reflection(mask, ratio=0.3, alpha=1):
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    lens_path = os.path.join(os.path.dirname(current_dir), "reflection","lens.png")
    lens = cv2.imread(lens_path, cv2.IMREAD_UNCHANGED)
    # lens_mask = lens[:, :, 3].astype(np.float32)
    # lens_mask = (lens_mask * alpha).astype(np.uint8)
    assert lens.shape[2] == 4, "lens must be in BGRA or RGBA"
    h, w = lens.shape[:2]
    # 随机shadow
    shadow_index = random.randint(1, 3)
    shadow_path = os.path.join(os.path.dirname(current_dir), "reflection", f"{shadow_index}.png")
    shadow = cv2.imread(shadow_path, cv2.IMREAD_UNCHANGED)
    if len(shadow.shape) != 2:
        shadow = cv2.cvtColor(shadow, cv2.COLOR_BGR2GRAY)
    shadow_h, shadow_w = shadow.shape
    # shadow随机位置
    x, y = random.randint(w // 5, w // 5 * 4), random.randint(h // 5, h // 5 * 4)
    # shadow随机大小
    shadow_h, shadow_w = (
        random.randint(int(shadow_h * 0.9), int(shadow_h * 1)),
        random.randint(int(shadow_w * 0.9), int(shadow_w * 1)),
    )
    shadow = cv2.resize(shadow, (shadow_w, shadow_h))
    # 添加shadow
    blank = np.zeros((h + 2 * shadow_h, w + 2 * shadow_w, 4), dtype=np.uint8)
    blank[shadow_h : shadow_h + h, shadow_w : shadow_w + w] = lens
    lens_crop = blank[y : y + shadow_h, x : x + shadow_w].astype(np.float32)
    lens_crop[:, :, 3][shadow > 0] *= ratio
    blank[y : y + shadow_h, x : x + shadow_w] = lens_crop
    lens = blank[shadow_h : shadow_h + h, shadow_w : shadow_w + w]
    lens = cv2.resize(lens, mask.shape[:2][::-1])
    lens[:, :, 3][mask == 0] = 0
    return lens.astype(np.uint8)


def add_lens(
    glasses,
    mask,
    reflections=None,
    mode="normal",
    ratio=0.3,
    alpha=1,
):
    contours = get_lens_contours(mask)
    rects = [cv2.boundingRect(contour) for contour in contours]
    lens_masks = [contour2mask(contour) for contour in contours]

    # show(lens_mask)
    if reflections is None:
        reflections = [
            get_reflection(lens_mask, ratio=ratio, alpha=alpha)
            for lens_mask in lens_masks
        ]
    else:
        reflections = [reflections for _ in range(len(lens_masks))]
    # cv2.imwrite("reflect.png", reflections[0])
    for i in range(2):
        reflection = reflections[i]
        reflection = cv2.resize(reflection, (rects[i][2], rects[i][3]))
        alpha = reflection[:, :, 3]
        rect = rects[i]
        crop = glasses[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2]]
        if mode == "normal":
            crop = normal(crop, reflection)
        else:
            crop[alpha != 0] = reflection[alpha != 0]
        glasses[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2]] = crop

    return glasses


def main():
    import os
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    glasses_path = "glasses.png"
    mask_path = "mask.png"
    glasses = cv2.imread(glasses_path, cv2.IMREAD_UNCHANGED)
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    # reflection = cv2.imread("reflection/lens.png", cv2.IMREAD_UNCHANGED)
    # print(reflection.shape)
    # glasses = add_lens(glasses, mask, reflections=reflection)
    glasses = add_lens(glasses, mask)
    cv2.imwrite("glasses_lens.png", glasses)


if __name__ == "__main__":
    # test()
    main()
