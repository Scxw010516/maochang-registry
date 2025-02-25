from typing import List

import cv2
import numpy as np
from torch import nn, Tensor
from torchvision.transforms import functional as F


class Predictor:
    def __init__(self, network: nn.Module, device="cuda"):
        self.network = network
        self.device = device
        self.network.to(device)
        self.network.eval()

    def predict(self, image: np.ndarray) -> List:
        image = self.format_image(image)
        prediction = self.network(image)[0]
        keypoints = (
            prediction["keypoints"].cpu().detach().numpy().astype(np.int32).tolist()
        )[0]
        # remove visibility
        keypoints = [[int(point[0]), int(point[1])] for point in keypoints]
        return keypoints

    def format_image(
        self,
        image: np.ndarray,
    ) -> Tensor:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = F.to_tensor(image)
        return image.unsqueeze(0).to(self.device)
