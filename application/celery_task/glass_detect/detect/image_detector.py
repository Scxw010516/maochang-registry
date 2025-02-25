from typing import Optional, List

import numpy as np
from torch import nn


class ImageDetector:
    def __init__(self, net: Optional[nn.Module] = None, device: str = "cpu"):
        self.net = net
        self.device = device

    def detect(self, image: np.ndarray) -> List:
        pass
