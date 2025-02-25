import cv2

from .size_visualize import SizeVisualizer
from typing import List, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .utils import format_points
from .draw import draw_parameter, draw_angle


class UpVisualizer(SizeVisualizer):
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
        self.visualize_face_angle()
        self.visualize_left_sagittal_angle()
        self.visualize_right_sagittal_angle()
        self.visualize_temple_length()
        self.visualize_temporal_width()
        self.visualize_left_spread_angle()
        self.visualize_right_spread_angle()
        self.visualize_pile_distance()

        return np.array(cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR))
        # if save_path is not None:
        #     self.image.save("up_visualize.png")

    def visualize_face_angle(self):
        assert (
            "bridge_point" in self.points and "pile_points" in self.points
        ), "bridge_point or pile_points not found"
        assert "face_angle" in self.parameters, "face_angle not found"

        vertex = self.points["bridge_point"]
        start = self.points["pile_points"][1]
        end = self.points["pile_points"][0]
        draw_angle(
            self.draw,
            vertex,
            start,
            end,
            round(self.parameters["face_angle"], self.precision),
            color=self.color,
            length=self.length,
            radius=self.radius,
            width=self.width,
            font=self.font,
            offset=(100, 0),
        )

    def visualize_left_sagittal_angle(self):
        # 上方为left
        assert (
            "tail_points" in self.points and "turning_points" in self.points
        ), "tail_points or turning_points not found"
        assert "sagittal_angle_left" in self.parameters, "sagittal_angle_left not found"

        vertex = self.points["turning_points"][0]
        start = self.points["tail_points"][0]
        end = [start[0], vertex[1]]
        draw_angle(
            self.draw,
            vertex,
            start,
            end,
            round(self.parameters["sagittal_angle_left"], self.precision),
            color=self.color,
            length=self.length,
            radius=self.radius,
            width=self.width,
            font=self.font,
            offset=(-140, 70),
        )

    def visualize_right_sagittal_angle(self):
        # 下方为right
        assert (
            "tail_points" in self.points and "turning_points" in self.points
        ), "tail_points or turning_points not found"
        assert (
            "sagittal_angle_right" in self.parameters
        ), "sagittal_angle_right not found"

        vertex = self.points["turning_points"][1]
        start = [self.points["tail_points"][1][0], vertex[1]]
        end = self.points["tail_points"][1]
        draw_angle(
            self.draw,
            vertex,
            start,
            end,
            round(self.parameters["sagittal_angle_right"], self.precision),
            color=self.color,
            length=self.length,
            radius=self.radius,
            width=self.width,
            font=self.font,
            offset=(-140, -70),
        )

    def visualize_temple_length(self):
        assert (
            "pile_points" in self.points and "tail_points" in self.points
        ), "pile_points or tail_points not found"
        assert "temple_length_left" in self.parameters, "temple_length_left not found"

        # visualize temple_length_left
        point1, point2 = self.points["tail_points"][0], self.points["pile_points"][0]
        # 高度与point2对齐
        point2, point1 = format_points([point2, point1], mode=1)
        draw_parameter(
            self.draw,
            point1,
            point2,
            round(self.parameters["temple_length_left"], self.precision),
            color=(255, 0, 0),
            dimension_mode=1,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(0, -50),
        )

    def visualize_temporal_width(self):
        assert "temporal_points" in self.points, "temporal_points not found"
        assert "temporal_width" in self.parameters, "temporal_width not found"
        point1, point2 = (
            self.points["temporal_points"][0],
            self.points["temporal_points"][1],
        )
        point1, point2 = format_points([point1, point2], mode=0)
        draw_parameter(
            self.draw,
            point1,
            point2,
            round(self.parameters["temporal_width"], self.precision),
            color=(255, 0, 0),
            dimension_mode=2,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(-20, 0),
        )

    def visualize_left_spread_angle(self):
        assert (
            "pile_points" in self.points
            and "bridge_point" in self.points
            and "temporal_points" in self.points
        ), "pile_points or bridge_point or temporal_points not found"
        assert "spread_angle_left" in self.parameters, "spread_angle_left not found"

        vertex = self.points["pile_points"][0]
        start = self.points["bridge_point"]
        end = self.points["temporal_points"][0]
        draw_angle(
            self.draw,
            vertex,
            start,
            end,
            round(self.parameters["spread_angle_left"], self.precision),
            color=self.color,
            length=self.length,
            radius=self.radius,
            width=self.width,
            font=self.font,
            offset=(-120, 120),
        )

    def visualize_right_spread_angle(self):
        assert (
            "pile_points" in self.points
            and "bridge_point" in self.points
            and "temporal_points" in self.points
        ), "pile_points or bridge_point or temporal_points not found"
        assert "spread_angle_right" in self.parameters, "spread_angle_right not found"

        vertex = self.points["pile_points"][1]
        start = self.points["temporal_points"][1]
        end = self.points["bridge_point"]
        draw_angle(
            self.draw,
            vertex,
            start,
            end,
            round(self.parameters["spread_angle_right"], self.precision),
            color=self.color,
            length=self.length,
            radius=self.radius,
            width=self.width,
            font=self.font,
            offset=(-120, -120),
        )

    def visualize_pile_distance(self):
        assert "pile_points" in self.points, "pile_points not found"
        assert "pile_distance" in self.parameters, "pile_distance not found"
        point1, point2 = self.points["pile_points"][0], self.points["pile_points"][1]
        point1, point2 = format_points([point1, point2], mode=0)
        draw_parameter(
            self.draw,
            point1,
            point2,
            round(self.parameters["pile_distance"], self.precision),
            color=(255, 0, 0),
            dimension_mode=2,
            width=self.width,
            dimension_length=self.dimension_length,
            font=self.font,
            offset=(-20, 0),
        )


if __name__ == "__main__":
    points = {
        "pile_points": [(3039, 658), (3039, 2733)],
        "temporal_points": [(2467, 682), (2472, 2718)],
        "turning_points": [(1538, 835), (1548, 2618)],
        "tail_points": [(1301, 1093), (1308, 2351)],
        "bridge_point": (3211, 1697),
    }

    parameters = {
        "face_angle": 161.17384124947267,
        "sagittal_angle_left": 38.077000495534406,
        "sagittal_angle_right": 41.87157375769405,
        "temple_length_left": 1791.6107278089178,
        "temple_length_right": 1772.6491474626332,
        "temporal_width": 2036.006139479938,
        "spread_angle_left": 96.99710420064447,
        "spread_angle_right": 97.91103718087473,
        "pile_distance": 2075.0,
    }

    image = cv2.imread("201300063039330109_0_painted.jpg")
    fv = UpVisualizer(
        image=image,
        points=points,
        parameters=parameters,
    )
    fv.visualize_parameters()
