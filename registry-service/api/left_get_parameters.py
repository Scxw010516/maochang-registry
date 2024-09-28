from .utils import *


def get_turning(image: IMAGE) -> List:
    margin = 1000
    image = cv2.copyMakeBorder(
        image, margin, margin, margin, margin, cv2.BORDER_CONSTANT
    )
    height, width = image.shape[:2]

    down_left = [margin, height - get_first_no_zero(image[:, margin][::-1])]
    down_right = get_top_point(image[::-1])
    down_right[1] = height - down_right[1]

    angle = get_angle(down_left, down_right)

    rotated_image = rotate_image(image, angle, down_left)
    top_rotated_point = get_top_point(rotated_image)
    top_point = rotate_point(top_rotated_point, down_left, angle)

    top_point[0] -= margin
    top_point[1] -= margin

    return top_point


def get_parameters(image: IMAGE) -> dict:
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    rect = cv2.boundingRect(contour)
    x, y, w, h = rect
    crop = image[y : y + h, x : x + w]

    turning_point = get_turning(
        crop[
            :,
            int(w * 0.3) :,
        ]
    )  # 镜腿尾部转折点
    turning_point[0] += int(w * 0.3)  # 加上前面去掉的x坐标
    right = [w - 1, get_first_no_zero(crop[:, w - 1])]  # 镜腿尾部点
    # print(turning_point, right)

    # 垂俯角
    vertical_angle = get_angle(turning_point, right) * 180 / np.pi

    # 垂长
    drop_length = (
        (turning_point[0] - right[0]) ** 2 + (turning_point[1] - right[1]) ** 2
    ) ** 0.5

    # 镜腿上面部分
    crop_up = crop[: turning_point[1] - 50, :]
    # 镜腿上边部分最左侧点
    left_up = get_top_point(crop_up.T)[::-1]
    # 镜框最下点
    left_down = get_top_point(crop[:, : int(w * 0.5)][::-1])
    left_down[1] = h - left_down[1]

    # 镜腿角
    temple_angle = get_angle(left_up, left_down) * 180 / np.pi
    # 前倾角
    forward_angle = 90 - temple_angle

    return {
        "vertical_angle": vertical_angle,  # 垂俯角
        "forward_angle": forward_angle,  # 前倾角
        "temple_angle": temple_angle,  # 镜腿角
        "drop_length": drop_length,  # 垂长
    }
