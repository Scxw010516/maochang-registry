from typing import Sequence, Union, Tuple, List

import cv2
import numpy as np
from cv2 import VideoCapture

CAPTURE = cv2.VideoCapture
IMAGE = np.ndarray


def open_capture(
    devices: Sequence[int] = (0, 1, 2),
    focuses: Sequence[int] = (460, 150, 442),
    exposures: Sequence[int] = (-6, -6, -6),
    brightnesses: Sequence[int] = (0, 0, 0),
) -> Tuple[Sequence[VideoCapture], bool]:
    """
    打开摄像头

    params:
        devices: 摄像头设备号
        focuses: 对焦值
    return:
        caps: 摄像头对象
    """
    # 启动成功
    ret = True
    # 检查参数
    focuses = list(focuses)
    if len(focuses) != len(devices):
        raise ValueError("len(focus) != len(device)")

    # 启用设备
    caps = [cv2.VideoCapture(i, cv2.CAP_DSHOW) for i in devices]
    for i, cap in enumerate(caps):
        # 注释这两行可以加快摄像头启动速度
        # 设置视频格式
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc("M", "J", "P", "G"))
        # # 设置帧率（不一定起作用）
        # ret = cap.set(cv2.CAP_PROP_FPS, 60)
        # 设置宽度（取低一点使opencv自动匹配，增加帧率）
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4650)
        # 设置高度（取低一点使opencv自动匹配，增加帧率）
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3496)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        # 关闭自动曝光
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        # 设置曝光值
        cap.set(cv2.CAP_PROP_EXPOSURE, exposures[i])
        # 此处即为修改相机对焦为手动对焦
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 2)
        # 修改焦点
        cap.set(cv2.CAP_PROP_FOCUS, focuses[i])
        # 修改亮度
        cap.set(cv2.CAP_PROP_BRIGHTNESS, brightnesses[i])

    if not all([cap.isOpened() for cap in caps]):
        ret = False

    return caps, ret


def init_capture(
    caps: Sequence[CAPTURE], wait_time: int = 10
) -> tuple[Sequence[VideoCapture], bool]:
    """
    初始化摄像头，调整焦点

    params:
        caps: 摄像头对象
        wait_time: 等待时间
    return:
        caps: 摄像头对象
    """
    # 等待,否则得到的图片可能会为全黑，仅启动后需要，若未关闭则不需要
    ret = True
    cv2.waitKey(wait_time)
    # 相机首次打开调整焦点，否则焦点会不正常
    focuses = [cap.get(cv2.CAP_PROP_FOCUS) for cap in caps]
    focuses = [focus - 50 for focus in focuses]
    for i, cap in enumerate(caps):
        cap.set(cv2.CAP_PROP_FOCUS, focuses[i])
    cv2.waitKey(wait_time)
    focuses = [focus + 50 for focus in focuses]
    for i, cap in enumerate(caps):
        cap.set(cv2.CAP_PROP_FOCUS, focuses[i])

    if not all([cap.isOpened() for cap in caps]):
        ret = False

    return caps, ret


def close_capture(caps: Sequence[CAPTURE]):
    """
    关闭摄像头

    params:
        caps: 摄像头对象
    """
    for cap in caps:
        cap.release()


def rotate_image(image: IMAGE, rotate: int) -> IMAGE:

    if rotate == 0:
        return image
    else:
        rotate_list = [
            cv2.ROTATE_90_CLOCKWISE,
            cv2.ROTATE_180,
            cv2.ROTATE_90_COUNTERCLOCKWISE,
        ]
        return cv2.rotate(image, rotate_list[rotate] - 1)


def get_image(
    caps: Sequence[CAPTURE], rotates: Sequence[int] = (0, 0, 0)
) -> tuple[Union[Sequence[IMAGE], Sequence[None]], bool]:
    """
    获取图像

    params:
        caps: 摄像头对象
        isShow: 是否显示图像
    return:
        frames: 图像
    """
    # 返回图像
    ret = True
    if all([cap.isOpened() for cap in caps]):
        frames = [cap.read()[1] for cap in caps]
        frames = [rotate_image(frame, rotate) for frame, rotate in zip(frames, rotates)]
    else:
        frames = [None for _ in caps]
        ret = False
    # 判断摄像头是否断开
    if any([cap.get(cv2.CAP_PROP_HUE) for cap in caps]):
        ret = False
    return frames, ret
