from .front_get_lens import *
from .front_get_parameters import *


def calc_front(
    image_path: str,
    background_path: str,
    thresholds: Sequence[int] = (20, 30),
    crop: Sequence[float] = (0, 0, 1, 1),
):

    image = load(image_path)

    # 图片高度、宽度、面积
    height, width = image.shape[:2]
    area = width * height
    crop = [
        int(height * crop[0]),
        int(width * crop[1]),
        int(height * crop[2]),
        int(width * crop[3]),
    ]
    # 裁剪
    background = load(background_path)
    [image, background] = crop_images([image, background], *crop)
    lens_area = area * 0.005
    # 得到阈值处理的轮廓
    gray, lens, glasses_type = get_lens(
        image,  # 原始图像
        num_gaussian=3,  # 高斯模糊次数
        thresholds=thresholds,
        background=background,
        area_threshold=lens_area,  # 镜片面积阈值
    )
    # show(gray, f"gray_{filename}")
    if np.sum(np.sum(gray)) < lens_area:
        print("Please increase thresholds.")
        sys.exit()
    if glasses_type == 0:
        # 腐蚀轮廓边缘
        gray = cv2.erode(gray, np.ones((3, 3), np.uint8), iterations=1)
        lens = [contour_morphology(l, gray.shape) for l in lens]
    # 以镜圈轮廓中心旋转
    lens_center = [get_contour_center(c) for c in lens]
    angle = get_angle(*lens_center)
    image = rotate_image(image, angle, lens_center[0])
    gray = rotate_image(gray, angle, lens_center[0])

    contours, areas = get_contours(gray, lens_area)

    # 获取镜片轮廓(有镜腿)
    lens_incomplete = get_lens_incomplete(contours, areas, 1.1)

    # 去除镜腿
    lens = remove_legs(lens_incomplete, gray.shape, 200)
    lens.sort(key=lambda x: get_contour_center(x)[0])
    if glasses_type == 0:
        # 轮廓平滑
        lens = [smooth_contour(c) for c in lens]
        # 去除镜圈内部标签
        gray = remove_label(gray, lens)
    else:
        gray = remove_label(gray, lens)
        lens = [smooth_contour(c) for c in lens]

    # 前景图
    foreground = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    foreground[gray == 0] = TRANSPARENT

    # 镜片参数
    parameters_inner = get_parameters_inner(lens)

    parameters_outer, distance = get_parameters_outer(
        gray, lens, parameters_inner["lens_center_points"]
    )
    # 打印参数
    parameters = {**parameters_inner, **parameters_outer}
    parameters = {
        k: round(v, 4) if isinstance(v, (int, float)) else v
        for k, v in parameters.items()
    }

    distance["distance_up"] += crop[0]
    return parameters, distance
