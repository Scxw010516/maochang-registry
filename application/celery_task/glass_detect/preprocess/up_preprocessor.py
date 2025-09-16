from typing import Union

import numpy as np

from .image_preprocessor import ImagePreprocessor


class UpPreprocessor(ImagePreprocessor):
    def __init__(self):
        super().__init__()

    def preprocess(
        self, image: np.ndarray, crop_region: Union[tuple, list] = (0, None, 0, None), dst_size=(4656, 3496)
    ) -> np.ndarray:
        # assert (
        #     image.shape[0] == 3496 and image.shape[1] == 4656
        # ), "image shape should be (3496,4656)"
        crop_image = self.crop(image, crop_region)
        crop_image = self.resize(crop_image, dst_size)
        ret = crop_image
        return ret
