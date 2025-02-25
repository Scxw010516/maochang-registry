import os

import cv2
import numpy as np
from tqdm import tqdm


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


def get_files(path, ext=(".png",)):
    if isinstance(ext, str):
        ext = (ext,)
    files = []

    for root, dirs, fs in os.walk(path):
        for filename in fs:
            files.append(os.path.join(root, filename))

    files = [f for f in files if os.path.splitext(f)[1] in ext]
    return files


def nose_transparent(image, nose, alpha=0.05):
    blank = np.zeros(image.shape[:2], dtype=np.uint8)
    blank[426:1450, 1100:2124] = nose
    image[:, :, 3][blank == 1] = int(255 * alpha)
    return image


def extract_sku_list(path):
    with open(path, "r") as f:
        data = f.readlines()
    return [line.strip() for line in data]


def main():
    nose_path = "D:/Project/glasses_label_nose/temp2_mask/"
    # frame_path = "D:/Project/temp/mask/frame/"
    sku_list = extract_sku_list("sku_list.txt")
    # print(len(sku_list))
    ps_path = "D:/Project/temp/ps/"
    save_path = "D:/Project/temp/ps2_nose/"
    files = get_files(nose_path)
    loop = tqdm(files)
    for fl in loop:
        sku = get_sku(fl)
        if sku in sku_list:
            continue
        nose = cv2.imread(fl, cv2.IMREAD_GRAYSCALE)
        image = cv2.imread(os.path.join(ps_path, sku + "_1.png"), cv2.IMREAD_UNCHANGED)
        image = nose_transparent(image, nose, 40)
        save_image(os.path.join(save_path, sku + "_1.png"), image)


if __name__ == "__main__":
    main()

    # skus = [get_sku(f) for f in files]
    # frames = [os.path.join(frame_path, sku + "_1.png") for sku in skus]
