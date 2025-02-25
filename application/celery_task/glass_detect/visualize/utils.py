import numpy as np


def get_angle(point1, point2):
    """
    计算线段AB与x轴的夹角，返回角度值（单位：度）
    :param x1: 点A的x坐标
    :param y1: 点A的y坐标
    :param x2: 点B的x坐标
    :param y2: 点B的y坐标
    :return: 线段AB与x轴的夹角（单位：度）
    """
    # 计算方向向量
    x1, y1 = point1
    x2, y2 = point2
    dx = x2 - x1
    dy = y2 - y1

    # 使用numpy的arctan2函数计算弧度值
    angle_radians = np.arctan2(dy, dx)

    # 将弧度转换为度
    angle_degrees = np.degrees(angle_radians)
    if angle_degrees == -180:
        return 180

    return -angle_degrees


def angle2theta(angle):
    """
    将角度转换为theta
    :param angle: 角度值
    :return: theta值
    """
    return angle / 180 * np.pi


def theta2angle(theta):
    """
    将theta转换为角度
    :param theta: theta值
    :return: 角度值
    """
    return theta / np.pi * 180


def format_points(points, mode=0):
    """
    将点对齐，方便进行距离表示
    :param points: points
    :param mode: 对齐的方式，0：水平位置对齐，1：高度对齐
    :return:
    """
    if mode == 0:
        point1 = points[0]
        point2 = [points[0][0], points[1][1]]
    elif mode == 1:
        point1 = points[0]
        point2 = [points[1][0], points[0][1]]
    else:
        raise ValueError("mode must be 0 or 1")
    return point1, point2


if __name__ == "__main__":
    print(get_angle((0, 0), (1, 1)))
