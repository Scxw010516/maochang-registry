import cv2
import numpy as np

from .image_process import ImageProcessor, Image
from .utils import (
    get_contour_center,
    get_angle,
    rotate_image,
    cal_frame_size,
    cal_curvature,
    cal_shape_factor,
)


class DataCalculator(ImageProcessor):
    def __init__(
        self,
        frame_image: Image,
        lens_image: Image,
        front_points: dict,
        is_balance: bool = True,
    ):
        super().__init__()

        # points
        self.lens_center_points = front_points["lens_center_points"]
        self.lens_contours = None

        self.frame = frame_image
        self.lens = lens_image

        if is_balance:
            self.balance_image()

    def get_parameters(self, param: dict) -> dict:
        if self.lens_contours is None:
            self.lens_contours = self.get_lens_contours()
        self.get_points()
        # 镜框大小
        self.frame_size = cal_frame_size(param["frame_width"])
        # 曲率
        self.left_curvature = cal_curvature(
            self.lens_contours[0].reshape(-1, 2).astype(np.float32)
        )
        self.right_curvature = cal_curvature(
            self.lens_contours[1].reshape(-1, 2).astype(np.float32)
        )
        # 形状因子
        self.left_factors = cal_shape_factor(self.lens_contours[0])
        self.right_factors = cal_shape_factor(self.lens_contours[1])
        # 高宽比
        self.height_width_proportion = (
            abs(param["lens_height_left"] / param["lens_width_left"])
            + abs(param["lens_height_right"] / param["lens_width_right"])
        ) / 2

        return {
            "frame_size": self.frame_size,
            "left_curvature": self.left_curvature,
            "right_curvature": self.right_curvature,
            "left_factors": self.left_factors,
            "right_factors": self.right_factors,
            "height_width_proportion": self.height_width_proportion,
        }

    def balance_image(self):
        lens_center_points = self.lens_center_points.copy()
        rotate_angle = get_angle(lens_center_points[0], lens_center_points[1])
        # print(rotate_angle)
        self.frame = rotate_image(
            self.frame,
            angle=rotate_angle,
            point=lens_center_points[0],
        )
        self.lens = rotate_image(
            self.lens,
            angle=rotate_angle,
            point=lens_center_points[0],
        )

    def get_lens_contours(self):
        lens_contours, lens_hierarchy = cv2.findContours(
            self.lens, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        lens_contours = sorted(lens_contours, key=cv2.contourArea, reverse=True)[:2]
        lens_contours = sorted(lens_contours, key=lambda x: get_contour_center(x)[0])
        return lens_contours


def main():
    # sku = "201302423041213162_1"
    sku = "201300153005530209_1"
    frame_image = cv2.imread(f"../../mask/frame/{sku}.png", cv2.IMREAD_GRAYSCALE)
    lens_image = cv2.imread(f"../../mask/lens/{sku}.png", cv2.IMREAD_GRAYSCALE)
    frame_image *= 255
    lens_image *= 255
    front_points = {"lens_center_points": [(892, 876), (2362, 861)]}
    fp = DataCalculator(
        frame_image=frame_image,
        lens_image=lens_image,
        front_points=front_points,
        is_balance=True,
    )

    param = {
        "frame_width": 129,
        "lens_height_left": 44,
        "lens_width_left": 43.8,
        "lens_height_right": 55,
        "lens_width_right": 54,
    }
    data = fp.get_parameters(param)
    print(data)


if __name__ == "__main__":
    main()
# fp = FrontProcessor(frame_image=np.array([1,2,3]),lens_image=np.array([1,2,3]))
