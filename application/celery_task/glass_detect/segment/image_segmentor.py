from typing import Optional

import numpy as np
from torch import nn


class ImageSegmentor:
    def __init__(self, net: Optional[nn.Module] = None, device: str = "cpu"):
        self.net = net
        self.device = device

    def segment(self, image: np.ndarray) -> np.ndarray:
        pass
