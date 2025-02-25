import cv2

from .size_visualize import SizeVisualizer

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .utils import format_points
from .draw import draw_parameter, draw_outer_parameter


class FrontVisualizer(SizeVisualizer):
    def __init__(self, image: np.ndarray, points, parameters, **kwargs):
        super().__init__(image, points, parameters)
        self.image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        self.draw = ImageDraw.Draw(self.image)
        self.points = points
        self.parameters = parameters
        self.width = kwargs.get("width", 5)

        self.color = kwargs.get("color", (255, 0, 0))
        self.dimension_length = kwargs.get("dimension_length", 200)
        self.precision = kwargs.get("precision", 1)

        font_size = kwargs.get("font_size", 50)
        self.font = ImageFont.load_default(size=font_size)

    def visualize_parameters(self) -> np.ndarray:
        self.visualize_lens_width()
        self.visualize_lens_height()
        self.visualize_pile_height()
        self.visualize_frame_width()
        self.visualize_frame_top_width()
        self.visualize_frame_height()
        self.visualize_bridge_width()
        self.visualize_lens_diagonal()

        return np.array(cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR))

    def visualize_lens_width(self):
        assert "lens_side_points" in self.points, "lens_side_points not found"
        assert (
            "lens_width_left" in self.parameters
            and "lens_width_right" in self.parameters
        ), "lens_width_left or lens_width_right not found"
        # visualize lens_width_left
        lens_side_points_left = self.points["lens_side_points"][0]
        lens_width = (
            self.parameters["lens_width_left"] + self.parameters["lens_width_right"]
        ) / 2
        point1, point2 = format_points(lens_side_points_left, 1)
        draw_parameter(
            self.draw,
            point1,
            point2,
            round(lens_width, self.precision),
            color=(255, 0, 0),
            dimension_mode=1,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(-150, -50),
        )

    def visualize_lens_height(self):
        assert (
            "lens_top_points" in self.points and "lens_bottom_points" in self.points
        ), "lens_top_points or lens_bottom_points not found"
        assert (
            "lens_height_left" in self.parameters
            and "lens_height_right" in self.parameters
        ), "lens_height_left or lens_height_right not found"
        # visualize lens_height_left
        lens_top_point_left = self.points["lens_top_points"][0]
        lens_bottom_point_left = self.points["lens_bottom_points"][0]
        lens_height = (
            self.parameters["lens_height_left"] + self.parameters["lens_height_right"]
        ) / 2
        point1, point2 = format_points([lens_top_point_left, lens_bottom_point_left], 0)
        draw_parameter(
            self.draw,
            point1,
            point2,
            round(lens_height, self.precision),
            color=(255, 0, 0),
            dimension_mode=2,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(50, 0),
        )

    def visualize_pile_height(self):
        assert (
            "pile_points" in self.points and "bottom_points" in self.points
        ), "pile_points or bottom_points not found"
        assert (
            "pile_height_left" in self.parameters
            and "pile_height_right" in self.parameters
        ), "pile_height_left or pile_height_right not found"

        # visualize pile_height_left
        pile_point_left = self.points["pile_points"][0]
        bottom_point_left = self.points["bottom_points"][0]
        pile_height = (
            self.parameters["pile_height_left"] + self.parameters["pile_height_right"]
        ) / 2
        point1, point2 = format_points([pile_point_left, bottom_point_left], 0)
        draw_parameter(
            self.draw,
            point1,
            point2,
            round(pile_height, self.precision),
            color=(255, 0, 0),
            dimension_mode=2,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(50, 0),
        )

    def visualize_frame_height(self):
        assert (
            "top_points" in self.points and "bottom_points" in self.points
        ), "top_points or bottom_points not found"
        assert "frame_height" in self.parameters, "frame_height not found"

        # visualize frame_height_right
        top_point_right = self.points["top_points"][1]
        bottom_point_right = self.points["bottom_points"][1]
        point1, point2 = format_points([top_point_right, bottom_point_right], 0)
        draw_parameter(
            self.draw,
            point1,
            point2,
            round(self.parameters["frame_height"], self.precision),
            color=(255, 0, 0),
            dimension_mode=2,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(50, -30),
        )

    def visualize_frame_width(self):
        assert "pile_points" in self.points, "pile_points not found"
        assert "frame_width" in self.parameters, "frame_width not found"
        point1, point2 = format_points(self.points["pile_points"], 1)
        draw_parameter(
            self.draw,
            point1,
            point2,
            round(self.parameters["frame_width"], self.precision),
            color=(255, 0, 0),
            dimension_mode=1,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(0, -50),
        )

    def visualize_bridge_width(self):
        assert "lens_side_points" in self.points, "lens_side_points not found"
        assert "bridge_width" in self.parameters, "bridge_width not found"
        lens_side_points_left_right = self.points["lens_side_points"][0][1]
        lens_side_points_right_left = self.points["lens_side_points"][1][0]

        point1, point2 = format_points(
            [lens_side_points_left_right, lens_side_points_right_left], 1
        )
        draw_parameter(
            self.draw,
            point1,
            point2,
            round(self.parameters["bridge_width"], self.precision),
            color=(255, 0, 0),
            dimension_mode=1,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(0, -50),
        )

    def visualize_lens_diagonal(self):
        assert "lens_diagonal_points" in self.points, "lens_diagonal_points not found"
        assert "lens_diagonal_right" in self.parameters, "lens_diagonal_right not found"

        # visualize lens_diagonal_right
        point1, point2 = self.points["lens_diagonal_points"][1]
        lens_diagonal_right = round(self.parameters["lens_diagonal_right"], 1)

        draw_parameter(
            self.draw,
            point1,
            point2,
            round(lens_diagonal_right, self.precision),
            color=(255, 0, 0),
            dimension_mode=3,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(-70, -30),
        )

    def visualize_frame_top_width(self):
        assert (
            "top_points" in self.points and "lens_top_points" in self.points
        ), "top_points or lens_top_points not found"
        assert "frame_top_width" in self.parameters, "frame_top_width not found"
        top_points_left = self.points["top_points"][0]
        lens_top_point_left = self.points["lens_top_points"][0]
        point1, point2 = format_points([top_points_left, lens_top_point_left], 0)
        draw_outer_parameter(
            self.draw,
            point1,
            point2,
            round(self.parameters["frame_top_width"], self.precision),
            color=(255, 0, 0),
            dimension_mode=2,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(60, -10),
        )


if __name__ == "__main__":
    parameters = {
        "lens_width_left": 1043,
        "lens_width_right": 1035,
        "bridge_width": 370,
        "pile_height_left": 824,
        "pile_height_right": 806,
        "frame_height": 922,
        "frame_width": 2918,
        "lens_height_left": 783,
        "lens_height_right": 781,
        "lens_diagonal_left": 1051.400019022256,
        "lens_diagonal_right": 1043.2032400256433,
        "lens_area_left": 686661.0,
        "lens_area_right": 679765.5,
        "frame_top_width": 80.5,
    }
    points = {
        "frame_bounding_points": [(161, 336), [3079, 1258]],
        "pile_points": [(161, 434), (3079, 452)],
        "lens_center_points": [(900, 793), (2346, 784)],
        "lens_bounding_points": [
            [(397, 418), [1440, 1201]],
            [(1810, 418), [2845, 1199]],
        ],
        "lens_diagonal_points": [
            [[506, 1119], [1347, 488]],
            [[1899, 486], [2732, 1114]],
        ],
        "lens_top_points": [[900, 418], [2346, 418]],
        "top_points": [[900, 336], [2346, 339]],
        "bottom_points": [[900, 1257], [2346, 1257]],
        "lens_bottom_points": [[900, 1200], [2346, 1198]],
        "lens_side_points": [[[397, 672], [1438, 614]], [[1809, 616], [2844, 730]]],
    }
    image = cv2.imread("201302723049010121_1.png")
    fv = FrontVisualizer(
        image=image,
        points=points,
        parameters=parameters,
    )
    fv.visualize_parameters()
