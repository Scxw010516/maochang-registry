import cv2
import numpy as np
from matplotlib import pyplot as plt


def contraction_feather(image, contraction_radius=1, feather_radius=3):
    mask = image[:, :, 3]
    # mask收缩1像素
    if contraction_radius > 3:
        mask = cv2.erode(
            mask,
            np.ones((contraction_radius, contraction_radius), np.uint8),
            iterations=1,
        )
    # 高斯模糊
    mask = cv2.GaussianBlur(
        mask,
        ksize=(feather_radius, feather_radius),
        sigmaX=feather_radius,
        borderType=cv2.BORDER_DEFAULT,
    )
    ret = image.copy()
    ret[:, :, 3] = mask

    return ret


# def bgr2


def shadow_light(foreground, dst=None, radius=100, alpha=1):
    frame = foreground[:, :, 3]

    frame_contours, frame_hiarachy = cv2.findContours(
        frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )
    # frame_contour = sorted(frame_contours, key=cv2.contourArea, reverse=True)[0]

    blank = np.zeros_like(foreground)
    opacue = np.linspace(0, 255, radius) * alpha

    for i in range(radius):
        cv2.drawContours(
            blank, frame_contours, -1, (0, 0, 0, int(opacue[i])), radius - i
        )
    if dst is not None:
        blank[frame == 255] = dst[frame == 255]
    else:
        blank[frame == 255] = foreground[frame == 255]

    return blank


def gradation_inverse(image):
    # image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    # 判断色相
    mask = image[:, :, 3]
    image_hsv = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2HSV)
    hue_channel = image_hsv[:, :, 0]
    hue_channel = hue_channel[mask != 0]
    hist = cv2.calcHist([hue_channel], [0], None, [180], [0, 180])
    max_val = np.argmax(hist)

    if 11 <= max_val <= 170:
        hue = 0  # 色相 橙色
    elif 0 <= max_val <= 10 or 156 < max_val <= 180:
        hue = 1  # 色相 红色
    else:
        hue = 2  # 色相 其他

    if hue == 0:
        b_channel = image[:, :, 0]
        channel = b_channel
    else:
        g_channel = image[:, :, 1]
        channel = g_channel

    channel[mask == 0] = 255

    channel = gray_rescale(channel, 0, 172)
    channel = 255 - channel
    channel = gray_binary_rescale(channel, 0.83)

    return channel


def gray_rescale(
    image,
    min_gray=0,
    max_gray=255,
):
    # 灰度值缩放
    lut = np.linspace(0, 255, max_gray - min_gray + 1).astype(np.float32)
    lut = np.concatenate([[0] * min_gray, lut, [255] * (255 - max_gray)]).astype(
        np.uint8
    )

    rescaled_image = cv2.LUT(image, lut)
    return rescaled_image


def gray_binary_rescale(image, ratio=1):
    # 黑白部分灰度按照 (0,128/ratio),(128/ratio,255)各自重新分配
    new_gray = int(128 / ratio)
    lut_black = lut = np.linspace(0, new_gray, 128).astype(np.float32)
    lut_white = np.linspace(new_gray, 255, 128).astype(np.float32)
    lut = np.concatenate([lut_black, lut_white]).astype(np.uint8)
    rescaled_image = cv2.LUT(image, lut)
    return rescaled_image


def illumi_adjust(image, alpha):
    img = image[:, :, :3]
    mask = image[:, :, 3]

    if alpha > 0:
        img = img * (1 - alpha) + alpha * 255.0
    else:
        img = img * (1 + alpha)
    img = np.clip(img, 0, 255).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = mask

    return img


def saturation_adjust(image, increment):
    mask = image[:, :, 3]
    image_bgr = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(image_hsv)

    alpha = np.clip(increment, 0.0, 1.0)
    s = np.clip(s * alpha, 0, 255).astype(np.uint8)

    image_hsv = cv2.merge([h, s, v])

    img = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = mask

    return np.array(img, dtype=np.uint8)


def levels_adjust(img, shadow, midtones, highlight, out_shadow, out_highlight, dim):
    # print(img)
    # dim = 3的时候调节RGB三个分量， 0调节B，1调节G，2调节R
    if dim == 3:
        mask_shadow = img < shadow
        img[mask_shadow] = shadow
        mask_Highlight = img > highlight
        img[mask_Highlight] = highlight
    else:
        mask_shadow = img[..., dim] < shadow
        img[mask_shadow] = shadow
        mask_Highlight = img[..., dim] > highlight
        img[mask_Highlight] = highlight

    if dim == 3:
        diff = highlight - shadow
        rgbDiff = img - shadow
        clRgb = np.power(rgbDiff / diff, 1 / midtones)
        outClRgb = clRgb * (out_highlight - out_shadow) / 255 + out_shadow
        data = np.array(outClRgb * 255, dtype="uint8")
        img = data
    else:
        diff = highlight - shadow
        rgbDiff = img[..., dim] - shadow
        clRgb = np.power(rgbDiff / diff, 1 / midtones)
        outClRgb = clRgb * (out_highlight - out_shadow) / 255 + out_shadow
        data = np.array(outClRgb * 255, dtype="uint8")
        img[..., dim] = data
    return img


# 亮度调整
def brightness_adjust(image, auto=True, alpha=1, base=128):
    # alpha = 1.2
    # beta = 50
    image_bgr = image[:, :, :3]
    mask = image[:, :, 3]
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    p = [-0.22555285, 0.26273859, 1.00457412]
    v = image_hsv[:, :, 2]
    if auto:
        v_mean = np.mean(v[mask != 0])
        ratio = v_mean / base
        alpha = p[0] * ratio**2 + p[1] * ratio + p[2]
        if alpha < 0.6:
            alpha = 0.6
        elif alpha > 1.1:
            alpha = 1.1
    v = np.clip(v * alpha, 0, 255).astype(np.uint8)

    image_hsv[:, :, 2] = v
    img = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = mask

    return img


def transparency_adjust(image, ratio=0.6):
    assert image.shape[2] == 4, "image must be in 4-channel"
    temp = image.astype(np.float32)
    temp[:, :, 3] *= ratio
    return temp.astype(np.uint8)


def get_nose_region(image, margin_ratio=0.1):
    mask = image[:, :, 3]
    contours, hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    frame_contour = contours[0]
    lens_contours = contours[1:3]
    lens_contours = sorted(lens_contours, key=lambda x: cv2.boundingRect(x)[0])
    lens_left_contour, lens_right_contour = lens_contours
    bounding_rect_left = cv2.boundingRect(lens_left_contour)
    bounding_rect_right = cv2.boundingRect(lens_right_contour)

    left = bounding_rect_left[0] + int(bounding_rect_left[2] * (1 - margin_ratio))
    right = bounding_rect_right[0] + int(bounding_rect_right[2] * margin_ratio)
    mid = int((left + right) / 2)
    # print(mid)
    # print(np.nonzero(mask[:, mid]))
    tops = [np.nonzero(mask[:, i])[0][-1] for i in range(mid - 10, mid + 10)]
    # print(tops)
    top = int(np.mean(tops))

    x, y, w, h = left, top, right - left, mask.shape[0] - top
    return x, y, w, h


def get_nose_opaque(layer_opaque, nose_region, transparent_threshold=20):
    ret = layer_opaque.copy()
    nose_opaque = layer_opaque[
        nose_region[1] :, nose_region[0] : nose_region[0] + nose_region[2]
    ]
    nose_opaque[nose_opaque < transparent_threshold] = 0
    ret = np.clip(ret, 1, 255).astype(np.uint8)
    ret[nose_region[1] :, nose_region[0] : nose_region[0] + nose_region[2]] = (
        nose_opaque
    )

    return ret


def main():
    image = cv2.imread(
        "./images/foreground/201300053024730500_1.png", cv2.IMREAD_UNCHANGED
    )
    # gray = np.array([[255, 215, 175], [135, 95, 55], [15, 5, 0]]).astype("uint8")

    # gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # lut = gray_rescale(gray, 0, 172)
    # # print(lut)
    # rescaled_image = gray_rescale(gray, 0, 172)
    # print(rescaled_image)

    # cv2.namedWindow("Original Gray Image", cv2.WINDOW_NORMAL)
    # cv2.namedWindow("Rescaled Gray Image", cv2.WINDOW_NORMAL)
    # # 显示原图和缩放后的图像
    # cv2.imshow("Original Gray Image", cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    # cv2.imshow("Rescaled Gray Image", rescaled_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print(128 // 0.83)
    gradation_inverse(image)


if __name__ == "__main__":
    main()
    # image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    # image[:, :, 0] = 180 - image[:, :, 0]
