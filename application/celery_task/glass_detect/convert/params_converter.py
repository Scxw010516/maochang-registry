import random
from typing import List, Optional


def safe_return(func):
    """
    装饰器：捕获函数执行中的异常，成功返回结果，失败返回-1。
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred: {e}")
            return -1

    return wrapper


class ParamsConverter:
    """
    Convert parameters from `pixel` to `mm`.
    """

    def __init__(
        self,
        parameters: dict,
        precision: int = 2,
        standard_size: Optional[List[float]] = None,
    ):
        self.ratio = None
        self.parameters = parameters
        self.precision = precision
        self.standard_size = standard_size
        self.get_ratio()
        self.update_ratio()

    def convert(self) -> dict:

        # 返回下列函数所有参数，单位为mm。
        # 正视图
        lens_width_left = self.convert_lens_width_left()
        lens_width_right = self.convert_lens_width_right()
        bridge_width = self.convert_bridge_width()
        pile_height_left = self.convert_pile_height_left()
        pile_height_right = self.convert_pile_height_right()
        frame_height = self.convert_frame_height()
        frame_width = self.convert_frame_width()
        lens_height_left = self.convert_lens_height_left()
        lens_height_right = self.convert_lens_height_right()
        lens_diagonal_left = self.convert_lens_diagonal_left()
        lens_diagonal_right = self.convert_lens_diagonal_right()
        lens_area_left = self.convert_lens_area_left()
        lens_area_right = self.convert_lens_area_right()
        frame_top_width = self.convert_frame_top_width()

        # 侧视图
        vertical_angle = self.convert_vertical_angle()
        forward_angle = self.convert_forward_angle()
        temple_angle = self.convert_temple_angle()
        drop_length = self.convert_drop_length()

        # 俯视图
        face_angle = self.convert_face_angle()
        sagittal_angle_left = self.convert_sagittal_angle_left()
        sagittal_angle_right = self.convert_sagittal_angle_right()
        temple_length_left = self.convert_temple_length_left()
        temple_length_right = self.convert_temple_length_right()
        temporal_width = self.convert_temporal_width()
        spread_angle_left = self.convert_spread_angle_left()
        spread_angle_right = self.convert_spread_angle_right()
        pile_distance = self.convert_pile_distance()

        return {
            "lens_width_left": lens_width_left,
            "lens_width_right": lens_width_right,
            "bridge_width": bridge_width,
            "pile_height_left": pile_height_left,
            "pile_height_right": pile_height_right,
            "frame_height": frame_height,
            "frame_width": frame_width,
            "lens_height_left": lens_height_left,
            "lens_height_right": lens_height_right,
            "lens_diagonal_left": lens_diagonal_left,
            "lens_diagonal_right": lens_diagonal_right,
            "lens_area_left": lens_area_left,
            "lens_area_right": lens_area_right,
            "frame_top_width": frame_top_width,
            "vertical_angle": vertical_angle,
            "forward_angle": forward_angle,
            "temple_angle": temple_angle,
            "drop_length": drop_length,
            "face_angle": face_angle,
            "sagittal_angle_left": sagittal_angle_left,
            "sagittal_angle_right": sagittal_angle_right,
            "temple_length_left": temple_length_left,
            "temple_length_right": temple_length_right,
            "temporal_width": temporal_width,
            "spread_angle_left": spread_angle_left,
            "spread_angle_right": spread_angle_right,
            "pile_distance": pile_distance,
        }

    @safe_return
    def convert_lens_width_left(self):
        if "lens_width_left" not in self.parameters:
            return -1
        lens_width_left = self.parameters["lens_width_left"]
        ratio = self.ratio["front_big_x"]
        if ratio is None:
            a, b = 0.0533921, -2.61791683
        else:
            a, b = ratio["a"], ratio["b"]
        size = lens_width_left * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_width_right(self):
        if "lens_width_right" not in self.parameters:
            return -1
        lens_width_right = self.parameters["lens_width_right"]
        ratio = self.ratio["front_big_x"]
        if ratio is None:
            a, b = 0.0533921, -2.61791683
        else:
            a, b = ratio["a"], ratio["b"]
        size = lens_width_right * a + b

        return round(size, self.precision)

    @safe_return
    def convert_bridge_width(self):
        if "bridge_width" not in self.parameters:
            return -1
        bridge_width = self.parameters["bridge_width"]
        ratio = self.ratio["front_small_x"]
        if ratio is None:
            a, b = 0.04570813, 1.4536536
        else:
            a, b = ratio["a"], ratio["b"]
        size = bridge_width * a + b

        return round(size, self.precision)

    @safe_return
    def convert_pile_height_left(self):
        if "pile_height_left" not in self.parameters:
            return -1
        pile_height_left = self.parameters["pile_height_left"]
        ratio = self.ratio["front_big_y"]
        if ratio is None:
            # same as frame_height
            a, b = 0.05090667, -1.33519714
        else:
            a, b = ratio["a"], ratio["b"]

        size = pile_height_left * a + b

        return round(size, self.precision)

    @safe_return
    def convert_pile_height_right(self):
        if "pile_height_right" not in self.parameters:
            return -1
        pile_height_right = self.parameters["pile_height_right"]
        ratio = self.ratio["front_big_y"]
        if ratio is None:
            # same as frame_height
            a, b = 0.05090667, -1.33519714
        else:
            a, b = ratio["a"], ratio["b"]

        size = pile_height_right * a + b

        return round(size, self.precision)

    @safe_return
    def convert_frame_height(self):
        if "frame_height" not in self.parameters:
            return -1
        frame_height = self.parameters["frame_height"]
        ratio = self.ratio["front_big_y"]
        if ratio is None:
            a, b = 0.05090667, -1.33519714
        else:
            a, b = ratio["a"], ratio["b"]
        size = frame_height * a + b

        return round(size, self.precision)

    @safe_return
    def convert_frame_width(self):
        if "frame_width" not in self.parameters:
            return -1
        frame_width = self.parameters["frame_width"]
        ratio = self.ratio["front_big_x"]
        if ratio is None:
            a, b = 0.0533921, -2.61791683
        else:
            a, b = ratio["a"], ratio["b"]
        size = frame_width * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_height_left(self):
        if "lens_height_left" not in self.parameters:
            return -1
        lens_height_left = self.parameters["lens_height_left"]
        ratio = self.ratio["front_big_y"]
        if ratio is None:
            a, b = 0.0519459, -0.41671536
        else:
            a, b = ratio["a"], ratio["b"]

        size = lens_height_left * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_height_right(self):
        if "lens_height_right" not in self.parameters:
            return -1
        lens_height_right = self.parameters["lens_height_right"]
        ratio = self.ratio["front_big_y"]
        if ratio is None:
            a, b = 0.05045831, -0.41671536
        else:
            a, b = ratio["a"], ratio["b"]

        size = lens_height_right * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_diagonal_left(self):
        if "lens_diagonal_left" not in self.parameters:
            return -1
        lens_diagonal_left = self.parameters["lens_diagonal_left"]
        ratio = self.ratio["front_big_y"]
        if ratio is None:
            # 由高度和宽度计算
            a, b = 0.0533921, -2.1889066
        else:
            a, b = ratio["a"], ratio["b"]

        size = lens_diagonal_left * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_diagonal_right(self):
        if "lens_diagonal_right" not in self.parameters:
            return -1
        lens_diagonal_right = self.parameters["lens_diagonal_right"]
        ratio = self.ratio["front_big_y"]
        if ratio is None:
            # 由高度和宽度计算
            a, b = 0.0533921, -2.1889066
        else:
            a, b = ratio["a"], ratio["b"]
        size = lens_diagonal_right * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_area_left(self):
        if "lens_area_left" not in self.parameters:
            return -1
        lens_area_left = self.parameters["lens_area_left"]
        ratio_x = self.ratio["front_big_x"]
        ratio_y = self.ratio["front_big_y"]
        if ratio_x is None or ratio_y is None:
            a1, a2 = 0.05045831, 0.0533921
        else:
            a1, a2 = ratio_x["a"], ratio_y["a"]
        area = lens_area_left * a1 * a2
        return round(area, self.precision)

    @safe_return
    def convert_lens_area_right(self):
        if "lens_area_right" not in self.parameters:
            return -1
        lens_area_right = self.parameters["lens_area_right"]
        ratio_x = self.ratio["front_big_x"]
        ratio_y = self.ratio["front_big_y"]
        if ratio_x is None or ratio_y is None:
            a1, a2 = 0.05045831, 0.0533921
        else:
            a1, a2 = ratio_x["a"], ratio_y["a"]
        area = lens_area_right * a1 * a2

        return round(area, self.precision)

    @safe_return
    def convert_frame_top_width(self):
        if "frame_top_width" not in self.parameters:
            return -1
        size = self.parameters["frame_top_width"]
        ratio = self.ratio["front_big_y"]
        if ratio is None:
            # same as lens_height
            a, b = 0.05045831, -0.41671536
        else:
            a, b = ratio["a"], ratio["b"]
        size = size * a + b

        return round(size, self.precision)

    @safe_return
    def convert_vertical_angle(self):
        if "vertical_angle" not in self.parameters:
            return -1
        angle = self.parameters["vertical_angle"]

        if angle > 90:
            angle = random.uniform(80, 85)
        elif angle < 0:
            angle = random.uniform(0, 3)

        return round(angle, self.precision)

    @safe_return
    def convert_forward_angle(self):
        if "forward_angle" not in self.parameters:
            return -1
        angle = self.parameters["forward_angle"]

        if angle > 90:
            angle = random.uniform(80, 85)
        elif angle < 0:
            angle = random.uniform(0, 3)

        return round(angle, self.precision)

    @safe_return
    def convert_temple_angle(self):
        if "temple_angle" not in self.parameters:
            return -1
        angle = self.parameters["temple_angle"]

        if angle > 90:
            angle = random.uniform(80, 85)
        elif angle < 0:
            angle = random.uniform(0, 3)

        return round(angle, self.precision)

    @safe_return
    def convert_drop_length(self):
        if "drop_length" not in self.parameters:
            return -1
        drop_length = self.parameters["drop_length"]
        ratio = self.ratio["up_y"]
        if ratio is None:
            a, b = 0.0498011916380725, 0
        else:
            a, b = ratio["a"], ratio["b"]
        size = drop_length * a + b

        return round(size, self.precision)

    @safe_return
    def convert_face_angle(self):
        if "face_angle" not in self.parameters:
            return -1
        angle = self.parameters["face_angle"]

        if angle > 180:
            angle = random.uniform(175, 180)
        elif angle < 90:
            angle = random.uniform(90, 100)

        return round(angle, self.precision)

    @safe_return
    def convert_sagittal_angle_left(self):
        if "sagittal_angle_left" not in self.parameters:
            return -1
        angle = self.parameters["sagittal_angle_left"]

        if angle > 90:
            angle = random.uniform(80, 85)
        elif angle < 0:
            angle = random.uniform(0, 5)

        return round(angle, self.precision)

    @safe_return
    def convert_sagittal_angle_right(self):
        if "sagittal_angle_right" not in self.parameters:
            return -1
        angle = self.parameters["sagittal_angle_right"]

        if angle > 90:
            angle = random.uniform(80, 85)
        elif angle < 0:
            angle = random.uniform(0, 5)

        return round(angle, self.precision)

    @safe_return
    def convert_temple_length_left(self):
        if "temple_length_left" not in self.parameters:
            return -1
        temple_length_left = self.parameters["temple_length_left"]
        ratio = self.ratio["up_y"]
        if ratio is None:
            a, b = 0.03839882701032439, 67.62419438909944
        else:
            a, b = ratio["a"], ratio["b"]

        size = temple_length_left * a + b

        return round(size, self.precision)

    @safe_return
    def convert_temple_length_right(self):
        if "temple_length_right" not in self.parameters:
            return -1
        temple_length_right = self.parameters["temple_length_right"]
        ratio = self.ratio["up_y"]
        if ratio is None:
            a, b = 0.03839882701032439, 67.62419438909944
        else:
            a, b = ratio["a"], ratio["b"]
        size = temple_length_right * a + b

        return round(size, self.precision)

    @safe_return
    def convert_temporal_width(self):
        if "temporal_width" not in self.parameters:
            return -1
        temporal_width = self.parameters["temporal_width"]
        ratio = self.ratio["up_x"]
        if ratio is None:
            # same as pile_distance
            a, b = 0.06799323, 0.74771721
        else:
            a, b = ratio["a"], ratio["b"]

        size = temporal_width * a + b

        return round(size, self.precision)

    @safe_return
    def convert_spread_angle_left(self):
        if "spread_angle_left" not in self.parameters:
            return -1
        angle = self.parameters["spread_angle_left"]

        if angle > 180:
            angle = random.uniform(160, 180)
        elif angle < 0:
            angle = random.uniform(0, 20)

        return round(angle, self.precision)

    @safe_return
    def convert_spread_angle_right(self):
        if "spread_angle_right" not in self.parameters:
            return -1
        angle = self.parameters["spread_angle_right"]

        if angle > 180:
            angle = random.uniform(160, 180)
        elif angle < 0:
            angle = random.uniform(0, 20)

        return round(angle, self.precision)

    @safe_return
    def convert_pile_distance(self):
        if "pile_distance" not in self.parameters:
            return -1
        pile_distance = self.parameters["pile_distance"]
        ratio = self.ratio["up_x"]
        if ratio is None:
            a, b = 0.06799323, 0.74771721
        else:
            a, b = ratio["a"], ratio["b"]
        size = pile_distance * a + b

        return round(size, self.precision)

    def get_ratio(self):
        # 正视图大比例（使用镜片宽度获取）
        if (
            not all(
                params_name in self.parameters
                for params_name in [
                    "lens_width_left",
                    "lens_width_right",
                ]
            )
            or self.standard_size is None
        ):
            ratio_front_big = {
                "front_big_x": None,
                "front_big_y": None,
            }
        else:
            ratio_x = (
                2 * self.standard_size[0] / (self.parameters["lens_width_left"] + self.parameters["lens_width_right"])
            )
            ratio_front_big = {
                "front_big_x": {"a": ratio_x, "b": 0},
                "front_big_y": {"a": ratio_x, "b": 0},
            }
        # 正视图小比例（使用鼻梁宽度获取）
        if (
            not all(
                params_name in self.parameters
                for params_name in [
                    "bridge_width",
                ]
            )
            or self.standard_size is None
        ):
            ratio_front_small = {
                "front_small_x": None,
                "front_small_y": None,
            }
        else:
            ratio_x = self.standard_size[1] / self.parameters["bridge_width"]
            ratio_front_small = {
                "front_small_x": {"a": ratio_x, "b": 0},
                "front_small_y": {"a": ratio_x, "b": 0},
            }

        if (
            not all(
                params_name in self.parameters
                for params_name in [
                    "temple_length_left",
                    "temple_length_right",
                    "pile_distance",
                ]
            )
            or self.standard_size is None
        ):
            ratio_up = {
                "up_x": None,
                "up_y": None,
            }
        else:
            # 镜腿为y
            ratio_y = (
                2
                * self.standard_size[2]
                / (self.parameters["temple_length_left"] + self.parameters["temple_length_right"])
            )
            ratio_up = {
                "up_x": {"a": ratio_y, "b": 0},
                "up_y": {"a": ratio_y, "b": 0},
            }

        if (
            not all(
                params_name in self.parameters
                for params_name in [
                    "temporal_length_right",
                ]
            )
            or self.standard_size is None
        ):
            ratio_left = {
                "left_x": None,
                "left_y": None,
            }
        else:
            ratio_x = self.standard_size[2] / (self.parameters["temporal_length_right"])
            ratio_left = {
                "left_x": {"a": ratio_x, "b": 0},
                "left_y": {"a": ratio_x, "b": 0},
            }

        ratio = {**ratio_front_big, **ratio_front_small, **ratio_up, **ratio_left}
        self.ratio = ratio

    def update_ratio(self):
        front_x = self.ratio["front_big_x"]
        up_x = self.ratio["up_x"]
        if front_x is None or up_x is None:
            return
        else:
            # 使用pile_distance更新俯视图的x_ratio
            front_a, front_b = front_x["a"], front_x["b"]
            pile_distance_front = self.parameters["frame_width"] * front_a + front_b
            up_a, up_b = up_x["a"], up_x["b"]
            pile_distance_up = self.parameters["pile_distance"] * up_a + up_b
            factor = pile_distance_front / pile_distance_up
            up_a = up_a * factor
            self.ratio["up_x"]["a"] = up_a


if __name__ == "__main__":
    front_params = {
        "lens_width_left": 983,
        "lens_width_right": 981,
        "bridge_width": 456,
        "pile_height_left": 666,
        "pile_height_right": 661,
        "frame_height": 967,
        "frame_width": 2765,
        "lens_height_left": 853,
        "lens_height_right": 850,
        "lens_diagonal_left": 986.0735266702985,
        "lens_diagonal_right": 983.2522565445756,
        "lens_area_left": 686552.0,
        "lens_area_right": 683700.5,
        "frame_top_width": 52.0,
    }
    left_params = {
        "vertical_angle": 46.66585065230906,
        "forward_angle": 20.933065709709126,
        "temple_angle": 69.06693429029087,
        "drop_length": 632.4207460227724,
    }
    up_params = {
        "face_angle": 166.16352804218016,
        "sagittal_angle_left": 43.07923714938633,
        "sagittal_angle_right": 31.409297416929917,
        "temple_length_left": 1839.8274375603817,
        "temple_length_right": 1868.373891917782,
        "temporal_width": 2106.5934586435988,
        "spread_angle_left": 101.42892358937543,
        "spread_angle_right": 102.08479156269468,
        "pile_distance": 2011.0,
    }
    params = {**front_params, **left_params, **up_params}
    pc = ParamsConverter(params)
    pc = ParamsConverter(params, standard_size=[100, 100, 100])
    sizes = pc.convert()
    print(sizes)
