from typing import Optional, List

import numpy as np
import torch
from torch import nn

from .image_detector import ImageDetector
from .keypointrcnn.model import get_model
from .keypointrcnn.predict import Predictor


class LeftDetector(ImageDetector):
    def __init__(self, net: Optional[nn.Module] = None, device: str = "cpu"):
        if net is None:
            net = get_model(num_keypoints=4, model="resnet101")
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            weights_path = os.path.join(current_dir, "checkpoints", "left_keypointsrcnn_resnet101_9.pth")
            weights = torch.load(
                weights_path, weights_only=True
            )
            net.load_state_dict(weights)
            net.to(device)
            net.eval()
        super().__init__(net, device)

    def detect(self, image: np.ndarray) -> List:
        predictor = Predictor(self.net, device=self.device)
        keypoints = predictor.predict(image)
        return keypoints
