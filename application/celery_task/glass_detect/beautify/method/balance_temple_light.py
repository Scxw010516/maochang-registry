import numpy as np
import cv2


def get_mean_light(
    image: np.ndarray,
    mask: np.ndarray,
):
    assert len(mask.shape) == 2 and len(image.shape) == 3
    if image.shape[2] == 4:
        image_bgr = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    else:
        image_bgr = image
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    light = image_hsv[:, :, 2]
    mean_light = np.mean(light[mask != 0])
    return mean_light


def balance_light_local(
    temple_image: np.ndarray,
    temple_mask: np.ndarray,
    front_image: np.ndarray,
    front_mask: np.ndarray,
    front_margin: float = 0.025,
    temple_local: bool = True,
    temple_margin: float = 0.1,
):
    temple_alpha = temple_image[:, :, 3]
    temple_image_bgr = cv2.cvtColor(temple_image, cv2.COLOR_BGRA2BGR)
    temple_image_hsv = cv2.cvtColor(temple_image_bgr, cv2.COLOR_BGR2HSV)
    # fornt_image_bgr = cv2.cvtColor(front_image, cv2.COLOR_BGRA2BGR)
    # fornt_image_hsv = cv2.cvtColor(fornt_image_bgr, cv2.COLOR_BGR2HSV)
    assert front_margin <= 1 and temple_margin <= 1
    temple_rect = cv2.boundingRect(temple_mask)
    front_rect = cv2.boundingRect(front_mask)

    # front crop
    front_image_left_crop = front_image[
        :, front_rect[0] : front_rect[0] + int(front_rect[2] * front_margin)
    ]
    front_image_right_crop = front_image[
        :,
        front_rect[0]
        + int(front_rect[2] * (1 - front_margin)) : front_rect[0]
        + front_rect[2],
    ]
    front_mask_left_crop = front_mask[
        :, front_rect[0] : front_rect[0] + int(front_rect[2] * front_margin)
    ]
    front_mask_right_crop = front_mask[
        :,
        front_rect[0]
        + int(front_rect[2] * (1 - front_margin)) : front_rect[0]
        + front_rect[2],
    ]
    if temple_local:
        # temple crop
        temple_image_left_crop = temple_image[
            :,
            temple_rect[0] : temple_rect[0] + int(temple_rect[2] * temple_margin),
        ]
        temple_mask_left_crop = temple_mask[
            :,
            temple_rect[0] : temple_rect[0] + int(temple_rect[2] * temple_margin),
        ]
    else:
        temple_image_left_crop = temple_image
        temple_mask_left_crop = temple_mask

    front_light = (
        get_mean_light(front_image_left_crop, front_mask_left_crop)
        + get_mean_light(front_image_right_crop, front_mask_right_crop)
    ) / 2
    temple_light = get_mean_light(temple_image_left_crop, temple_mask_left_crop)
    ratio = front_light / temple_light
    if ratio > 1.3:
        return temple_image
    # print(temple_light, front_light, ratio, flush=True)
    temple_image_hsv[:, :, 2][temple_mask != 0] = (
        temple_image_hsv[:, :, 2][temple_mask != 0] * ratio
    )
    temple_image_hsv[:, :, 2] = np.clip(temple_image_hsv[:, :, 2], 0, 255)
    ret_bgr = cv2.cvtColor(temple_image_hsv, cv2.COLOR_HSV2BGR)
    ret = cv2.cvtColor(ret_bgr, cv2.COLOR_BGR2BGRA)
    ret[:, :, 3] = temple_alpha
    return ret
