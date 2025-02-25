from typing import Optional

import numpy as np


class SizeVisualizer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        image: np.ndarray,
        points: dict,
        parameters: dict,
    ):
        self.image = image
        self.points = points
        self.parameters = parameters
