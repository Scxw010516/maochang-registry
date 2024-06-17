from .utils import *


def get_glasses(image: IMAGE, background: IMAGE, thresholds: Sequence[int] = (20,30)) -> IMAGE:
    gray_glasses = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    gray_background = gaussian_blur(gray_background, 5)
    gray_glasses = gaussian_blur(gray_glasses, 5)

    gray_background = gray_background.astype(np.int32)
    gray_glasses = gray_glasses.astype(np.int32)

    gray_subtraction = gray_glasses - gray_background
    gray_subtraction[np.abs(gray_subtraction) < thresholds[0]] = 255

    gray_subtraction = (255 - gray_subtraction).astype(np.uint8)

    _, th = cv2.threshold(gray_subtraction, thresholds[1], 255, cv2.THRESH_BINARY)

    # th = cv2.erode(th, kernel=np.ones((3, 3)), iterations=20)
    # th = cv2.dilate(th, kernel=np.ones((3, 3)), iterations=20)

    th = remove_small(th, 10000)
    th = fill_small(th, 50000)

    return th


def rotate_glasses_left(image: IMAGE) -> IMAGE:
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    rect = cv2.boundingRect(contour)

    crop = image[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2]]

    point1 = [
        int(rect[2] * 0.3),
        get_first_no_zero(crop[:, int(rect[2] * 0.3) - 25 : int(rect[2] * 0.3) + 25]),
    ]
    point2 = [
        int(rect[2] * 0.5),
        get_first_no_zero(crop[:, int(rect[2] * 0.5) - 25 : int(rect[2] * 0.5) + 25]),
    ]
    angle = get_angle(point1, point2)

    img = rotate_image(image, angle, (point1[0] + rect[0], point1[1] + rect[1]))

    point3 = rotate_point(point2, point1, -angle)
    point3[0] += rect[0]
    point3[1] += rect[1]
    point1[0] += rect[0]
    point1[1] += rect[1]
    # res = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # cv2.circle(res, point1, 20, (0, 0, 255), -1)
    # cv2.circle(res, point3, 20, (0, 0, 255), -1)
    # show(res)
    return img
