import cv2
import numpy as np


def darken(target, blend, alpha=1):
    # 变暗
    target_bgr = target[:, :, :3]
    blend_bgr = blend[:, :, :3]
    target_alpha = target[:, :, 3] / 255
    blend_alpha = blend[:, :, 3] / 255 * alpha
    img = np.minimum(target_bgr, blend_bgr)
    img = (img * alpha + target_bgr * (1 - alpha)).astype(np.uint8)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    img[:, :, 3] = ((blend_alpha + target_alpha * (1 - blend_alpha)) * 255).astype(
        np.uint8
    )

    return img


def darker(target, blend, alpha=1):
    target_bgr = target[:, :, :3]
    blend_bgr = blend[:, :, :3]
    target_alpha = target[:, :, 3] / 255
    blend_alpha = blend[:, :, 3] / 255 * alpha

    if np.sum(target_bgr) == np.sum(blend_bgr):
        target_Y = np.sum(cv2.cvtColor(target_bgr, cv2.COLOR_BGR2YCrCb)[:, :, 0])
        blend_Y = np.sum(cv2.cvtColor(blend_bgr, cv2.COLOR_BGR2YCrCb)[:, :, 0])
        if target_Y <= blend_Y:
            img = target_bgr
        else:
            img = blend_bgr
    elif np.sum(target_bgr) > np.sum(blend_bgr):
        img = blend_bgr
    else:
        img = target_bgr
    img = (img * alpha + target_bgr * (1 - alpha)).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    img[:, :, 3] = ((blend_alpha + target_alpha * (1 - blend_alpha)) * 255).astype(
        np.uint8
    )
    return img


def multiply(target, blend, alpha=1):
    # 正片叠底
    return np.array(np.multiply(target / 255, blend / 255) * 255, dtype=np.uint8)


def color_burn(target, blend, alpha=1):
    # 颜色加深
    target_bgr = target[:, :, :3] / 255
    blend_bgr = blend[:, :, :3] / 255
    target_alpha = target[:, :, 3] / 255
    blend_alpha = blend[:, :, 3] / 255 * alpha

    img = (1 - (1 - target_bgr) / blend_bgr) * 255
    img = np.clip(img, 0, 255)

    img = (img * alpha + target_bgr * (1 - alpha) * 255).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    img[:, :, 3] = ((blend_alpha + target_alpha * (1 - blend_alpha)) * 255).astype(
        np.uint8
    )

    return img


def linear_burn(target, blend, alpha=1):
    # 线性加深
    return target / 255 + blend / 255 - 1


def lighten(target, blend, alpha=1):
    # 变亮
    target_bgr = target[:, :, :3]
    blend_bgr = blend[:, :, :3]
    target_alpha = target[:, :, 3] / 255
    blend_alpha = blend[:, :, 3] / 255 * alpha
    img = np.maximum(target_bgr, blend_bgr)
    img = (img * alpha + target_bgr * (1 - alpha)).astype(np.uint8)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    img[:, :, 3] = ((blend_alpha + target_alpha * (1 - blend_alpha)) * 255).astype(
        np.uint8
    )

    return img


def screen(target, blend, alpha=1):
    # 滤色
    return 1 - (1 - target / 255) * (1 - blend / 255)


def color_dodge(target, blend, alpha=1):
    # 颜色减淡
    target = target / 255
    blend = blend / 255
    return target + (target * blend) / (1 - blend)


def linear_dodge(target, blend, alpha=1):
    # 线性减淡
    return cv2.add(target, blend)


def overlay(target, blend, alpha=1):
    # 叠加
    mask1 = target <= 128
    mask2 = target > 128
    img = np.zeros(target.shape, dtype=np.float64)
    img[mask1] = np.multiply(
        target[mask1] / 255, blend[mask1] / 255
    )  # （暗部正片叠底，更暗）
    img[mask2] = 1 - (1 - target[mask2] / 255) * (
        1 - blend[mask2] / 255
    )  # （亮部滤色，更亮）
    return img


def soft_light(target, blend, alpha=1):
    # 柔光
    mask1 = blend <= 128
    mask2 = blend > 128
    target = target / 255
    blend_alpha = blend[:, :, 3] / 255 * alpha
    img = np.zeros(target.shape, dtype=np.float64)
    img[mask1] = (target[mask1] * blend[mask1]) / 0.5 + (
        target[mask1] * target[mask1]
    ) * (1 - 2 * blend[mask1])
    img[mask2] = (target[mask2] * (1 - blend[mask2])) / 0.5 + np.sqrt(target[mask2]) * (
        2 * blend[mask2] - 1
    )
    return img


def hard_light(target_ori, blend_ori, alpha=1):
    # 强光
    target = target_ori[:, :, :3]
    blend = blend_ori[:, :, :3]
    target_alpha = target_ori[:, :, 3] / 255
    blend_alpha = blend_ori[:, :, 3] / 255 * alpha

    mask1 = blend <= 128
    mask2 = blend > 128
    target = target / 255
    blend = blend / 255
    img = np.zeros(target.shape, dtype=np.float64)
    img[mask1] = target[mask1] * blend[mask1] * 2
    img[mask2] = 1 - (1 - target[mask2]) * (1 - blend[mask2]) * 2

    img = img * alpha + target * (1 - alpha)

    img = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = ((blend_alpha + target_alpha * (1 - blend_alpha)) * 255).astype(
        np.uint8
    )

    return img


def vivid_Light(target, blend, alpha=1):
    # 亮光
    mask1 = blend <= 128
    mask2 = blend > 128
    target = target / 255
    blend = blend / 255
    img = np.zeros(target.shape, dtype=np.float64)
    img[mask1] = target[mask1] - (1 - target[mask1]) * (1 - 2 * blend[mask1]) / (
        2 * blend[mask1]
    )
    img[mask2] = target[mask2] + target[mask2] * (2 * blend[mask2] - 1) / (
        2 * (1 - blend[mask2])
    )
    return img


def linear_light(target, blend, alpha=1):
    # 线性光
    return target / 255 + 2 * blend / 255 - 1


def luminosity(target, blend, alpha=1):
    # 明度
    target_bgr = target[:, :, :3]
    blend_bgr = blend[:, :, :3]
    target_alpha = target[:, :, 3] / 255
    blend_alpha = blend[:, :, 3] / 255 * alpha
    mask = blend_alpha + target_alpha * (1 - blend_alpha)

    target_hsv = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2YCrCb)
    blend_hsv = cv2.cvtColor(blend_bgr, cv2.COLOR_BGR2YCrCb)
    # target_hsv[:, :, 0] = blend_hsv[:, :, 0]
    t_l, b_l = target_hsv[:, :, 0], blend_hsv[:, :, 0]
    r_l = blend_alpha * b_l + (1 - blend_alpha) * t_l
    target_hsv[:, :, 0] = r_l
    img = cv2.cvtColor(target_hsv, cv2.COLOR_YCrCb2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    img[:, :, 3] = (mask * 255).astype(np.uint8)
    return img


def normal(target, blend, alpha=1):
    # 正常
    target_bgr = target[:, :, :3]
    blend_bgr = blend[:, :, :3]
    target_alpha = target[:, :, 3] / 255
    blend_alpha = blend[:, :, 3] / 255 * alpha

    mask = blend_alpha + target_alpha * (1 - blend_alpha)

    blend_alpha3 = np.repeat(blend_alpha[..., np.newaxis], 3, axis=2)
    target_alpha3 = np.repeat(target_alpha[..., np.newaxis], 3, axis=2)

    mask_repeat = np.repeat(mask[..., np.newaxis], 3, axis=2)
    mask_repeat[mask_repeat == 0] = 1e-10  # 避免除数为0
    img = (
        blend_bgr * blend_alpha3 + target_bgr * target_alpha3 * (1 - blend_alpha3)
    ) / mask_repeat

    img = img.astype(np.uint8)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = (mask * 255).astype(np.uint8)
    return img


def divide(target, blend, alpha=1):
    # 划分
    target_bgr = target[:, :, :3]
    blend_bgr = blend[:, :, :3]
    target_alpha = target[:, :, 3] / 255
    blend_alpha = blend[:, :, 3] / 255 * alpha

    # img = np.zeros_like(target).astype(np.float64)
    img = (target_bgr / blend_bgr) * 255
    img = np.clip(img, 0, 255)
    img = (img * alpha + target_bgr * (1 - alpha)).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = ((blend_alpha + target_alpha * (1 - blend_alpha)) * 255).astype(
        np.uint8
    )
    # img = img.astype(np.uint8)

    return img


def substract(target, blend, alpha=1, fill=1):
    target_bgr = target[:, :, :3]
    blend_bgr = blend[:, :, :3]
    target_alpha = target[:, :, 3] / 255
    blend_alpha = blend[:, :, 3] / 255 * alpha

    img = (target_bgr.astype(np.float64) - blend_bgr.astype(np.float64)) * fill + (
        1 - fill
    ) * target_bgr

    img = np.clip(img, 0, 255).astype(np.uint8)
    img = (img * alpha + target_bgr * (1 - alpha)).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = ((blend_alpha + target_alpha * (1 - blend_alpha)) * 255).astype(
        np.uint8
    )
    return img


if __name__ == "__main__":
    face_path = "D:/Project/utils/ps/0.png"
    face = cv2.imread(face_path, cv2.IMREAD_UNCHANGED)
    print(face.shape)
    # face = cv2.cvtColor(face, cv2.COLOR_BGR2BGRA)

    # glasses_path = "D:/Project/utils/ps/1.png"
    # glasses = cv2.imread(glasses_path, cv2.IMREAD_UNCHANGED)
    # ret = luminosity(face, glasses, alpha=1)
    # cv2.imwrite("./ps/ret.png", ret)
