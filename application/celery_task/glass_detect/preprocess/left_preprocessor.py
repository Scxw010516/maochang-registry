from typing import Union

import numpy as np

from .image_preprocessor import ImagePreprocessor


class LeftPreprocessor(ImagePreprocessor):
    def __init__(self):
        super().__init__()

    def preprocess(
        self,
        image: np.ndarray,
        crop_region: Union[tuple, list] = (1500, 3450, 600, 4500),
    ) -> np.ndarray:
        assert (
            image.shape[0] == 3496 and image.shape[1] == 4656
        ), "image shape should be (3496,4656)"
        crop_image = self.crop(image, crop_region)
        ret = crop_image
        return ret
