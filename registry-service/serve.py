import asyncio
import json
import traceback

import cv2, time
import numpy as np
from websockets.server import serve
import api.capture_usb as capture
from api.weight import (
    read_weight_,
    reset_weight_,
    open_serial_,
    close_serial_,
    detect_weight_port,
)
from PyCameraList.camera_device import list_video_devices

from api.configs import server as server_cfg
from api.up_main import calc_up
from api.front_main import calc_front
from api.left_main import calc_left
from api.get_size import get_size
from api.utils import draw_dash_line


# 秤串口
ser = None
# 秤串口号
WEIGHT_COM = 5
# 重量
weight = 0.0


# 摄像头
caps = []
# 支持的摄像头设备名称
support_device_names = server_cfg["support_device_names"]
# 摄像头初始顺序（俯、正、侧）
devices = server_cfg["devices"]
# 旋转图像
rotates = server_cfg["rotates"]
# 摄像头曝光（俯、正、侧）
exposures = server_cfg["exposures"]
# 焦点（俯、正、侧）
focuses = server_cfg["focuses"]
# 图片裁剪区域(y1,x1,y2,x2)
crop_front = server_cfg["crop_front"]
crop_up = server_cfg["crop_up"]
crop_left = server_cfg["crop_left"]
auto_order = server_cfg["auto_order"]
brightnesses = server_cfg["brightnesses"]

# 重写print
rewrite_print = print
log = f"log/log_{int(time.time())}.txt"


def print(*arg):
    # 获取log的文件名，若没有就新建文件，并将文件名返回

    rewrite_print(*arg)  # 打印到控制台

    with open(log, "a", encoding="utf-8") as f:
        rewrite_print(*arg, file=f)  # 写入文件


def default_dump(obj):
    """Convert numpy classes to JSON serializable objects."""
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


async def read_weight(websocket):
    global ser, weight
    if not ser or not ser.is_open:
        ser, ret = await open_serial_(WEIGHT_COM)
        if not ret:
            await websocket.send(json.dumps({"code": -1, "data": None}))
            return
    while websocket.open:
        try:
            if ser.is_open:
                try:
                    weight = await read_weight_(ser)
                except:
                    await websocket.send(
                        json.dumps({"code": -1, "data": None}, default=default_dump)
                    )
                    return
                await websocket.send(
                    json.dumps(
                        {"code": 0, "data": str(weight)},
                        default=default_dump,
                    )
                )
                await asyncio.sleep(1.0 / 24)
        except:
            print("Connection closed")
            break


async def reset_weight(websocket):
    global ser
    if not ser or not ser.is_open:
        ser, ret = await open_serial_(WEIGHT_COM)
        if not ret:
            await websocket.send(
                json.dumps({"code": -1, "data": None}, default=default_dump)
            )
            return
    await reset_weight_(ser)
    await websocket.send(json.dumps({"code": 0, "data": None}, default=default_dump))


async def log_weight(websocket):
    global ser
    if not ser or not ser.is_open:
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    close_serial_(ser)
    await websocket.send(json.dumps({"code": 0, "data": None}, default=default_dump))


async def detect_weight(websocket):
    global WEIGHT_COM, ser
    # 识别秤串口
    if ser and ser.is_open:
        close_serial_(ser)
    print("开始自动识别串口")
    temp_com = detect_weight_port()
    if temp_com != -1:
        WEIGHT_COM = temp_com
        print(f"自动识别串口成功。串口号：{WEIGHT_COM}")
        ser, ret = await open_serial_(WEIGHT_COM)
        if not ret:
            await websocket.send(
                json.dumps({"code": -1, "data": None}, default=default_dump)
            )
        await websocket.send(
            json.dumps({"code": 0, "data": None}, default=default_dump)
        )
    else:
        print(f"未识别到串口。采用默认串口号：{WEIGHT_COM}")
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )


# 下面两个函数，算摄像头顺序
def calculate_phash(img_path):
    """
    计算给定图像的感知哈希值。
    :param image_path: 图像文件路径
    :return: 8x8的二进制矩阵，代表感知哈希值
    """
    # 打开图像并调整大小为32x32，转换为灰度
    img = cv2.imread(img_path)
    img = cv2.resize(img, (32, 32))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 将图像转为numpy数组，并进行DCT变换
    img_array = np.array(img, dtype=np.float32)
    dct = cv2.dct(img_array)
    dct = cv2.dct(dct)

    # 将DCT系数缩放，只保留低频部分
    dct_low_freq = dct[:8, :8]

    # 计算平均值，用于后续的二值化
    avg = np.mean(dct_low_freq)

    # 二值化处理，大于平均值设为1，否则为0
    hash_matrix = dct_low_freq > avg

    # 将二值矩阵转换为整数表示的哈希值
    return hash_matrix.astype(int)


def hamming_distance(hash1, hash2):
    """
    计算两个感知哈希值之间的汉明距离。
    :param hash1: 一个感知哈希矩阵
    :param hash2: 另一个感知哈希矩阵
    :return: 汉明距离，即不同位的数量
    """
    return np.count_nonzero(hash1 != hash2)


# 摄像头预览
async def camera_usb(websocket, cam_id: int):
    global caps
    # 摄像头未打开报错
    if len(caps) == 0:
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    cap = caps[cam_id]
    rotate = rotates[cam_id]
    # 判断摄像头是否全部打开
    if not cap.isOpened():
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    while websocket.open:
        images, ret = capture.get_image([cap], rotates=[rotate])
        # 判断获取图像是否成功
        if not ret:
            await websocket.send(
                json.dumps({"code": -1, "data": None}, default=default_dump)
            )
            return
        if cam_id == 0:
            image = draw_dash_line(
                images[0], (3250, 500), (3250, 3100), (0, 0, 200), 10, gap=50
            )
            _, encoded = cv2.imencode(".jpg", image)
        else:
            _, encoded = cv2.imencode(".jpg", images[0])
        await websocket.send(encoded.tobytes())
        await asyncio.sleep(1.0 / 24)


# 摄像头拍摄
async def capture_usb(websocket, cam_id: int):
    global caps
    # 摄像头未打开报错
    if len(caps) == 0:
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    cap = caps[cam_id]
    rotate = rotates[cam_id]
    images, ret = capture.get_image([cap], rotates=[rotate])
    # 判断获取图像是否成功
    if not ret:
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    save_path = f"./images/capture_{cam_id}.jpg"
    _, encoded = cv2.imencode(".jpg", images[0])
    open(save_path, "wb").write(encoded.tobytes())
    await websocket.send(encoded.tobytes())


# 摄像头拍摄背景
async def capture_bg_usb(websocket):
    global caps
    # 摄像头未打开报错
    if len(caps) == 0:
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    # 清除摄像头图片缓存
    capture.get_image(caps, rotates=rotates)
    # 拍摄背景
    images, ret = capture.get_image(caps, rotates=rotates)
    # 判断获取图像是否成功
    if not ret:
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
    else:
        # 拍摄三张背景
        for i in range(3):
            save_path = f"./images/background_{i}.jpg"
            _, encoded = cv2.imencode(".jpg", images[i])
            open(save_path, "wb").write(encoded.tobytes())
        # 计算参数
        data = calc_frame()
        await websocket.send(
            json.dumps({"code": 0, "data": data}, default=default_dump)
        )


# 摄像头初始化
async def init_camera_usb(websocket):
    global caps, devices, focuses, exposures, rotates, brightnesses
    # 获取所有摄像头设备
    cameras = list_video_devices()
    print(cameras)
    indices = [camera[0] for camera in cameras if camera[1] in support_device_names]
    # （去除内部摄像头设备）
    if len(indices) == 3:
        devices_actual = tuple(indices[i] for i in devices)
    else:
        print("摄像头设备数量不足")
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    print("摄像头顺序：", devices_actual)

    # 摄像头warm up，防止焦点错误
    caps, ret = capture.open_capture(
        devices_actual, focuses, exposures=exposures, brightnesses=brightnesses
    )
    if not ret:
        print("预热-摄像头打开失败")
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    caps, ret = capture.init_capture(caps, wait_time=500)
    if not ret:
        print("预热-摄像头初始化失败")
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    capture.get_image(caps, rotates=rotates)
    capture.close_capture(caps)
    print(
        "摄像头预热完成。 时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    )

    # 正式启动
    caps, ret = capture.open_capture(
        devices_actual, focuses, exposures=exposures, brightnesses=brightnesses
    )
    if not ret:
        print("预热-摄像头启动失败")
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    print(
        f"摄像头启动成功。时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
    )
    caps, ret = capture.init_capture(caps, wait_time=500)
    if not ret:
        print("摄像头初始化失败")
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )
        return
    print(
        f"摄像头初始化完成。时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
    )
    capture.get_image(caps, rotates=rotates)

    if auto_order == 1:
        # 拍摄背景
        images, ret = capture.get_image(caps, rotates=rotates)
        # 判断获取图像是否成功

        # 拍摄三张背景
        for i in range(3):
            save_path = f"./temp/background_{i}.jpg"
            _, encoded = cv2.imencode(".jpg", images[i])
            open(save_path, "wb").write(encoded.tobytes())

        hash_c = [calculate_phash(f"temp/background_{i}.jpg") for i in range(3)]
        hash_s = [calculate_phash(f"standard/background_{i}.jpg") for i in range(3)]
        distances = [
            [hamming_distance(hash_c[i], hash_s[j]) for i in range(3)] for j in range(3)
        ]

        indices = np.argmin(distances, axis=1)

        devices_actual = [devices_actual[indices[i]] for i in range(3)]

        capture.close_capture(caps)

        caps, ret = capture.open_capture(
            devices_actual, focuses, exposures=exposures, brightnesses=brightnesses
        )
        if not ret:
            print("预热-摄像头启动失败")
            await websocket.send(
                json.dumps({"code": -1, "data": None}, default=default_dump)
            )
            return
        print(
            f"摄像头启动成功。时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        )
        caps, ret = capture.init_capture(caps, wait_time=500)
        if not ret:
            print("摄像头初始化失败")
            await websocket.send(
                json.dumps({"code": -1, "data": None}, default=default_dump)
            )
            return
        print(
            f"摄像头初始化完成。时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        )
        capture.get_image(caps, rotates=rotates)

    # 打印摄像头焦点和曝光信息
    focuses_p = [cap.get(cv2.CAP_PROP_FOCUS) for cap in caps]
    print(f"焦点：{focuses_p}")
    exposure_p = [cap.get(cv2.CAP_PROP_EXPOSURE) for cap in caps]
    print(f"曝光：{exposure_p}")
    brightness_p = [cap.get(cv2.CAP_PROP_BRIGHTNESS) for cap in caps]
    print(f"亮度：{brightness_p}")

    # 释放摄像头
    capture.close_capture(caps)

    await websocket.send(json.dumps({"code": 0, "data": None}, default=default_dump))


# 下面两个调整曝光值的
async def light_up(websocket, cam_id: int):
    global brightnesses
    try:
        cap = caps[cam_id]
        b = cap.get(cv2.CAP_PROP_BRIGHTNESS)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, b + 10)
        print(f"Brightness: {cap.get(cv2.CAP_PROP_BRIGHTNESS)}")
        brightnesses_list = list(brightnesses)

        brightnesses_list[cam_id] = cap.get(cv2.CAP_PROP_BRIGHTNESS)
        brightnesses = tuple(brightnesses_list)
        await websocket.send(
            json.dumps({"code": 0, "data": None}, default=default_dump)
        )
    except:
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )


async def light_down(websocket, cam_id: int):
    global brightnesses
    try:
        cap = caps[cam_id]
        b = cap.get(cv2.CAP_PROP_BRIGHTNESS)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, b - 10)
        print(f"Brightness: {cap.get(cv2.CAP_PROP_BRIGHTNESS)}")
        brightnesses_list = list(brightnesses)

        brightnesses_list[cam_id] = cap.get(cv2.CAP_PROP_BRIGHTNESS)
        brightnesses = tuple(brightnesses_list)

        await websocket.send(
            json.dumps({"code": 0, "data": None}, default=default_dump)
        )
    except:
        await websocket.send(
            json.dumps({"code": -1, "data": None}, default=default_dump)
        )


# 清除摄像头预览缓存
async def clear_camera_cache():
    global caps
    capture.get_image(caps, rotates=rotates)


# 疑似没用到
async def load_captured(websocket, cam_id: int):
    img = open(f"./images/capture_{cam_id}.jpg", "rb")
    await websocket.send(img.read())


async def load_background(websocket, cam_id: int):
    img = open(f"./images/background_{cam_id}.jpg", "rb")
    await websocket.send(img.read())


# 计算参数的代码
def calc_frame():
    front_path = "./images/capture_1.jpg"
    up_path = "./images/capture_0.jpg"
    left_path = "./images/capture_2.jpg"
    front_bg_path = "./images/background_1.jpg"
    up_bg_path = "./images/background_0.jpg"
    left_bg_path = "./images/background_2.jpg"
    # 返回错误码
    flags = [1, 1, 1]
    # 标定距离
    distances = {"distance_left": 919, "distance_front": 1493.5, "distance_up": 1805.0}
    try:
        up_params, distance_part = calc_up(up_path, up_bg_path, crop=crop_up)
        distances = {**distances, **distance_part}
    except Exception as e:
        print(f"出现如下异常：{e}")
        traceback.print_exc()
        flags[0] = 0
        up_params = {
            "face_angle": -1,  # 面弯
            "sagittal_angle_left": -1,  # 左垂内角
            "sagittal_angle_right": -1,  # 右垂内角
            "temple_length_left": -1,  # 左镜腿长度
            "temple_length_right": -1,  # 右镜腿长度
            "temporal_width": -1,  # 颞距
            "spread_angle_left": -1,  # 左镜腿外张角
            "spread_angle_right": -1,  # 右镜腿外张角
            "pile_distance": -1,
        }

    try:
        front_params, distance_part = calc_front(
            front_path, front_bg_path, crop=crop_front
        )
        distances = {**distances, **distance_part}
    except Exception as e:
        print(f"出现如下异常：{e}")
        traceback.print_exc()
        flags[1] = 0
        front_params = {
            "frame_rects": [
                [-1, -1, -1, -1],
                [-1, -1, -1, -1],
            ],  # 镜圈轮廓对应的边界框坐标（x,y,w,h）
            "lens_width_left": -1,  # 左镜圈宽度
            "lens_width_right": -1,  # 右镜圈宽度
            "lens_height_left": -1,  # 左镜圈高度
            "lens_height_right": -1,  # 右镜圈高度
            "lens_diagonal_left": -1,  # 左镜圈对角线长度
            "lens_diagonal_right": -1,  # 右镜圈对角线长度
            "lens_area_left": -1,  # 左镜圈面积
            "lens_area_right": -1,  # 右镜圈面积
            "bridge_width": -1,  # 鼻梁长度
            "lens_center_points": [[-1, -1], [-1, -1]],  # 镜圈中心点坐标
            "lens_top_points": [[-1, -1], [-1, -1]],  # 镜圈顶部点坐标
            "frame_height": -1,  # 镜框高度
            "frame_width": -1,  # 镜框宽度
            "pile_height_left": -1,  # 左桩头高度
            "pile_height_right": -1,  # 右桩头高度
            "frame_top_width": -1,  # 镜框上边厚度
            "top_points": -1,  # 镜框左右最高点坐标
        }

    try:
        left_params = calc_left(left_path, left_bg_path, crop=crop_left)
    except Exception as e:
        print(f"出现如下异常：{e}")
        traceback.print_exc()
        flags[2] = 0
        left_params = {
            "vertical_angle": -1,  # 垂俯角
            "forward_angle": -1,  # 前倾角
            "temple_angle": -1,  # 镜腿角
            "drop_length": -1,  # 垂长
        }
    if flags[0]:
        up_params = get_size(up_params, distances)
    print("俯视参数计算完成。")
    if flags[1]:
        front_params = get_size(front_params, distances)
    print("正视参数计算完成。")
    if flags[2]:
        left_params = get_size(left_params, distances)
    print("侧视参数计算完成。")
    return {"flag": 1 if all(flags) else 0, **front_params, **up_params, **left_params}


# 以下是websocket路由配置，和启动命令
class PathSolver:
    def __init__(self, ws, route_prefix: str, callback):
        self.route_prefix = route_prefix
        self.callback = callback
        self.ws = ws

    async def solve(self, path: str):
        if path.startswith(self.route_prefix):
            print(f"solved by: {self.route_prefix}")
            await self.callback(self.ws, int(path.replace(self.route_prefix, "")))


async def WSServer(websocket, path: str):
    print(f"routing for: {path}")
    await PathSolver(websocket, "/load-captured/", load_captured).solve(path)
    await PathSolver(websocket, "/load-background/", load_background).solve(path)
    await PathSolver(websocket, "/camera-usb/", camera_usb).solve(path)
    await PathSolver(websocket, "/capture-usb/", capture_usb).solve(path)
    await PathSolver(websocket, "/light-up/", light_up).solve(path)
    await PathSolver(websocket, "/light-down/", light_down).solve(path)
    await PathSolver(websocket, "/log-weight/", log_weight).solve(path)

    if path == "/hello":
        await websocket.send("hello")
    if path == "/read-weight":
        await read_weight(websocket)
    if path == "/log-weight":
        await log_weight(websocket)
    if path == "/reset-weight":
        await reset_weight(websocket)
    if path == "/init-weight":
        await detect_weight(websocket)
    if path == "/calc-frame":
        await capture_bg_usb(websocket)
    if path == "/init-camera-usb":
        await init_camera_usb(websocket)
    if path == "/clear-camera-cache":
        await clear_camera_cache()


def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    print(f"Caught exception: {msg}")


loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)


async def main():
    print("服务端已启动...")

    async with serve(WSServer, "localhost", 8765):
        await asyncio.Future()


asyncio.run(main())
