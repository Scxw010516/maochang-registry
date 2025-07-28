from typing import Optional
import os
import numpy as np
import torch
from torch import nn

from .image_segmentor import ImageSegmentor
from .unet.predict.predictor import Predictor


class TempleWfSegmentor(ImageSegmentor):
    def __init__(self, net: Optional[nn.Module] = None, device: str = "cpu"):
        # image should be in BGR format
        if net is None:
            from .unet.utils.create_unet import create_unet

            net = create_unet(num_classes=2)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            checkpoint_path = os.path.join(current_dir, "checkpoints", "templeWf.pth")
            checkpoint = torch.load(
                checkpoint_path, weights_only=False
            )
            net.load_state_dict(checkpoint["network_weights"])
            # net = net.to(device)
            net.eval()

        super().__init__(net, device)

    def segment(
        self,
        image: np.ndarray,
        properties: Optional[dict] = None,
        patch_size: tuple = (896, 1792),
        is_one: bool = True,
    ) -> np.ndarray:
        default_properties = {
            "spacing": (999, 1, 1),
            "shape_before_cropping": (1, 1950, 3900),
            "bbox_used_for_cropping": [[0, 1], [0, 1950], [0, 3900]],
            "shape_after_cropping_and_before_resampling": (1, 1950, 3900),
        }
        properties = (
            default_properties
            if properties is None
            else {**default_properties, **properties}
        )

        image = image.transpose(2, 0, 1).astype(np.float32)
        image = np.expand_dims(image, axis=1)
        image = torch.from_numpy(image)

        predictor = Predictor(
            network=self.net,
            patch_size=patch_size,
            use_mirroring=False,
            device=torch.device(self.device),
        )

        y = predictor.predict_single_npy_array(
            image, properties, num_segmentation_heads=2
        )[0]
        if not is_one:
            y *= 255
        y = y.astype(np.uint8)

        return y
