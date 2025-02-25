import cv2
import numpy as np
from skimage.morphology import skeletonize

from .blend import normal


def get_contours(mask):
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )  # 全部轮廓
    contours_inner = [
        contours[i] for i in range(len(contours)) if hierarchy[0][i][3] != -1
    ]  # 内部轮廓
    contours_outer = [
        contours[i] for i in range(len(contours)) if hierarchy[0][i][3] == -1
    ]
    contours_lens = sorted(contours_inner, key=cv2.contourArea, reverse=True)[
        :2
    ]  # 镜片轮廓
    contours_lens = sorted(contours_lens, key=lambda x: x[0][0][0])  # 左右排序
    contours_frame = sorted(contours_outer, key=cv2.contourArea, reverse=True)[:1]
    return contours_frame, contours_lens


def draw_contour(contours, image=None, size=(1600, 3200), width=1, inner=False):
    temp = np.zeros(size) if image is None else image
    mask = np.zeros(size)
    if not isinstance(contours, list):
        contours = [contours]
    cv2.fillPoly(mask, contours, 255)
    cv2.drawContours(temp, contours, -1, 255, width * 2)

    if inner:
        temp[mask == 0] = 0
    else:
        temp[mask != 0] = 0
    return temp


def enhance_depth(
    glasses,
    mask,
    lens_opacity=0.15,
    frame_opacity=0.2,
    lens_width=10,
    frame_width=-1,
    lens_color=(221, 221, 221),
    frame_color=(221, 221, 221),
):
    if frame_width == -1:
        # 根据边框宽度自适应宽度
        distances = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
        skeleton = skeletonize(mask).astype(np.uint8)
        distances[skeleton == 0] = 0
        nonzero = distances[distances > 0]
        frame_width = int(np.median(nonzero) / 3)
    # print("frame_width:", frame_width)
    contours_frame, contours_lens = get_contours(mask)
    depth_frame_mask = draw_contour(
        contours=contours_frame,
        size=mask.shape[:2],
        width=frame_width,
        inner=True,
    )
    depth_frame_mask = draw_contour(
        contours=contours_lens,
        image=depth_frame_mask,
        size=mask.shape[:2],
        width=frame_width,
        inner=False,
    )
    depth_lens_mask = draw_contour(
        contours=contours_lens,
        size=mask.shape[:2],
        width=lens_width,
        inner=True,
    )
    depth_frame = np.zeros((*mask.shape[:2], 4), dtype=np.uint8)
    depth_lens = np.zeros((*mask.shape[:2], 4), dtype=np.uint8)
    depth_frame[depth_frame_mask > 0] = [*(frame_color), 255]
    depth_lens[depth_lens_mask > 0] = [*(lens_color), 255]
    glasses = normal(glasses, depth_lens, lens_opacity)
    glasses = normal(glasses, depth_frame, frame_opacity)
    return glasses
    # show(depth_frame)


def show(image: np.ndarray):
    temp = image.copy()
    if len(image.shape) == 3 and image.shape[2] == 4:
        temp = temp[:, :, :3]
    elif len(image.shape) == 2:
        temp = temp * 255 if np.max(temp) <= 1 else temp
    temp = temp.astype(np.uint8)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", temp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test():
    # mask = cv2.imread("D:/Project/utils/ps/mask.png", cv2.IMREAD_UNCHANGED)
    foreground = cv2.imread("D:/Project/utils/ps/foreground.png", cv2.IMREAD_UNCHANGED)
    mask = foreground[:, :, 3]
    g = enhance_depth(glasses=foreground, mask=mask)
    cv2.imwrite("D:/Project/utils/ps/ret.png", g)


if __name__ == "__main__":
    test()
    test()
    test()
