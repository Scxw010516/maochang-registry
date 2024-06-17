import json

from .get_glasses import get_glasses, rotate_glasses_left
from .get_parameters import get_parameters
from .utils import *


def calc_left(
    img_path: str,
    background_path: str,
    thresholds: Sequence[int] = (20, 30),
    crop: Sequence[float] = (0, 0, 1, 1),
):
    image = load(img_path)
    background = load(background_path)
    height, width = image.shape[:2]
    crop = [
        int(height * crop[0]),
        int(width * crop[1]),
        int(height * crop[2]),
        int(width * crop[3]),
    ]
    # show(image)
    [image, background] = crop_images([image, background], *crop)
    gray = get_glasses(image, background, thresholds=thresholds)

    gray = rotate_glasses_left(gray)

    # skeleton = morphology.skeletonize(gray)
    # show(gray)
    parameters = get_parameters(gray)
    parameters = {
        k: round(v, 4) if isinstance(v, (int, float)) else v
        for k, v in parameters.items()
    }
    return parameters
    # print(json.dumps(parameters, sort_keys=False, indent=2, default=default_dump))


if __name__ == "__main__":
    pass
    # main()
