from typing import Union

import numpy as np


class ImagePreprocessor:
    def __init__(self):
        pass

    def crop(self, image, crop_region: Union[tuple, list]) -> np.ndarray:
        # crop_region:(y1,y2,x1,x2)
        crop_image = image[
            crop_region[0] : crop_region[1], crop_region[2] : crop_region[3]
        ]
        return crop_image
