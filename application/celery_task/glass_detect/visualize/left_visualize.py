import cv2

from .size_visualize import SizeVisualizer
from typing import List, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .utils import format_points
from .draw import draw_parameter, draw_angle, draw_outer_angle


class LeftVisualizer(SizeVisualizer):
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
        self.radius = kwargs.get("radius", 100)
        self.length = kwargs.get("length", 200)
        font_size = kwargs.get("font_size", 50)
        self.font = ImageFont.load_default(size=font_size)

    def visualize_parameters(self) -> np.ndarray:
        self.visualize_vertical_angle()
        self.visualize_forward_angle()
        self.visualize_temple_angle()
        self.visualize_drop_length()

        return np.array(cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR))

    def visualize_vertical_angle(self):
        assert (
            "turning_point" in self.points and "tail_point" in self.points
        ), "turning_point or tail_point not found"
        assert "vertical_angle" in self.parameters, "vertical_angle not found"

        vertex = self.points["turning_point"]
        start = [self.points["tail_point"][0], vertex[1]]
        end = self.points["tail_point"]
        draw_angle(
            self.draw,
            vertex,
            start,
            end,
            round(self.parameters["vertical_angle"], self.precision),
            color=self.color,
            length=self.length,
            radius=self.radius,
            width=self.width,
            font=self.font,
            offset=(200, 50),
        )

    def visualize_forward_angle(self):
        assert (
            "head_point" in self.points and "down_point" in self.points
        ), "head_point or down_point not found"
        assert "forward_angle" in self.parameters, "forward_angle not found"

        vertex = self.points["head_point"]
        start = self.points["down_point"]
        end = [vertex[0], start[1]]
        draw_outer_angle(
            self.draw,
            vertex,
            start,
            end,
            round(self.parameters["forward_angle"], self.precision),
            color=self.color,
            length=self.length,
            radius=150,
            width=self.width,
            font=self.font,
            offset=(60, -10),
        )

    def visualize_temple_angle(self):
        assert (
            "head_point" in self.points and "down_point" in self.points
        ), "head_point or down_point not found"
        assert "temple_angle" in self.parameters, "temple_angle not found"
        vertex = self.points["head_point"]
        start = [self.points["down_point"][0], vertex[1]]
        end = self.points["down_point"]
        draw_angle(
            self.draw,
            vertex,
            start,
            end,
            round(self.parameters["temple_angle"], self.precision),
            color=self.color,
            length=self.length,
            radius=self.radius,
            width=self.width,
            font=self.font,
            offset=(200, 50),
        )

    def visualize_drop_length(self):
        assert (
            "turning_point" in self.points and "tail_point" in self.points
        ), "turning_point or tail_point not found"
        assert "drop_length" in self.parameters, "drop_length not found"

        point1, point2 = self.points["turning_point"], self.points["tail_point"]
        draw_parameter(
            self.draw,
            point1,
            point2,
            round(self.parameters["drop_length"], self.precision),
            color=(255, 0, 0),
            dimension_mode=3,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(-20, 0),
        )


if __name__ == "__main__":
    points = {
        "head_point": (414, 733),
        "down_point": (653, 1260),
        "turning_point": (2787, 733),
        "tail_point": (3236, 1127),
    }
    parameters = {
        "vertical_angle": 41.26713172796637,
        "forward_angle": 24.394787933635072,
        "temple_angle": 65.60521206636493,
        "drop_length": 597.3583514106085,
    }

    image = cv2.imread("201300053024730270_2_painted.jpg")
    fv = LeftVisualizer(
        image=image,
        points=points,
        parameters=parameters,
    )
    fv.visualize_parameters()
