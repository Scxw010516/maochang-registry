import time
from typing import Union, Tuple

import serial
from serial import Serial
from serial.tools import list_ports
import asyncio

from .configs import weight as weight_cfg

WEIGHT_SERIAL_NUMBERS = weight_cfg["WEIGHT_SERIAL_NUMBERS"]


def Open_Serial(
    port: int,
) -> Tuple[Union[Serial, None], bool]:
    port_str = f"COM{port}"
    # global ser
    # 打开串口, COM11, 4800 波特率, 8 数据位, 0 停止位
    try:
        ser = serial.Serial(
            port_str,
            9600,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
        )
    except serial.SerialException as e:
        print(e)
        return None, False
    # print("串口已打开")
    # 检查串口是否已经打开
    if ser.is_open:
        print("串口已成功打开.")
        return ser, True
    else:
        print("串口打开失败.")
        return None, False


def Read_Weight(ser: serial.Serial) -> float:  # 读取重量
    # 要发送的数据
    data_to_send = [0x01, 0x03, 0x00, 0x50, 0x00, 0x02, 0xC4, 0x1A]
    # 将数据转换为字节串并发送
    ser.write(bytes(data_to_send))
    # 读取数据包, 分字节和功能读取, 数据位为2 字节
    address = ser.read(3)  # 清楚缓存
    weight = ser.read(4)  # 读取重量数据（2 字节）
    # 将字节串转换为整数
    # 重量计算
    # 将重量数据转换为有符号的十进制数

    weight = weight.hex()

    decimal = int(weight, 16)
    # 因为是32位补码表示，检查是否需要转换为负数
    if decimal >= 2**31:
        decimal -= 2**32

    # 打印接收到的数据
    # print("重量: {} ".format(weight))
    ser.read(2)
    time.sleep(0.8)  # 休眠1秒
    return decimal


def Close_Serial(ser: serial.Serial):  # 关闭串口
    ser.close()
    print("串口已关闭")


def Set_Zero(ser: serial.Serial):  # 设置零点

    # 要发送的数据
    data_to_send = [0x01, 0x10, 0x00, 0x5E, 0x00, 0x01, 0x02, 0x00, 0x01, 0x6A, 0xEE]

    # 将数据转换为字节串并发送
    ser.write(bytes(data_to_send))

    time.sleep(0.3)
    ser.read(8)
    time.sleep(0.5)


def Set_Range(ser: serial.Serial, value: int):  # 设置量程
    # a = int(input("请输入你想修改到的量程"))
    b = "{:08x}".format(value)  # 将输入的十进制数转化为四个两位十六进制数
    str1 = int("0x" + b[0:2], 16)
    str2 = int("0x" + b[2:4], 16)
    str3 = int("0x" + b[4:6], 16)
    str4 = int("0x" + b[6:8], 16)
    # 要发送的数据
    data_to_send = [
        0x01,
        0x10,
        0x00,
        0x56,
        0x00,
        0x02,
        0x04,
        str1,
        str2,
        str3,
        str4,
        0x6C,
        0x85,
    ]
    # 将数据转换为字节串并发送
    ser.write(bytes(data_to_send))
    time.sleep(0.1)  # 休眠0.1秒


def Set_Judge_Time(ser: serial.Serial, value: int):  # 输入判稳时间，最大65535ms
    # a = input("请输入你想修改到的判稳时间,最大65535ms")
    b = "{:04x}".format(value)  # 将输入的十进制数转化为四个两位十六进制数
    str1 = int("0x" + b[0:2], 16)
    str2 = int("0x" + b[2:4], 16)
    # 要发送的数据
    data_to_send = [0x01, 0x10, 0x00, 0x63, 0x00, 0x01, 0x02, str1, str2, 0x2F, 0xC4]
    # 将数据转换为字节串并发送
    ser.write(bytes(data_to_send))
    time.sleep(0.1)  # 休眠0.1秒


def Set_Graduation(
    ser: serial.Serial, value: float
):  # 分度值设置 0x0C:1 0x09:0.1  0x0F:10
    # a = input("请输入你想修改的分度值,输入1/0.1/10")
    if value == 1:
        data_to_send = [
            0x01,
            0x10,
            0x00,
            0x58,
            0x00,
            0x01,
            0x02,
            0x00,
            0x0C,
            0x6B,
            0x4E,
        ]
        # 将数据转换为字节串并发送
        ser.write(bytes(data_to_send))
        time.sleep(0.1)  # 休眠0.1秒
    elif value == 0.1:
        data_to_send = [
            0x01,
            0x10,
            0x00,
            0x58,
            0x00,
            0x01,
            0x02,
            0x00,
            0x09,
            0x6B,
            0x4E,
        ]
        # 将数据转换为字节串并发送
        ser.write(bytes(data_to_send))
        time.sleep(0.1)  # 休眠0.1秒
    elif value == 10:
        data_to_send = [
            0x01,
            0x10,
            0x00,
            0x58,
            0x00,
            0x01,
            0x02,
            0x00,
            0x0F,
            0x6B,
            0x4E,
        ]
        # 将数据转换为字节串并发送
        ser.write(bytes(data_to_send))
        time.sleep(0.1)  # 休眠0.1秒


async def read_weight_(ser: serial.Serial):
    if not ser:
        print("串口未打开, 无法读取重量。")
        return float(-1.0)
    weight = Read_Weight(ser) / 10
    print(f"重量：{weight} g, 当前时间:{time.ctime()}")
    # Close_Serial(ser)
    await asyncio.sleep(0.1)  # 休眠0.1秒
    return weight


async def reset_weight_(ser: serial.Serial):
    # ser = Open_Serial(num)
    if not ser:
        print("串口未打开, 无法置零。")
    else:
        Set_Zero(ser)
        # Close_Serial(ser)
        await asyncio.sleep(0.1)


async def open_serial_(COM: int):
    ser, ret = Open_Serial(COM)
    await asyncio.sleep(0.1)
    if not ret:
        print("串口打开失败.")
    return ser, ret


def detect_weight_port():
    port_list = list(list_ports.comports())
    port_list = [port for port in port_list if port.serial_number]
    for port in port_list:
        if port.serial_number in WEIGHT_SERIAL_NUMBERS:
            device = port.device
            return int(device[3:])
    else:
        device_list = [int(port.device[3:]) for port in port_list]
        # print(device_list)
        for d in device_list:
            try:
                ser, flag = Open_Serial(d)
                if ser:
                    device = d
                    ser.close()
                    return device
            except serial.serialutil.SerialException:
                continue
    return -1


def close_serial_(ser):
    Close_Serial(ser)
    return
