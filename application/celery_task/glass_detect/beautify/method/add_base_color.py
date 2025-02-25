import cv2
import numpy as np

from .blend import normal


def add_base_color(image, mask, image_base=None, min_saturation_value=240, alpha=0.5):
    assert len(image.shape) == 3, "image must be in H,W,C"
    assert image.shape[2] == 4, "image must be in BGRA"
    image_bgr = image[:, :, :3]
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    # 饱和度增加20%，亮度降低10%
    image_hsv[:, :, 1] *= 1.2
    image_hsv[:, :, 2] *= 0.8
    image_hsv = np.clip(image_hsv, 0, 255).astype(np.uint8)

    # 找到最大饱和度值位置
    saturation_channel = image_hsv[:, :, 1]
    max_saturation_value = np.max(saturation_channel)

    max_saturation_position = np.unravel_index(
        np.argmax(saturation_channel), saturation_channel.shape
    )
    max_saturation_pixel_hsv = image_hsv[
        max_saturation_position[0], max_saturation_position[1]
    ]

    max_saturation_pixel_hsv[1] = max(min_saturation_value, max_saturation_value)

    max_saturation_pixel_bgr = cv2.cvtColor(
        np.array(max_saturation_pixel_hsv).reshape((1, 1, -1)), cv2.COLOR_HSV2BGR
    )[0][0]
    # max_saturation_pixel_bgr[1]

    image_color = np.ones_like(image)
    image_color[:, :, 0] = max_saturation_pixel_bgr[0]
    image_color[:, :, 1] = max_saturation_pixel_bgr[1]
    image_color[:, :, 2] = max_saturation_pixel_bgr[2]
    image_color[:, :, 3] = mask * 255
    if image_color is None:
        return normal(image, image_color, alpha=alpha)
    return normal(image_base, image_color, alpha=alpha)
    # cv2.imwrite("./base.png", image_base)
    # print(max_saturation_pixel_bgr)


def main():
    sku = "201300283010630992"

    image_path = f"./temp/image/{sku}_1.png"
    mask_path = f"./temp/mask/{sku}_1.png"
    nose_path = f"./temp/nose/{sku}_1.png"
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    nose = cv2.imread(nose_path, cv2.IMREAD_GRAYSCALE)

    image_new = add_base_color(image, mask, alpha=0.4)
    cv2.imwrite("test.png", image_new)
    cv2.imwrite("test1.png", image)


if __name__ == "__main__":
    main()
