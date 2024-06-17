from .utils import *


def get_bridge(image: IMAGE, piles: Sequence[List], rect: Sequence[int]) -> List:
    x, w = rect[0], rect[2]
    y = piles[0][1]
    h = piles[1][1] - y

    scope = 0.01
    crop = image[
        y + int(h * (0.5 - scope)) : y + int(h * (0.5 + scope)),
        x + int(w * 0.5) : x + w,
    ]

    indices = np.argmax(crop, axis=1)
    bridge_x = int(np.mean(indices)) + x + int(w * 0.5)
    bridge_y = y + h // 2

    return [bridge_x, bridge_y]


def get_turning(image: IMAGE):
    margin = 1000
    image = cv2.copyMakeBorder(
        image, margin, margin, margin, margin, cv2.BORDER_CONSTANT
    )
    height, width = image.shape[:2]
    left = get_top_point(image.T)[::-1]
    # left[1] = height - left[1]
    right = [width - 1 - margin, get_first_no_zero(image[:, width - 1 - margin][::-1])]
    right[1] = height - right[1]

    angle = get_angle(left, right)
    image_rotated = rotate_image(image, angle, left)
    top_point_rotated = get_top_point(image_rotated)
    top_point = rotate_point(top_point_rotated, left, angle)
    top_point[0] -= margin
    top_point[1] -= margin

    return top_point


def get_parameters(image: IMAGE, piles: Sequence[List]) -> tuple[dict, dict]:
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    rect = cv2.boundingRect(contour)
    x, y, w, h = rect
    crop = image[y : y + h, x : x + w]

    # 鼻梁中心点
    bridge = get_bridge(image, piles, rect)

    # 正视标定距离
    distance_front = (bridge[0] + piles[0][0]) / 2

    face_angle_up = 90 - get_angle(bridge, piles[0]) * 180 / np.pi
    face_angle_down = 90 + get_angle(bridge, piles[1]) * 180 / np.pi
    # 面弯
    face_angle = face_angle_up + face_angle_down

    # 镜腿尾部弯折点
    turning_up = get_turning(crop[: h // 2, : int(w * 0.4)])
    turning_down = get_turning(crop[h // 2 :, : int(w * 0.4)][::-1])
    turning_up[0] += x
    turning_up[1] += y
    turning_down[0] += x
    turning_down[1] = h // 2 - turning_down[1]
    turning_down[1] += y + h // 2

    # 镜腿尾部点
    left_up = get_top_point(crop[: h // 2, : w // 2].T)[::-1]
    left_down = get_top_point(crop[h // 2 :, : w // 2].T)[::-1]
    left_up[0] += x
    left_up[1] += y
    left_down[0] += x
    left_down[1] += y + h // 2

    # 侧视标定距离
    distance_left = (y + left_up[1]) // 2

    # 垂内角
    sagittal_angle_up = -get_angle(left_up, turning_up) * 180 / np.pi
    sagittal_angle_down = get_angle(left_down, turning_down) * 180 / np.pi

    # 镜腿长度
    temple_length_up = piles[0][0] - left_up[0]
    temple_length_down = piles[1][0] - left_down[0]

    # 计算颞距的上下点
    temporal_up = [
        int(w * 0.7),
        get_first_no_zero(crop[: h // 2, int(w * 0.7) - 20 : int(w * 0.7) + 20][::-1]),
    ]
    temporal_down = [
        int(w * 0.7),
        get_first_no_zero(crop[h // 2 :, int(w * 0.7) - 20 : int(w * 0.7) + 20]),
    ]
    temporal_up[1] = h // 2 - temporal_up[1]
    temporal_up[0] += x
    temporal_up[1] += y
    temporal_down[0] += x
    temporal_down[1] += y + h // 2

    # 颞距
    temporal_width = temporal_down[1] - temporal_up[1]

    # 镜腿外张角
    spread_angle_up = get_angle(turning_up, piles[0]) * 180 / np.pi
    spread_angle_down = -get_angle(turning_down, piles[1]) * 180 / np.pi

    # 桩头距离
    pile_distance = abs(piles[1][1] - piles[0][1])

    return {
        "face_angle": face_angle,  # 面弯
        "sagittal_angle_left": sagittal_angle_up,  # 左垂内角
        "sagittal_angle_right": sagittal_angle_down,  # 右垂内角
        "temple_length_left": temple_length_up,  # 左镜腿长度
        "temple_length_right": temple_length_down,  # 右镜腿长度
        "temporal_width": temporal_width,  # 颞距
        "spread_angle_left": spread_angle_up,  # 左镜腿外张角
        "spread_angle_right": spread_angle_down,  # 右镜腿外张角
        "pile_distance": pile_distance,  # 桩头距离
    }, {"distance_left": distance_left, "distance_front": distance_front}
