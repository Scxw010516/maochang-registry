import cv2
import numpy as np
from typing import Tuple, List, Sequence, Union

from .image_calculator import ImageCalculator, Image
from .utils import (
    get_first_no_zero,
    get_first_no_zero_index,
    show_point,
    get_contour_center,
    get_angle,
    rotate_image,
    add,
    show_rect,
    euclidean_distance,
)


class FrontCalculator(ImageCalculator):
    def __init__(
        self,
        frame_image: Image,
        lens_image: Image,
        is_balance: bool = True,
    ):
        super().__init__()

        # parameters
        self.lens_side_points = None
        self.lens_bottom_points = None
        self.bottom_points = None
        self.frame_top_width = None
        self.lens_area_right = None
        self.lens_area_left = None
        self.lens_diagonal_right = None
        self.lens_diagonal_left = None
        self.lens_height_right = None
        self.lens_height_left = None
        self.frame_width = None
        self.frame_height = None
        self.pile_height_right = None
        self.pile_height_left = None
        self.bridge_width = None
        self.lens_width_right = None
        self.lens_width_left = None
        # points
        self.top_points = None
        self.lens_top_points = None
        self.lens_diagonal_points = None
        self.frame_bounding_points = None
        self.lens_bounding_points = None
        self.pile_points = None
        self.lens_center_points = None

        self.rotate_angle = None
        self.lens_contours = None

        self.frame = frame_image
        self.lens = lens_image
        self.is_balance = is_balance

        if is_balance:
            self.balance_image()

    def get_points(self) -> dict:
        self.frame_bounding_points = self.get_frame_bounding_points()
        self.pile_points = self.get_pile_points()
        self.lens_center_points = self.get_lens_center_points()
        self.lens_bounding_points = self.get_lens_bounding_points()
        self.lens_diagonal_points = self.get_lens_diagonal_points()
        self.lens_top_points = self.get_lens_top_points()
        self.top_points = self.get_top_points()
        self.bottom_points = self.get_bottom_points()
        self.lens_bottom_points = self.get_lens_bottom_points()
        self.lens_side_points = self.get_lens_side_points()

        # 返回上述参数
        return {
            "frame_bounding_points": self.frame_bounding_points,
            "pile_points": self.pile_points,
            "lens_center_points": self.lens_center_points,
            "lens_bounding_points": self.lens_bounding_points,
            "lens_diagonal_points": self.lens_diagonal_points,
            "lens_top_points": self.lens_top_points,
            "top_points": self.top_points,
            "bottom_points": self.bottom_points,
            "lens_bottom_points": self.lens_bottom_points,
            "lens_side_points": self.lens_side_points,
        }

    def get_parameters(self) -> dict:
        self.get_points()
        # 左镜片宽度
        self.lens_width_left = (
            self.lens_bounding_points[0][1][0] - self.lens_bounding_points[0][0][0]
        )
        # 右镜片宽度
        self.lens_width_right = (
            self.lens_bounding_points[1][1][0] - self.lens_bounding_points[1][0][0]
        )
        # 鼻梁宽度
        self.bridge_width = (
            self.lens_bounding_points[1][0][0] - self.lens_bounding_points[0][1][0]
        )
        # 左桩头高度
        self.pile_height_left = (
            self.frame_bounding_points[1][1] - self.pile_points[0][1]
        )
        # 右桩头高度
        self.pile_height_right = (
            self.frame_bounding_points[1][1] - self.pile_points[1][1]
        )
        # 镜框高度
        self.frame_height = (
            self.frame_bounding_points[1][1] - self.frame_bounding_points[0][1]
        )
        # 镜框宽度
        self.frame_width = (
            self.frame_bounding_points[1][0] - self.frame_bounding_points[0][0]
        )
        # 左镜圈高度
        self.lens_height_left = (
            self.lens_bounding_points[0][1][1] - self.lens_bounding_points[0][0][1]
        )
        # 右镜圈高度
        self.lens_height_right = (
            self.lens_bounding_points[1][1][1] - self.lens_bounding_points[1][0][1]
        )
        # 左对角线长度
        self.lens_diagonal_left = euclidean_distance(*self.lens_diagonal_points[0])
        # 右对角线长度
        self.lens_diagonal_right = euclidean_distance(*self.lens_diagonal_points[1])
        # 左镜圈面积
        self.lens_area_left = cv2.contourArea(self.lens_contours[0])
        # 右镜圈面积
        self.lens_area_right = cv2.contourArea(self.lens_contours[1])
        # 镜框上边厚度
        self.frame_top_width = (
            abs(self.top_points[0][1] - self.lens_top_points[0][1])
            + abs(self.top_points[1][1] - self.lens_top_points[1][1])
        ) / 2

        return {
            "lens_width_left": self.lens_width_left,
            "lens_width_right": self.lens_width_right,
            "bridge_width": self.bridge_width,
            "pile_height_left": self.pile_height_left,
            "pile_height_right": self.pile_height_right,
            "frame_height": self.frame_height,
            "frame_width": self.frame_width,
            "lens_height_left": self.lens_height_left,
            "lens_height_right": self.lens_height_right,
            "lens_diagonal_left": self.lens_diagonal_left,
            "lens_diagonal_right": self.lens_diagonal_right,
            "lens_area_left": self.lens_area_left,
            "lens_area_right": self.lens_area_right,
            "frame_top_width": self.frame_top_width,
        }

    def balance_image(self):
        if self.lens_center_points is None:
            self.lens_center_points = self.get_lens_center_points()
        lens_center_points = self.lens_center_points.copy()
        self.rotate_angle = get_angle(lens_center_points[0], lens_center_points[1])
        self.frame = rotate_image(
            self.frame,
            angle=self.rotate_angle,
            point=lens_center_points[0],
        )
        self.lens = rotate_image(
            self.lens,
            angle=self.rotate_angle,
            point=lens_center_points[0],
        )
        self.lens_center_points = self.get_lens_center_points()

    def get_rotated_image(
        self,
        image: np.ndarray,
        crop_region: Union[tuple, list] = (1350, 2950, 750, 3950),
    ):
        if not self.is_balance or not self.rotate_angle:
            return image
        rotated_image = rotate_image(
            image,
            angle=self.rotate_angle,
            point=add(self.lens_center_points[0], [crop_region[0], crop_region[2]]),
        )
        return rotated_image[
            crop_region[0] : crop_region[1], crop_region[2] : crop_region[3]
        ]

    def get_lens_contours(self):
        lens_contours, lens_hierarchy = cv2.findContours(
            self.lens, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        lens_contours = sorted(lens_contours, key=cv2.contourArea, reverse=True)[:2]
        lens_contours = sorted(lens_contours, key=lambda x: get_contour_center(x)[0])
        return lens_contours

    def get_frame_bounding_points(self) -> List[Sequence]:
        frame_bounding_rect = cv2.boundingRect(self.frame)
        frame_bounding_points = [
            frame_bounding_rect[:2],
            add(frame_bounding_rect[2:], frame_bounding_rect[:2]),
        ]
        return frame_bounding_points

    def get_lens_center_points(self) -> Sequence[Tuple]:
        if self.lens_contours is None:
            self.lens_contours = self.get_lens_contours()
        lens_contours = self.lens_contours.copy()

        lens_center_points = [get_contour_center(contour) for contour in lens_contours]
        # 左右排序
        lens_center_points = sorted(lens_center_points, key=lambda x: x[0])
        return lens_center_points

    def get_pile_points(self) -> List[Sequence]:
        # bounding rect
        frame_bounding_rect = cv2.boundingRect(self.frame)
        x, y, w, h = frame_bounding_rect

        frame_crop = self.frame[y : y + h, x : x + w]

        # 获取左右桩头点
        left_pile_point_y = get_first_no_zero_index(frame_crop[:, 1], axis=0)
        right_pile_point_y = get_first_no_zero_index(frame_crop[:, -1], axis=0)

        # 加上裁切高宽
        left_pile_point_y += y
        right_pile_point_y += y
        left_pile_point = (x, left_pile_point_y)
        right_pile_point = (x + w, right_pile_point_y)

        pile_points = [left_pile_point, right_pile_point]

        return pile_points

    def get_lens_bounding_points(self) -> List[Sequence]:
        lens_contours, lens_hierarchy = cv2.findContours(
            self.lens, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        lens_contours = sorted(lens_contours, key=cv2.contourArea, reverse=True)[:2]
        lens_bounding_rects = [cv2.boundingRect(contour) for contour in lens_contours]

        # 左右排序
        lens_bounding_rects = sorted(lens_bounding_rects, key=lambda x: x[0])
        # xywh -> xyxy
        lens_bounding_points = [
            [rect[:2], add(rect[2:], rect[:2])] for rect in lens_bounding_rects
        ]
        return lens_bounding_points

    def get_lens_diagonal_points(self) -> List[Sequence]:
        if self.lens_contours is None:
            self.get_lens_contours()
        lens_contours = self.lens_contours.copy()
        lens_contour_points = [cnt.reshape((-1, 2)) for cnt in lens_contours]

        if self.lens_center_points is None:
            self.lens_center_points = self.get_lens_center_points()
        lens_center_points = self.lens_center_points.copy()
        # 每个轮廓左半边点
        lens_contour_left_points = [
            [p for p in lens_contour_points[i] if p[0] < lens_center_points[i][0]]
            for i in range(2)
        ]
        # 每个轮廓右半边点
        lens_contour_right_points = [
            [p for p in lens_contour_points[i] if p[0] > lens_center_points[i][0]]
            for i in range(2)
        ]
        # 合并
        lens_contour_points = [
            lens_contour_left_points[0],
            lens_contour_right_points[0],
            lens_contour_left_points[1],
            lens_contour_right_points[1],
        ]
        if self.lens_bounding_points is None:
            self.lens_bounding_points = self.get_lens_bounding_points()
        lens_bounding_points = self.lens_bounding_points.copy()
        # 左镜圈对角线为 左上--右下
        lens_bounding_points[0] = [
            [lens_bounding_points[0][1][0], lens_bounding_points[0][0][1]],
            [lens_bounding_points[0][0][0], lens_bounding_points[0][1][1]],
        ]
        # print("lens_bounding_points", lens_bounding_points)
        # Ax + By + C = 0
        diagonal_lines = [
            [
                points[1][1] - points[0][1],
                -(points[1][0] - points[0][0]),
                points[1][0] * points[0][1] - points[0][0] * points[1][1],
            ]
            for points in lens_bounding_points
        ]
        # 计算距离
        distances = [
            [
                [
                    abs(
                        diagonal_lines[i // 2][0] * point[0]
                        + diagonal_lines[i // 2][1] * point[1]
                        + diagonal_lines[i // 2][2]
                    )
                    / np.sqrt(
                        diagonal_lines[i // 2][0] ** 2 + diagonal_lines[i // 2][1] ** 2
                    ),
                    j,
                ]
                for j, point in enumerate(lens_contour_points[i])
            ]
            for i in range(4)
        ]

        distances = [sorted(d, key=lambda x: x[0]) for d in distances]

        # for i in range(4):
        #     print(distances[i][0][1])
        lens_diagonal_points = [
            lens_contour_points[i][distances[i][0][1]] for i in range(4)
        ]
        lens_diagonal_points = [
            [lens_diagonal_points[0], lens_diagonal_points[1]],
            [lens_diagonal_points[2], lens_diagonal_points[3]],
        ]
        self.lens_diagonal_points = lens_diagonal_points
        return lens_diagonal_points

    # 不是严格的最上方点，而是横坐标位于镜片中心点上的最上方点
    def get_lens_top_points(self) -> List[Sequence]:
        if self.lens_center_points is None:
            self.lens_center_points = self.get_lens_center_points()
        lens_center_points = self.lens_center_points.copy()
        lens_top_points = [
            [
                lens_center_points[i][0],
                get_first_no_zero_index(self.lens[:, lens_center_points[i][0]]),
            ]
            for i in range(2)
        ]
        return lens_top_points

    # 不是严格的最下上方点，而是横坐标位于镜片中心点上的最上方点
    def get_top_points(self) -> List[Sequence]:
        if self.lens_center_points is None:
            self.lens_center_points = self.get_lens_center_points()
        lens_center_points = self.lens_center_points.copy()

        top_points = [
            [
                lens_center_points[i][0],
                get_first_no_zero_index(self.frame[:, lens_center_points[i][0]]),
            ]
            for i in range(2)
        ]

        return top_points

    # 不是严格的最下方点，而是横坐标位于镜片中心点下的最下方点
    def get_lens_bottom_points(self) -> List[Sequence]:
        if self.lens_center_points is None:
            self.lens_center_points = self.get_lens_center_points()
        lens_center_points = self.lens_center_points.copy()
        lens_bottom_points = [
            [
                lens_center_points[i][0],
                self.lens.shape[0]
                - get_first_no_zero_index(self.lens[:, lens_center_points[i][0]][::-1]),
            ]
            for i in range(2)
        ]
        return lens_bottom_points

    def get_bottom_points(self) -> List[Sequence]:
        if self.lens_center_points is None:
            self.lens_center_points = self.get_lens_center_points()
        lens_center_points = self.lens_center_points.copy()

        bottom_points = [
            [
                lens_center_points[i][0],
                self.frame.shape[0]
                - get_first_no_zero_index(
                    self.frame[:, lens_center_points[i][0]][::-1]
                ),
            ]
            for i in range(2)
        ]

        return bottom_points

    # 严格意义的最左侧点和最右侧点
    def get_lens_side_points(self):
        if self.lens_contours is None:
            self.lens_contours = self.get_lens_contours()
        lens_contours = self.lens_contours.copy()
        lens_contours_points = [cnt.reshape((-1, 2)) for cnt in lens_contours]
        lens_contours_points_sorted = [
            sorted(lens_contours_points[i], key=lambda x: x[0]) for i in range(2)
        ]
        lens_side_points = [
            [
                lens_contours_points_sorted[i][0],
                lens_contours_points_sorted[i][-1],
            ]
            for i in range(2)
        ]
        return lens_side_points


def main():
    # sku = "201302423041213162_1"
    sku = "201302423041213236_1"
    frame_image = cv2.imread(f"./images/frame/{sku}.png", cv2.IMREAD_GRAYSCALE)
    lens_image = cv2.imread(f"./images/lens/{sku}.png", cv2.IMREAD_GRAYSCALE)
    frame_image *= 255
    lens_image *= 255
    fp = FrontCalculator(
        frame_image=frame_image, lens_image=lens_image, is_balance=True
    )
    # fp.__init__(frame_image=frame_image, lens_image=lens_image, is_balance=True)
    # fp.get_points()
    points = fp.get_lens_top_points()
    show_point(frame_image, points)

    # show_point(lens_image, points[1])
    # show_point(lens_image, points[1])


if __name__ == "__main__":
    main()
# fp = FrontProcessor(frame_image=np.array([1,2,3]),lens_image=np.array([1,2,3]))
