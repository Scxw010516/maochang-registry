import cv2
import numpy as np
from typing import Tuple, List, Sequence, Union
from skimage.morphology import skeletonize

from .image_calculator import ImageCalculator, Image
from .utils import (
    get_first_no_zero,
    get_first_no_zero_index,
    show_point,
    get_contour_center,
    get_angle,
    get_intersection_angle,
    rotate_image,
    rotate_point,
    add,
    show_rect,
    euclidean_distance,
    show,
)


class UpCalculator(ImageCalculator):
    def __init__(self, keypoints, is_balance: bool = True):
        super().__init__()
        self.pile_distance = None
        self.spread_angle_left = None
        self.temporal_width = None
        self.spread_angle_right = None
        self.temple_length_right = None
        self.temple_length_left = None
        self.sagittal_angle_right = None
        self.sagittal_angle_left = None
        self.face_angle = None
        self.turning_points = None
        self.tail_points = None
        self.bridge_point = None
        self.temporal_points = None
        self.pile_points = None
        self.keypoints = keypoints

        self.rotate_angle = None
        self.is_balance = is_balance
        self.get_points()
        if is_balance:
            self.balance_points()

    def get_points(self) -> dict:
        self.pile_points = self.get_pile_points()
        self.temporal_points = self.get_temporal_points()
        self.turning_points = self.get_turning_points()
        self.tail_points = self.get_tail_points()
        self.bridge_point = self.get_bridge_point()

        # 返回上述参数
        return {
            "pile_points": self.pile_points,
            "temporal_points": self.temporal_points,
            "turning_points": self.turning_points,
            "tail_points": self.tail_points,
            "bridge_point": self.bridge_point,
        }

    def get_parameters(self) -> dict:
        # self.get_points()

        self.face_angle = np.degrees(
            get_intersection_angle(
                self.pile_points[0], self.bridge_point, self.pile_points[1]
            )
        )
        self.sagittal_angle_left = 180 - np.degrees(
            get_intersection_angle(
                self.tail_points[0], self.turning_points[0], self.temporal_points[0]
            )
        )
        self.sagittal_angle_right = 180 - np.degrees(
            get_intersection_angle(
                self.tail_points[1], self.turning_points[1], self.temporal_points[1]
            )
        )
        self.temple_length_left = euclidean_distance(
            self.tail_points[0], self.pile_points[0]
        )
        self.temple_length_right = euclidean_distance(
            self.tail_points[1], self.pile_points[1]
        )
        self.temporal_width = euclidean_distance(
            self.temporal_points[0], self.temporal_points[1]
        )
        self.spread_angle_left = np.degrees(
            get_intersection_angle(
                self.temporal_points[0], self.pile_points[0], self.bridge_point
            )
        )
        self.spread_angle_right = np.degrees(
            get_intersection_angle(
                self.temporal_points[1], self.pile_points[1], self.bridge_point
            )
        )
        self.pile_distance = euclidean_distance(
            self.pile_points[0], self.pile_points[1]
        )
        return {
            "face_angle": self.face_angle,
            "sagittal_angle_left": self.sagittal_angle_left,
            "sagittal_angle_right": self.sagittal_angle_right,
            "temple_length_left": self.temple_length_left,
            "temple_length_right": self.temple_length_right,
            "temporal_width": self.temporal_width,
            "spread_angle_left": self.spread_angle_left,
            "spread_angle_right": self.spread_angle_right,
            "pile_distance": self.pile_distance,
        }

    def balance_points(self):
        pile_points = (
            self.pile_points if self.pile_points is not None else self.get_pile_points()
        )

        self.rotate_angle = get_angle(pile_points[0], pile_points[1])

        for i in range(9):
            self.keypoints[i] = rotate_point(
                self.keypoints[i], pile_points[0], (np.pi / 2 - self.rotate_angle)
            )
        self.get_points()

    def get_rotated_image(
        self, image: np.ndarray, crop_region: Union[tuple, list] = (0, -1, 0, -1)
    ):
        if not self.is_balance or not self.rotate_angle:
            return image
        rotated_image = rotate_image(
            image,
            angle=-(np.pi / 2 - self.rotate_angle),
            point=add(self.pile_points[0], [crop_region[0], crop_region[2]]),
        )
        return rotated_image[
            crop_region[0] : crop_region[1], crop_region[2] : crop_region[3]
        ]

    def get_pile_points(self):
        pile_points = [self.keypoints[6], self.keypoints[7]]

        return pile_points

    def get_temporal_points(self):
        temporal_points = [self.keypoints[4], self.keypoints[5]]

        return temporal_points

    def get_turning_points(self):
        turning_points = [self.keypoints[2], self.keypoints[3]]

        return turning_points

    def get_tail_points(self):
        tail_points = [self.keypoints[0], self.keypoints[1]]

        return tail_points

    def get_bridge_point(self):
        bridge_point = self.keypoints[8]

        return bridge_point


def main():
    image = cv2.imread("./images/up/201300063039330109_0.png")
    keypoints = [
        [1309, 1126],
        [1340, 2384],
        [1541, 864],
        [1585, 2646],
        [2467, 693],
        [2510, 2729],
        [3039, 658],
        [3078, 2733],
        [3231, 1694],
    ]
    up = UpCalculator(keypoints)
    params = up.get_parameters()
    print(params)


if __name__ == "__main__":
    main()
