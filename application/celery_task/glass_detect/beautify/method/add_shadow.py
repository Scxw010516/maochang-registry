from typing import List, Tuple, Union

import cv2
import numpy as np

from .blend import normal


def add_shadow(
    image,
    mask=None,
    offset: Union[Tuple[int], List[int]] = (0, 20),
    alpha: float = 0.5,
    expansion: int = 10,
):
    assert image.shape[2] == 4, "image must be RGBA"
    mask_ori = image[:, :, 3] if mask is None else mask.copy()
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask_ori, kernel, iterations=expansion)
    # 计算距离变换
    distance_transform = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
    # distance_binary = distance_transform > 0
    # skeleton = morphology.skeletonize(mask_ori)
    # # show(distance_transform, revert=True)
    # print(np.mean(distance_transform[skeleton == 1]))
    # 归一化距离变换
    normalized_distance = cv2.normalize(distance_transform, None, 0, 1, cv2.NORM_MINMAX)
    shadow = np.zeros_like(image)
    # 转变尺度
    shadow_mask = (normalized_distance * 255).astype(np.uint8)

    # cv2.GaussianBlur(shadow_mask, (51, 51), 10, shadow_mask)
    shadow_mask = cv2.medianBlur(shadow_mask, 41).astype(np.float64)
    shadow_mask *= alpha
    shadow_mask = np.clip(shadow_mask, 0, 255).astype(np.uint8)
    # shadow_mask[shadow_mask > 150] = 150
    shadow[:, :, 3] = shadow_mask
    # cv2.imwrite("./ps/shadow.png", shadow)
    h, w = image.shape[:2]
    x, y = offset
    x_abs, y_abs = abs(x), abs(y)
    blank = np.zeros((h + 2 * y_abs, w + 2 * x_abs, 4), dtype=np.uint8)
    blank[y_abs : y_abs + h, x_abs : x_abs + w] = shadow

    shadow = blank[y_abs - y : y_abs - y + h, x_abs - x : x_abs - x + w]
    return normal(shadow, image)
    # return


def show(image, revert=False):
    if len(image.shape) == 3 and image.shape[2] == 4:
        mask = image[:, :, 3]

        image = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGRA2BGR)

        image[mask == 0] = [0, 0, 0]
    if revert:
        image = abs(255 - image)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def apply_curve(channel, curve):
    return np.interp(channel, [0, 255], curve)


def main():
    foreground_path = "D:/Project/utils/ps/foreground.png"
    foreground = cv2.imread(foreground_path, cv2.IMREAD_UNCHANGED)
    ret = add_shadow(foreground, alpha=0.5, expansion=10, offset=(0, 60))
    cv2.imwrite("./ps/ret.png", ret)
    # show(ret)
    # plt.title("RGB Curves")
    # plt.plot(x, adjusted_r, color="r", label="Red Curve")
    # plt.show()


if __name__ == "__main__":
    main()
