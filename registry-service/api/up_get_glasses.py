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

    th = cv2.dilate(th, kernel=np.ones((3, 3)), iterations=10)
    th = cv2.erode(th, kernel=np.ones((3, 3)), iterations=10)

    th = remove_small(th, 30000)
    th = fill_small(th, 200000)

    return th


def get_piles(image: IMAGE) -> Sequence[List]:
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    rect = cv2.boundingRect(contour)
    x, y, w, h = rect
    margin = 2000

    glasses_up = image[y : y + h // 2, x : x + w]
    glasses_down = image[y + h // 2 : y + h, x : x + w]

    up_left = get_top_point(glasses_up.T)[::-1]
    up_right = [get_first_no_zero(glasses_up[h // 2 - 1, :]), h // 2 - 1]

    angle = get_angle(up_left, up_right)
    glasses_up_rotated = rotate_image(
        cv2.copyMakeBorder(
            glasses_up, margin, margin, margin, margin, cv2.BORDER_CONSTANT
        ),
        angle,
        [i + margin for i in up_left],
    )

    up_pile_rotated = get_top_point(glasses_up_rotated)
    up_pile = rotate_point(up_pile_rotated, [i + margin for i in up_left], angle)
    up_pile = [i - margin for i in up_pile]
    up_pile[0] += x
    up_pile[1] += y

    down_left = get_top_point(glasses_down.T)[::-1]
    down_right = [get_first_no_zero(glasses_down[0, :]), 0]

    angle = get_angle(down_left, down_right)
    glasses_down_rotated = rotate_image(
        cv2.copyMakeBorder(
            glasses_down, margin, margin, margin, margin, cv2.BORDER_CONSTANT
        ),
        angle,
        [i + margin for i in down_left],
    )

    down_pile_rotated = get_top_point(glasses_down_rotated[::-1])
    down_pile_rotated[1] = glasses_down_rotated.shape[0] - down_pile_rotated[1]

    down_pile = rotate_point(down_pile_rotated, [i + margin for i in down_left], angle)
    down_pile = [i - margin for i in down_pile]
    down_pile[0] += x
    down_pile[1] += y + h // 2

    return [up_pile, down_pile]

