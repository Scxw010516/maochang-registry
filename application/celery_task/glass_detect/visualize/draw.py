from typing import List, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .utils import get_angle, theta2angle, angle2theta


def draw_text(
    draw: ImageDraw.ImageDraw,
    position: Union[Tuple[float, float], List[float]],
    text="Hello World!",
    color=(255, 0, 0),
    font=None,
    angle: int = 0,
    offset: Union[Tuple[int, int], List[int]] = (0, 0),
):
    assert len(position) == 2, "position must be (x, y)"
    if font is None:
        font = ImageFont.load_default()
    text_bbox = font.getbbox(text)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    hypotenuse = (text_width**2 + text_height**2) ** 0.5
    temp_img = Image.new("RGBA", (int(hypotenuse), int(hypotenuse)), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)

    temp_draw.text(
        ((hypotenuse - text_width) // 2, (hypotenuse - text_height) // 2),
        text,
        fill=color,
        font=font,
    )
    rotated_text = temp_img.rotate(
        angle,
        expand=True,
        resample=Image.BICUBIC,
        center=(hypotenuse // 2, hypotenuse // 2),
    )
    paste_position = (
        int(position[0] - hypotenuse // 2 + offset[0]),
        int(position[1] - hypotenuse // 2 + offset[1]),
    )
    draw._image.paste(rotated_text, paste_position, rotated_text)


def draw_line(
    draw: ImageDraw.ImageDraw,
    start: Union[Tuple[int, int], List[int]],
    end: Union[Tuple[int, int], List[int]],
    color=(255, 0, 0),
    width: int = 1,
):
    draw.line([*start, *end], fill=color, width=width)


def draw_dashed_line(
    draw: ImageDraw.ImageDraw,
    start: Union[Tuple[int, int], List[int]],
    end: Union[Tuple[int, int], List[int]],
    color=(255, 0, 0),
    width: int = 1,
    dash_ratio: float = 1.0,
    line_length: int = 15,
):
    interval_length = line_length * dash_ratio
    distance = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
    ratio = [(end[0] - start[0]) / distance, (end[1] - start[1]) / distance]
    num = int(distance / (interval_length + line_length))
    lines = []

    for i in range(num):
        s = [
            start[0] + i * (line_length + interval_length) * ratio[0],
            start[1] + i * (line_length + interval_length) * ratio[1],
        ]
        e = [
            s[0] + line_length * ratio[0],
            s[1] + line_length * ratio[1],
        ]
        lines.append([*s, *e])
    residual_length = distance - num * (line_length + interval_length)
    s = (
        [start[0], start[1]]
        if num == 0
        else [
            lines[-1][2] + interval_length * ratio[0],
            lines[-1][3] + interval_length * ratio[1],
        ]
    )
    e = [
        (
            s[0]
            + (
                residual_length * ratio[0]
                if residual_length < interval_length
                else line_length * ratio[0]
            )
        ),
        (
            s[1]
            + (
                residual_length * ratio[1]
                if residual_length < interval_length
                else line_length * ratio[1]
            )
        ),
    ]
    lines.append([*s, *e])

    for line in lines:
        draw.line(line, fill=color, width=width)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    head: Union[Tuple[int, int], List[int]],
    color=(255, 0, 0),
    length=10,
    angle=0,
):
    angle1 = -angle - 30
    angle2 = -angle + 30
    theta1 = angle2theta(angle1)
    theta2 = angle2theta(angle2)

    foot1 = [head[0] - length * np.cos(theta1), head[1] - length * np.sin(theta1)]
    foot2 = [head[0] - length * np.cos(theta2), head[1] - length * np.sin(theta2)]

    triangle = [*head, *foot1, *foot2]
    draw.polygon(triangle, fill=color)


def draw_parameter(
    draw: ImageDraw.ImageDraw,
    start: Union[Tuple[int, int], List[int]],
    end: Union[Tuple[int, int], List[int]],
    parameter: float,
    color=(255, 0, 0),
    width: int = 1,
    font=None,
    dimension_mode=0,
    dimension_length=100,
    offset: Union[Tuple[int, int], List[int]] = (0, 0),
):
    assert dimension_mode in [
        0,
        1,
        2,
        3,
    ]  # 0: no dimension, 1: vertical, 2: horizontal, 3: adaptive
    if font is None:
        font = ImageFont.load_default()
    angle = get_angle(start, end)
    draw_line(draw, start, end, color=color, width=width)
    draw_arrow(draw, end, color=color, angle=angle, length=width * 5)
    draw_arrow(draw, start, color=color, angle=angle + 180, length=width * 5)
    draw_text(
        draw,
        [(start[0] + end[0]) // 2, (start[1] + end[1]) // 2],
        text=str(parameter),
        color=color,
        font=font,
        angle=angle,
        offset=offset,
    )

    if dimension_mode == 1:
        points1 = [
            [start[0], start[1] - dimension_length // 2],
            [start[0], start[1] + dimension_length // 2],
        ]
        points2 = [
            [end[0], end[1] - dimension_length // 2],
            [end[0], end[1] + dimension_length // 2],
        ]
        draw_dashed_line(draw, points1[0], points1[1], width=width)
        draw_dashed_line(draw, points2[0], points2[1], width=width)
    elif dimension_mode == 2:
        points1 = [
            [start[0] - dimension_length // 2, start[1]],
            [start[0] + dimension_length // 2, start[1]],
        ]
        points2 = [
            [end[0] - dimension_length // 2, end[1]],
            [end[0] + dimension_length // 2, end[1]],
        ]
        draw_dashed_line(draw, points1[0], points1[1], width=width)
        draw_dashed_line(draw, points2[0], points2[1], width=width)
    elif dimension_mode == 3:
        theta = angle2theta(angle)
        points1 = [
            [
                start[0] - int(dimension_length / 2 * np.sin(theta)),
                start[1] - int(dimension_length / 2 * np.cos(theta)),
            ],
            [
                start[0] + int(dimension_length / 2 * np.sin(theta)),
                start[1] + int(dimension_length / 2 * np.cos(theta)),
            ],
        ]
        points2 = [
            [
                end[0] - int(dimension_length / 2 * np.sin(theta)),
                end[1] - int(dimension_length / 2 * np.cos(theta)),
            ],
            [
                end[0] + int(dimension_length / 2 * np.sin(theta)),
                end[1] + int(dimension_length / 2 * np.cos(theta)),
            ],
        ]
        draw_dashed_line(draw, points1[0], points1[1], width=width)
        draw_dashed_line(draw, points2[0], points2[1], width=width)


def draw_outer_parameter(
    draw: ImageDraw.ImageDraw,
    start: Union[Tuple[int, int], List[int]],
    end: Union[Tuple[int, int], List[int]],
    parameter: float,
    color=(255, 0, 0),
    width: int = 1,
    font=None,
    dimension_mode=0,
    dimension_length=100,
    offset: Union[Tuple[int, int], List[int]] = (0, 0),
):
    assert dimension_mode in [
        0,
        1,
        2,
        3,
    ]  # 0: no dimension, 1: vertical, 2: horizontal, 3: adaptive
    if font is None:
        font = ImageFont.load_default()
    angle = get_angle(start, end)
    draw_line(draw, start, end, color=color, width=width)
    draw_arrow(draw, end, color=color, angle=angle, length=width * 5)
    draw_arrow(draw, start, color=color, angle=angle + 180, length=width * 5)
    # 引出线
    middle_point = [(start[0] + end[0]) // 2, (start[1] + end[1]) // 2]
    poly1_point = [middle_point[0] + 150, middle_point[1] - 150]
    poly2_point = [poly1_point[0] + 50, poly1_point[1]]
    draw_line(
        draw,
        middle_point,
        poly1_point,
        color=color,
        width=width // 2,
    )
    draw_line(draw, poly1_point, poly2_point, color=color, width=width // 2)
    draw_text(
        draw,
        poly2_point,
        text=str(parameter),
        color=color,
        font=font,
        angle=0,
        offset=offset,
    )

    if dimension_mode == 1:
        points1 = [
            [start[0], start[1] - dimension_length // 2],
            [start[0], start[1] + dimension_length // 2],
        ]
        points2 = [
            [end[0], end[1] - dimension_length // 2],
            [end[0], end[1] + dimension_length // 2],
        ]
        draw_dashed_line(draw, points1[0], points1[1], width=width)
        draw_dashed_line(draw, points2[0], points2[1], width=width)
    elif dimension_mode == 2:
        points1 = [
            [start[0] - dimension_length // 2, start[1]],
            [start[0] + dimension_length // 2, start[1]],
        ]
        points2 = [
            [end[0] - dimension_length // 2, end[1]],
            [end[0] + dimension_length // 2, end[1]],
        ]
        draw_dashed_line(draw, points1[0], points1[1], width=width)
        draw_dashed_line(draw, points2[0], points2[1], width=width)
    elif dimension_mode == 3:
        theta = angle2theta(angle)
        points1 = [
            [
                start[0] - int(dimension_length / 2 * np.sin(theta)),
                start[1] - int(dimension_length / 2 * np.cos(theta)),
            ],
            [
                start[0] + int(dimension_length / 2 * np.sin(theta)),
                start[1] + int(dimension_length / 2 * np.cos(theta)),
            ],
        ]
        points2 = [
            [
                end[0] - int(dimension_length / 2 * np.sin(theta)),
                end[1] - int(dimension_length / 2 * np.cos(theta)),
            ],
            [
                end[0] + int(dimension_length / 2 * np.sin(theta)),
                end[1] + int(dimension_length / 2 * np.cos(theta)),
            ],
        ]
        draw_dashed_line(draw, points1[0], points1[1], width=width)
        draw_dashed_line(draw, points2[0], points2[1], width=width)


def draw_arc(
    draw: ImageDraw.ImageDraw,
    vertex: Union[Tuple[int, int], List[int]],
    start: Union[Tuple[int, int], List[int]],
    end: Union[Tuple[int, int], List[int]],
    color=(255, 0, 0),
    radius=10,
    width=1,
):
    # print(vertex, start, end)
    angle1, angle2 = get_angle(vertex, start), get_angle(vertex, end)
    # print(angle1, angle2)
    theta1, theta2 = angle2theta(angle1), angle2theta(angle2)
    x0, y0 = vertex[0] - radius, vertex[1] - radius
    x1, y1 = vertex[0] + radius, vertex[1] + radius
    # print(x0, y0, x1, y1)
    # arc角度为顺时针方向
    # xy中心为圆心，宽高为圆直径
    draw.arc((x0, y0, x1, y1), -angle1, -angle2, width=width, fill=color)


def draw_angle(
    draw: ImageDraw.ImageDraw,
    vertex: Union[Tuple[int, int], List[int]],
    start: Union[Tuple[int, int], List[int]],
    end: Union[Tuple[int, int], List[int]],
    parameter: float,
    color=(255, 0, 0),
    length=200,
    radius=100,
    width=1,
    font=None,
    offset: Union[Tuple[int, int], List[int]] = (0, 0),
):
    # start->end应为顺时针方向

    angle1, angle2 = get_angle(vertex, start), get_angle(vertex, end)
    theta1, theta2 = angle2theta(angle1), angle2theta(angle2)
    point1 = [vertex[0] + length * np.cos(theta1), vertex[1] - length * np.sin(theta1)]
    point2 = [vertex[0] + length * np.cos(theta2), vertex[1] - length * np.sin(theta2)]
    draw_dashed_line(draw, vertex, point1, width=width)
    draw_dashed_line(draw, vertex, point2, width=width)
    draw_arc(draw, vertex, start, end, color=color, radius=radius, width=width)
    draw_text(
        draw,
        [vertex[0] - 10, vertex[1] - 10],
        str(parameter) + "°",
        color,
        font,
        offset=offset,
    )


def draw_outer_angle(
    draw: ImageDraw.ImageDraw,
    vertex: Union[Tuple[int, int], List[int]],
    start: Union[Tuple[int, int], List[int]],
    end: Union[Tuple[int, int], List[int]],
    parameter: float,
    color=(255, 0, 0),
    length=200,
    radius=100,
    width=1,
    font=None,
    offset: Union[Tuple[int, int], List[int]] = (0, 0),
):
    # start->end应为顺时针方向

    angle1, angle2 = get_angle(vertex, start), get_angle(vertex, end)
    theta1, theta2 = angle2theta(angle1), angle2theta(angle2)
    point1 = [vertex[0] + length * np.cos(theta1), vertex[1] - length * np.sin(theta1)]
    point2 = [vertex[0] + length * np.cos(theta2), vertex[1] - length * np.sin(theta2)]
    draw_dashed_line(draw, vertex, point1, width=width)
    draw_dashed_line(draw, vertex, point2, width=width)
    draw_arc(draw, vertex, start, end, color=color, radius=radius, width=width)

    # 引出线
    middle_point1 = [
        vertex[0] + radius * np.cos(theta1),
        vertex[1] - radius * np.sin(theta1),
    ]
    middle_point2 = [
        vertex[0] + radius * np.cos(theta2),
        vertex[1] - radius * np.sin(theta2),
    ]
    middle_point = [
        (middle_point1[0] + middle_point2[0]) // 2,
        (middle_point1[1] + middle_point2[1]) // 2,
    ]
    poly_point1 = [middle_point[0] + 150, middle_point[1] + 150]
    poly_point2 = [poly_point1[0] + 50, poly_point1[1]]
    draw_line(
        draw,
        middle_point,
        poly_point1,
        color=color,
        width=width,
    )
    draw_line(
        draw,
        poly_point1,
        poly_point2,
        color=color,
        width=width,
    )
    draw_text(
        draw,
        poly_point2,
        str(parameter) + "°",
        color,
        font,
        offset=offset,
    )


def main():
    font = ImageFont.truetype("SimHei.ttf", size=30)
    image = Image.open("201300063039330005.png")
    draw = ImageDraw.Draw(image)
    vertex = (2787, 733)
    start = (3236, 733)
    end = (3236, 1127)
    # draw.arc((100, 100, 400, 200), 0, 210, width=5, fill="red")
    # draw.arc((50, 50, 250, 250), start=45, end=315, fill="blue", width=2)
    # draw_arc(draw, vertex, start, end, color=(255, 0, 0), length=100, width=5)
    # draw_angle(
    #     draw, vertex, start, end, 45, color=(255, 0, 0), length=100, width=5, font=font
    # )
    # draw_parameter(draw, start, end, 4000000, color=(255, 0, 0), font=font)
    # draw_line(draw, start, end, color=(255, 0, 0))
    # angle = get_angle(start, end)
    #
    # draw_arrow(draw, end, color=(255, 0, 0), length=10, angle=angle)
    # draw_text(
    #     draw, [1000, 350], "Hello World!", color=(255, 0, 0), font=font, angle=angle
    # )
    image.save("201300063039330005_1.png")


if __name__ == "__main__":
    main()
    # print(np.cos(angle2theta(90)))
