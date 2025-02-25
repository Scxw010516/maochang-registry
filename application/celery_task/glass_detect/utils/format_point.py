import numpy as np


def format_point(points):
    if isinstance(points, dict):
        return {key: format_point(value) for key, value in points.items()}
    elif (
        isinstance(points, list)
        or isinstance(points, tuple)
        or isinstance(points, np.ndarray)
    ):
        return [format_point(point) for point in points]
    else:
        return points
