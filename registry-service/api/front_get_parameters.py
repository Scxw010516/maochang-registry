from .utils import *


def get_pile_height(
    image: IMAGE, contour: CONTOUR, pile_scale: float = 0.01, margin: int = 10
):
    # 镜框轮廓
    rect = cv2.boundingRect(contour)
    x, y, w, h = rect

    # 左右桩头前景
    image_pile_left = image[y : y + h, x : x + int(w * pile_scale)]
    image_pile_right = image[y : y + h, int(x + (1 - pile_scale) * w) : x + w]

    # 添加margin，方便提取轮廓
    image_pile_left = cv2.copyMakeBorder(
        image_pile_left,
        top=margin,
        bottom=margin,
        left=margin,
        right=margin,
        borderType=cv2.BORDER_CONSTANT,
    )
    image_pile_right = cv2.copyMakeBorder(
        image_pile_right,
        top=margin,
        bottom=margin,
        left=margin,
        right=margin,
        borderType=cv2.BORDER_CONSTANT,
    )

    # 左桩头
    contour_left = cv2.findContours(
        image_pile_left, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )[0][0]
    # 轮廓
    rect_left = cv2.boundingRect(contour_left)
    # 桩头高度(轮廓高度)
    pile_height_left = h - (rect_left[1] + rect_left[3] - margin)

    contour_right = cv2.findContours(
        image_pile_right, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )[0][0]
    rect_right = cv2.boundingRect(contour_right)
    pile_height_right = h - (rect_right[1] + rect_right[3] - margin)

    distance_up = (rect_left[1] + rect_right[1]) / 2 - margin + y

    return pile_height_left, pile_height_right, distance_up


def get_parameters_inner(contours: CONTOURS) -> dict:
    """
    获取镜框参数

    params：
        - contours: CONTOURS - 待处理的一组轮廓，每个轮廓都是二维点集

    return：
    - 返回一个字典，包含以下内容：
        - rects: list of tuples - 每个轮廓对应的边界框坐标（左上角x, 左上角y, 宽度, 高度）
        - width: float - 两个最邻近轮廓边界框平均宽度
        - height: float - 两个最邻近轮廓边界框平均高度
        - bridge_width: float - 两个轮廓之间的最小宽度
        - center: list of lists - 每个轮廓中心点坐标（x, y）
        - top_points: list of lists - 每个轮廓顶部点坐标（x, y）
    """
    contours.sort(key=lambda x: get_contour_center(x)[0])
    radius = [cv2.minEnclosingCircle(contour)[1] for contour in contours]
    diagonal_left = radius[0] * 2
    diagonal_right = radius[1] * 2
    areas = [cv2.contourArea(contour) for contour in contours]

    rects = [cv2.boundingRect(contour) for contour in contours]

    width_left = rects[0][2]
    width_right = rects[1][2]

    height_left = rects[0][3]
    height_right = rects[1][3]

    bridge_width = min(
        abs(rects[0][0] + rects[0][2] - rects[1][0]),
        abs(rects[1][0] + rects[1][2] - rects[0][0]),
    )
    center = [[rect[0] + rect[2] / 2, rect[1] + rect[3] / 2] for rect in rects]

    contours_ = [np.reshape(contour, (-1, 2)) for contour in contours]
    top_points = [contour[np.argmin(contour[:, 1])] for contour in contours_]
    top_points = [point.tolist() for point in top_points]

    return {
        "frame_rects": rects,  # 镜圈轮廓对应的边界框坐标（x,y,w,h）
        "lens_width_left": width_left,  # 左镜圈宽度
        "lens_width_right": width_right,  # 右镜圈宽度
        "lens_height_left": height_left,  # 左镜圈高度
        "lens_height_right": height_right,  # 右镜圈高度
        "lens_diagonal_left": diagonal_left,  # 左镜圈对角线长度
        "lens_diagonal_right": diagonal_right,  # 右镜圈对角线长度
        "bridge_width": bridge_width,  # 鼻梁长度
        "lens_area_left": areas[0],  # 左镜圈面积
        "lens_area_right": areas[1],  # 右镜圈面积
        "lens_center_points": center,  # 镜圈中心点坐标
        "lens_top_points": top_points,  # 镜圈顶部点坐标
    }


def get_parameters_outer(
    image: IMAGE, contours: CONTOURS, center: Sequence[Sequence[int]]
) -> Tuple[dict, dict]:
    """
        获取镜框参数

        params：
            - image: IMAGE - 输入图像，用于获取上下文或进行其他相关操作（根据代码逻辑，该参数在原始代码中未使用，但在此处假设为输入图像）
            - contours: CONTOURS - 待处理的一组轮廓，每个轮廓都是二维点集
            - center: Sequence[Sequence[int]] - 图像中两个关键点的中心坐标

        return：
        - 返回一个字典，包含以下内容：
        - "framework_width": list - 每个部分对应的框架宽度列表
        - "points_correspond": list - 距离顶部参考点最近的轮廓点列表
        - "top_points": list - 两个顶部参考点及其关联信息的列表
    。
    """

    # 镜框高宽
    frameworks, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    frameworks = sorted(frameworks, key=lambda x: cv2.contourArea(x), reverse=True)
    framework = frameworks[0]
    boundingRect = cv2.boundingRect(framework)

    # 桩头位置
    piles_height_left, piles_height_right, distance_up = get_pile_height(
        image, framework
    )

    # (n,1,2)->(n,2)
    contours = [np.reshape(contour, (-1, 2)) for contour in contours]
    # 根据轮廓中心的x坐标对轮廓进行排序
    contours.sort(key=lambda x: get_contour_center(x)[0])

    # 按左右 中心点分为两个部分
    image_parts = [
        image[:, int(center[0][0]) - 5 : int(center[0][0]) + 5],
        image[:, int(center[1][0]) - 5 : int(center[1][0]) + 5],
    ]
    # 眼镜框最上方点
    top_points = [
        [int(center[i][0]), get_first_no_zero(image_parts[i])] for i in range(2)
    ]

    framework_width = []
    points_correspond = []

    # 镜框厚度
    # 遍历每个部分  # 计算每个轮廓点到顶部点的距离
    for i in range(2):
        distances = contours[i] - top_points[i]
        distances = np.linalg.norm(distances, axis=1)
        min_arg = np.argmin(distances)
        point = contours[i][min_arg].tolist()
        points_correspond.append(point)
        framework_width.append(np.linalg.norm(np.array(top_points[i]) - point))

    return {
        "frame_height": boundingRect[3],  # 镜框高度
        "frame_width": boundingRect[2],  # 镜框宽度
        "pile_height_left": piles_height_left,  # 左桩头高度
        "pile_height_right": piles_height_right,  # 右桩头高度
        "frame_top_width": np.mean(framework_width),  # 镜框上边厚度
        "top_points": top_points,  # 镜框左右最高点坐标
    }, {"distance_up": distance_up}
