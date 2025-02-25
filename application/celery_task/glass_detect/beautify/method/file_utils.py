import os
import shutil

import cv2


def get_files(path, ext=(".png",)):
    if isinstance(ext, str):
        ext = (ext,)
    files = []

    for root, dirs, fs in os.walk(path):
        for filename in fs:
            files.append(os.path.join(root, filename))
    if ext is not None:
        files = [f for f in files if os.path.splitext(f)[1] in ext]
    return files


def get_sku(file_path):
    # 返回sku
    sku = os.path.basename(file_path).split("_")[0]
    return sku


def save_image(path, image):
    """
    保存图像到指定路径，如果路径不存在则创建。

    参数:
    image: 图像数据 (numpy.ndarray)
    path: 图像保存的完整路径包括文件名，如 './images/new_image.jpg'
    """
    # 分离路径和文件名
    directory, filename = os.path.split(path)

    # 检查目录是否存在，如果不存在，则创建
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 使用OpenCV保存图像
    cv2.imwrite(path, image)


def copy(src, dst, force=True):
    if not force and os.path.exists(dst):
        return
    path = os.path.dirname(dst)
    try:
        os.makedirs(path)
    except FileExistsError:
        pass

    shutil.copy(src, dst)
