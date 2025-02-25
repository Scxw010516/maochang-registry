import threading

import cv2
from typing import Union, Optional
import numpy as np
import time

Image = np.ndarray


class ImageCalculator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, image: Optional[Image] = None):
        self.image = image

    def get_points(self) -> dict:
        pass

    def get_parameters(self) -> dict:
        pass


if __name__ == "__main__":

    ip1 = ImageCalculator(np.array([1]))
    ip2 = ImageCalculator(np.array([2]))
    print(ip1.image)
    print(ip1 is ip2)
