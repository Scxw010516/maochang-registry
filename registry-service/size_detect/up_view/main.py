import json
import time

from .get_glasses import *
from .get_parameters import get_parameters
from .utils import *


def calc_up(
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

    [image, background] = crop_images([image, background], *crop)
    gray = get_glasses(image, background, thresholds=thresholds)
    piles = get_piles(gray)
    angle = get_angle(piles[0], piles[1])
    if angle > 0:
        angle -= np.pi / 2
    else:
        angle += np.pi / 2
    gray = rotate_image(gray, angle, piles[0])
    piles[1] = rotate_point(piles[1], piles[0], -angle)

    parameters, distance = get_parameters(gray, piles)
    parameters = {
        k: round(v, 4) if isinstance(v, (int, float)) else v
        for k, v in parameters.items()
    }
    # 标定距离加回裁剪的部分
    distance["distance_front"] = width - (crop[1] + distance["distance_front"])
    distance["distance_left"] += crop[0]

    return parameters, distance

    # print(json.dumps(parameters, sort_keys=False, indent=2, default=default_dump))


if __name__ == "__main__":
    pass
    # break
    # main()
