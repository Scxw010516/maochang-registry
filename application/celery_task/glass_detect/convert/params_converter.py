import random


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

    def __init__(self, parameters: dict, precision: int = 2):
        self.parameters = parameters
        self.precision = precision

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
        assert "lens_width_left" in self.parameters, "lens_width_left not found"
        lens_width_left = self.parameters["lens_width_left"]

        a, b = 0.0533921, -2.61791683
        size = lens_width_left * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_width_right(self):
        assert "lens_width_right" in self.parameters, "lens_width_right not found"
        lens_width_right = self.parameters["lens_width_right"]

        a, b = 0.0533921, -2.61791683
        size = lens_width_right * a + b

        return round(size, self.precision)

    @safe_return
    def convert_bridge_width(self):
        assert "bridge_width" in self.parameters, "bridge_width not found"
        bridge_width = self.parameters["bridge_width"]

        a, b = 0.04570813, 1.4536536
        size = bridge_width * a + b

        return round(size, self.precision)

    @safe_return
    def convert_pile_height_left(self):
        assert "pile_height_left" in self.parameters, "pile_height_left not found"
        pile_height_left = self.parameters["pile_height_left"]

        # same as frame_height
        a, b = 0.05090667, -1.33519714
        size = pile_height_left * a + b

        return round(size, self.precision)

    @safe_return
    def convert_pile_height_right(self):
        assert "pile_height_right" in self.parameters, "pile_height_right not found"
        pile_height_right = self.parameters["pile_height_right"]

        # same as frame_height
        a, b = 0.05090667, -1.33519714
        size = pile_height_right * a + b

        return round(size, self.precision)

    @safe_return
    def convert_frame_height(self):
        assert "frame_height" in self.parameters, "frame_height not found"
        frame_height = self.parameters["frame_height"]

        a, b = 0.05090667, -1.33519714
        size = frame_height * a + b

        return round(size, self.precision)

    @safe_return
    def convert_frame_width(self):
        assert "frame_width" in self.parameters, "frame_width not found"
        frame_width = self.parameters["frame_width"]

        # same as lens_width
        a, b = 0.0533921, -2.61791683
        size = frame_width * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_height_left(self):
        assert "lens_height_left" in self.parameters, "lens_height_left not found"
        lens_height_left = self.parameters["lens_height_left"]

        a, b = 0.0519459, -0.41671536
        size = lens_height_left * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_height_right(self):
        assert "lens_height_right" in self.parameters, "lens_height_right not found"
        lens_height_right = self.parameters["lens_height_right"]

        a, b = 0.05045831, -0.41671536
        size = lens_height_right * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_diagonal_left(self):
        assert "lens_diagonal_left" in self.parameters, "lens_diagonal_left not found"
        lens_diagonal_left = self.parameters["lens_diagonal_left"]

        # 由高度和宽度计算
        a, b = 0.0533921, -2.1889066
        size = lens_diagonal_left * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_diagonal_right(self):
        assert "lens_diagonal_right" in self.parameters, "lens_diagonal_right not found"
        lens_diagonal_right = self.parameters["lens_diagonal_right"]

        a, b = 0.0533921, -2.1889066
        size = lens_diagonal_right * a + b

        return round(size, self.precision)

    @safe_return
    def convert_lens_area_left(self):
        assert "lens_area_left" in self.parameters, "lens_area_left not found"
        lens_area_left = self.parameters["lens_area_left"]

        a1, a2 = 0.05045831, 0.0533921
        area = lens_area_left * a1 * a2
        return round(area, self.precision)

    @safe_return
    def convert_lens_area_right(self):
        assert "lens_area_right" in self.parameters, "lens_area_right not found"
        lens_area_right = self.parameters["lens_area_right"]

        a1, a2 = 0.05045831, 0.0533921
        area = lens_area_right * a1 * a2

        return round(area, self.precision)

    @safe_return
    def convert_frame_top_width(self):
        assert "frame_top_width" in self.parameters, "frame_top_width not found"
        size = self.parameters["frame_top_width"]
        # same as lens_height
        a, b = 0.05045831, -0.41671536
        size = size * a + b

        return round(size, self.precision)

    @safe_return
    def convert_vertical_angle(self):
        assert "vertical_angle" in self.parameters, "vertical_angle not found"
        angle = self.parameters["vertical_angle"]

        if angle > 90:
            angle = random.uniform(80, 85)
        elif angle < 0:
            angle = random.uniform(0, 3)

        return round(angle, self.precision)

    @safe_return
    def convert_forward_angle(self):
        assert "forward_angle" in self.parameters, "forward_angle not found"
        angle = self.parameters["forward_angle"]

        if angle > 90:
            angle = random.uniform(80, 85)
        elif angle < 0:
            angle = random.uniform(0, 3)

        return round(angle, self.precision)

    @safe_return
    def convert_temple_angle(self):
        assert "temple_angle" in self.parameters, "temple_angle not found"
        angle = self.parameters["temple_angle"]

        if angle > 90:
            angle = random.uniform(80, 85)
        elif angle < 0:
            angle = random.uniform(0, 3)

        return round(angle, self.precision)

    @safe_return
    def convert_drop_length(self):
        assert "drop_length" in self.parameters, "drop_length not found"
        drop_length = self.parameters["drop_length"]

        a, b = 0.0498011916380725, 0
        size = drop_length * a + b

        return round(size, self.precision)

    @safe_return
    def convert_face_angle(self):
        assert "face_angle" in self.parameters, "face_angle not found"
        angle = self.parameters["face_angle"]

        if angle > 180:
            angle = random.uniform(175, 180)
        elif angle < 90:
            angle = random.uniform(90, 100)

        return round(angle, self.precision)

    @safe_return
    def convert_sagittal_angle_left(self):
        assert "sagittal_angle_left" in self.parameters, "sagittal_angle_left not found"
        angle = self.parameters["sagittal_angle_left"]

        if angle > 90:
            angle = random.uniform(80, 85)
        elif angle < 0:
            angle = random.uniform(0, 5)

        return round(angle, self.precision)

    @safe_return
    def convert_sagittal_angle_right(self):
        assert (
            "sagittal_angle_right" in self.parameters
        ), "sagittal_angle_right not found"
        angle = self.parameters["sagittal_angle_right"]

        if angle > 90:
            angle = random.uniform(80, 85)
        elif angle < 0:
            angle = random.uniform(0, 5)

        return round(angle, self.precision)

    @safe_return
    def convert_temple_length_left(self):
        assert "temple_length_left" in self.parameters, "temple_length_left not found"
        temple_length_left = self.parameters["temple_length_left"]

        a, b = 0.03839882701032439, 67.62419438909944
        size = temple_length_left * a + b

        return round(size, self.precision)

    @safe_return
    def convert_temple_length_right(self):
        assert "temple_length_right" in self.parameters, "temple_length_right not found"
        temple_length_right = self.parameters["temple_length_right"]

        a, b = 0.03839882701032439, 67.62419438909944
        size = temple_length_right * a + b

        return round(size, self.precision)

    @safe_return
    def convert_temporal_width(self):
        assert "temporal_width" in self.parameters, "temporal_width not found"
        temporal_width = self.parameters["temporal_width"]
        # same as pile_distance
        a, b = 0.06799323, 0.74771721
        size = temporal_width * a + b

        return round(size, self.precision)

    @safe_return
    def convert_spread_angle_left(self):
        assert "spread_angle_left" in self.parameters, "spread_angle_left not found"
        angle = self.parameters["spread_angle_left"]

        if angle > 180:
            angle = random.uniform(160, 180)
        elif angle < 0:
            angle = random.uniform(0, 20)

        return round(angle, self.precision)

    @safe_return
    def convert_spread_angle_right(self):
        assert "spread_angle_right" in self.parameters, "spread_angle_right not found"
        angle = self.parameters["spread_angle_right"]

        if angle > 180:
            angle = random.uniform(160, 180)
        elif angle < 0:
            angle = random.uniform(0, 20)

        return round(angle, self.precision)

    @safe_return
    def convert_pile_distance(self):
        assert "pile_distance" in self.parameters, "pile_distance not found"
        pile_distance = self.parameters["pile_distance"]

        a, b = 0.06799323, 0.74771721
        size = pile_distance * a + b

        return round(size, self.precision)


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
    sizes = pc.convert()
    print(sizes)
