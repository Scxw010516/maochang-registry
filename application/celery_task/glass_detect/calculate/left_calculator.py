from typing import Union

import cv2
import numpy as np

from .utils import (
    show_point,
    get_angle,
    rotate_image,
    rotate_point,
    euclidean_distance,
    add,
)


class LeftCalculator:
    def __init__(self, keypoints, is_balance: bool = True):

        self.vertical_angle = None
        self.forward_angle = None
        self.temple_angle = None
        self.drop_length = None
        self.head_point = None
        self.down_point = None
        self.turning_point = None
        self.tail_point = None
        self.keypoints = keypoints

        self.rotate_angle = None
        self.is_balance = is_balance
        self.get_points()
        if is_balance:
            self.balance_points()

    def get_points(self) -> dict:
        self.head_point = self.get_head_point()
        self.down_point = self.get_down_points()
        self.turning_point = self.get_turning_point()
        self.tail_point = self.get_tail_point()

        # 返回上述参数
        return {
            "head_point": self.head_point,
            "down_point": self.down_point,
            "turning_point": self.turning_point,
            "tail_point": self.tail_point,
        }

    def get_parameters(self) -> dict:
        self.vertical_angle = self.get_vertical_angle()
        self.forward_angle = self.get_forward_angle()
        self.temple_angle = self.get_temple_angle()
        self.drop_length = self.get_drop_length()
        return {
            "vertical_angle": self.vertical_angle,
            "forward_angle": self.forward_angle,
            "temple_angle": self.temple_angle,
            "drop_length": self.drop_length,
        }

    def balance_points(self):
        head_point = self.head_point
        turning_point = self.turning_point
        self.rotate_angle = get_angle(head_point, turning_point)
        for i in range(4):
            self.keypoints[i] = rotate_point(
                self.keypoints[i], head_point, -self.rotate_angle
            )
        self.get_points()

    def get_rotated_image(
        self,
        image: np.ndarray,
        crop_region: Union[tuple, list] = (1500, 3450, 600, 4500),
    ):
        if not self.is_balance or not self.rotate_angle:
            return image
        rotated_image = rotate_image(
            image,
            angle=self.rotate_angle,
            point=add(self.head_point, [crop_region[0], crop_region[2]]),
        )
        return rotated_image[
            crop_region[0] : crop_region[1], crop_region[2] : crop_region[3]
        ]

    def get_head_point(self):
        return self.keypoints[0]

    def get_down_points(self):
        return self.keypoints[1]

    def get_turning_point(self):
        return self.keypoints[2]

    def get_tail_point(self):
        return self.keypoints[3]

    def get_vertical_angle(self):
        vertical_angle = get_angle(self.turning_point, self.tail_point)
        return vertical_angle / np.pi * 180

    def get_forward_angle(self):
        forward_angle = get_angle(self.head_point, self.down_point)
        return 90 - (forward_angle / np.pi * 180)

    def get_temple_angle(self):
        temple_angle = get_angle(self.head_point, self.down_point)
        return temple_angle / np.pi * 180

    def get_drop_length(self):
        return euclidean_distance(self.turning_point, self.tail_point)


def main():
    image = cv2.imread("201300053024730270_2.jpg")
    keypoints = [
        [414, 733],
        [618, 1275],
        [2782, 891],
        [3204, 1315],
    ]
    lc = LeftCalculator(keypoints, painted_image=image)
    points = lc.get_points()
    print(points)
    points_only = [
        points["head_point"],
        points["turning_point"],
        points["down_point"],
        points["tail_point"],
    ]
    cv2.imwrite("201300053024730270_2_painted.jpg", lc.painted_image)
    show_point(lc.painted_image, points_only)
    params = lc.get_parameters()
    print(params)
    # print(params)


if __name__ == "__main__":
    main()
