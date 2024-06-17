# -- coding: utf-8 --

import sys
import time

import cv2
import numpy as np

# from windows_toasts import Toast, WindowsToaster

# sys.path.append(r"F:\python project\maochang-recommendation\face")
# from MvImport.MvCameraControl_class import *

sys.path.append("../mvs/")
from mvs.MvCameraControl_class import *


def VALUE(_type):
    value = _type()
    memset(byref(value), 0, sizeof(value))
    return value


def Enum_device(tlayerType, deviceList):
    """
    ch:枚举设备 | en:Enum device
    nTLayerType [IN] 枚举传输层 ，pstDevList [OUT] 设备列表
    """
    ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
    if ret != 0:
        print("enum devices fail! ret[0x%x]" % ret)
        sys.exit()

    if deviceList.nDeviceNum == 0:
        print("find no device!")
        # sys.exit()
    # deviceList: CameraParams_header._MV_CC_DEVICE_INFO_LIST_
    # print([a for a in dir(deviceList) if not a.startswith("__")])
    # # print(len(deviceList.pDeviceInfo))
    # print(
    #     [
    #         a
    #         for a in dir(deviceList.pDeviceInfo[0].contents.SpecialInfo.stGigEInfo)
    #         if not a.startswith("__")
    #     ]
    # )
    # print(deviceList.pDeviceInfo[0].contents.SpecialInfo.stGigEInfo.nCurrentIp)
    for i in range(deviceList.nDeviceNum):
        for j in range(deviceList.nDeviceNum - i - 1):
            mvcc_dev_info = [
                cast(deviceList.pDeviceInfo[j], POINTER(MV_CC_DEVICE_INFO)).contents,
                cast(
                    deviceList.pDeviceInfo[j + 1], POINTER(MV_CC_DEVICE_INFO)
                ).contents,
            ]
            if (
                mvcc_dev_info[0].SpecialInfo.stGigEInfo.nCurrentIp
                > mvcc_dev_info[1].SpecialInfo.stGigEInfo.nCurrentIp
            ):
                temp = mvcc_dev_info[0]
                deviceList.pDeviceInfo[j].contents = mvcc_dev_info[1]
                deviceList.pDeviceInfo[j + 1].contents = temp
    # deviceList.sort(key=lambda x:)
    # print(dir(deviceList))

    print("Find %d devices!" % deviceList.nDeviceNum)

    for i in range(0, deviceList.nDeviceNum):
        mvcc_dev_info = cast(
            deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)
        ).contents
        if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
            print("\ngige device: [%d]" % i)
            # 输出设备名字
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                if per == 0:
                    break
                strModeName = strModeName + chr(per)
            print(f"device model name: {strModeName}")
            # 输出设备ID
            nip1 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xFF000000) >> 24
            nip2 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00FF0000) >> 16
            nip3 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000FF00) >> 8
            nip4 = mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000FF
            print("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
        # 输出USB接口的信息
        elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
            print("\nu3v device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                if per == 0:
                    break
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
            print("user serial number: %s" % strSerialNumber)


def enable_device(nConnectionNum, deviceList):
    """
    设备使能
    :param nConnectionNum: 设备编号
    :return: 相机, 图像缓存区, 图像数据大小
    """
    # ch:创建相机实例 | en:Creat Camera Object
    # (exposure_time_us,) = paras
    cam = MvCamera()

    # ch:选择设备并创建句柄 | en:Select device and create handle
    # cast(typ, val)，这个函数是为了检查val变量是typ类型的，但是这个cast函数不做检查，直接返回val
    stDeviceList = cast(
        deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)
    ).contents

    ret = cam.MV_CC_CreateHandle(stDeviceList)
    if ret != 0:
        print("create handle fail! ret[0x%x]" % ret)
        sys.exit()

    # ch:打开设备 | en:Open device
    ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
    if ret != 0:
        print("open device fail! ret[0x%x]" % ret)
        sys.exit()

    # 获取图像格式
    # cam.MV_CC_SetEnumValue("PixelFormat", PixelType_Gvsp_RGB8_Packed)

    # Set the pixel format (replace PixelType_Gvsp_RGB8_Packed with the actual format)
    if cam.MV_CC_SetEnumValue("PixelFormat", PixelType_Gvsp_RGB8_Packed) != 0:
        print("Error: Unable to set the pixel format.")
        exit()

    # Set exposure time (replace ExposureTime_us with the desired exposure time value)
    # exposure_time_us = 5000  # For example, 10 milliseconds
    # if cam.MV_CC_SetFloatValue("ExposureTime", exposure_time_us) != 0:
    #     print("Error: Unable to set exposure time.")
    #     exit()

    # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
    if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
        nPacketSize = cam.MV_CC_GetOptimalPacketSize()
        if int(nPacketSize) > 0:
            ret = cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
            if ret != 0:
                print("Warning: Set Packet Size fail! ret[0x%x]" % ret)
        else:
            print("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)

    # ch:设置触发模式为off | en:Set trigger mode as off
    ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
    if ret != 0:
        print("set trigger mode fail! ret[0x%x]" % ret)
        sys.exit()

    # 从这开始，获取图片数据
    # ch:获取数据包大小 | en:Get payload size
    stParam = MVCC_INTVALUE()
    memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))
    # MV_CC_GetIntValue，获取Integer属性值，handle [IN] 设备句柄
    # strKey [IN] 属性键值，如获取宽度信息则为"Width"
    # pIntValue [IN][OUT] 返回给调用者有关相机属性结构体指针
    # 得到图片尺寸，这一句很关键
    # payloadsize，为流通道上的每个图像传输的最大字节数，相机的PayloadSize的典型值是(宽x高x像素大小)，此时图像没有附加任何额外信息
    ret = cam.MV_CC_GetIntValue("PayloadSize", stParam)
    if ret != 0:
        print("get payload size fail! ret[0x%x]" % ret)
        sys.exit()

    nPayloadSize = stParam.nCurValue

    # ch:开始取流 | en:Start grab image
    ret = cam.MV_CC_StartGrabbing()
    if ret != 0:
        print("start grabbing fail! ret[0x%x]" % ret)
        sys.exit()
    #  返回获取图像缓存区。
    data_buf = (c_ubyte * nPayloadSize)()
    #  date_buf前面的转化不用，不然报错，因为转了是浮点型
    return cam, data_buf, nPayloadSize


def get_image(data_buf, nPayloadSize, cam):
    """
    获取图像
    :param data_buf:
    :param nPayloadSize:
    :return: 图像
    """
    # 输出帧的信息
    stFrameInfo = MV_FRAME_OUT_INFO_EX()
    # void *memset(void *s, int ch, size_t n);
    # 函数解释:将s中当前位置后面的n个字节 (typedef unsigned int size_t )用 ch 替换并返回 s
    # memset:作用是在一段内存块中填充某个给定的值，它是对较大的结构体或数组进行清零操作的一种最快方法
    # byref(n)返回的相当于C的指针右值&n，本身没有被分配空间
    # 此处相当于将帧信息全部清空了
    memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))

    # 采用超时机制获取一帧图片，SDK内部等待直到有数据时返回，成功返回0
    ret = cam.MV_CC_GetOneFrameTimeout(data_buf, nPayloadSize, stFrameInfo, 1000)
    if ret == 0:
        # print(
        #     "get one frame: Width[%d], Height[%d], nFrameNum[%d]"
        #     % (stFrameInfo.nWidth, stFrameInfo.nHeight, stFrameInfo.nFrameNum)
        # )
        pass
    else:
        print("no data[0x%x]" % ret)

    image = np.asarray(data_buf)  # 将c_ubyte_Array转化成ndarray得到（3686400，）

    image = image.reshape(
        (stFrameInfo.nHeight, stFrameInfo.nWidth, -1)
    )  # 根据自己分辨率进行转化
    return image


def close_device(cam, data_buf):
    """
    关闭设备
    :param cam:
    :param data_buf:
    """
    # ch:停止取流 | en:Stop grab image
    ret = cam.MV_CC_StopGrabbing()
    if ret != 0:
        print("stop grabbing fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()

    # ch:关闭设备 | Close device
    ret = cam.MV_CC_CloseDevice()
    if ret != 0:
        print("close deivce fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()

    # ch:销毁句柄 | Destroy handle
    ret = cam.MV_CC_DestroyHandle()
    if ret != 0:
        print("destroy handle fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()
    # global cams
    # cams = {}
    del data_buf


def capture(deviceIndex):
    # 获得设备信息
    deviceList = MV_CC_DEVICE_INFO_LIST()
    tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE

    # ch: 枚举设备 | en:Enum device
    # nTLayerType[IN] 枚举传输层 ，pstDevList[OUT] 设备列表
    Enum_device(tlayerType, deviceList)
    # print(deviceList)
    count = 1
    exposure_obj = VALUE(MVCC_FLOATVALUE)
    exposure_time_us = 90000
    rotate = 0
    height, width = 1080, 1920
    # exposure_auto = 1
    # 获取相机和图像数据缓存区
    cam, data_buf, nPayloadSize = enable_device(deviceIndex, deviceList)  # 选择设备
    cam.MV_CC_SetFloatValue("ExposureTime", exposure_time_us)
    cam.MV_CC_SetIntValue("width", width)
    cam.MV_CC_SetIntValue("height", height)
    # cam.MV_CC_SetEnumValue("ExposureMode", MV_EXPOSURE_AUTO_MODE_OFF)
    while True:
        image = get_image(data_buf, nPayloadSize, cam)
        # print(image.shape, flush=True)
        image = cv2.cvtColor(
            image, cv2.COLOR_BGR2RGB
        )  # 默认是BRG，要转化成RGB，颜色才正常
        # 旋转图像
        if rotate == 0:
            pass
        elif rotate == 1:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif rotate == 2:
            image = cv2.rotate(image, cv2.ROTATE_180)
        elif rotate == 3:
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        image_text = image.copy()
        # exposure_time = VALUE(MVCC_FLOATVALUE)
        cam.MV_CC_GetFloatValue("ExposureTime", exposure_obj)
        exposure_time_us = exposure_obj.fCurValue
        cv2.putText(
            image_text,
            f"exposure: {exposure_time_us} us",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 255, 0),
            5,
        )
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.imshow("image", image_text)
        key = cv2.waitKeyEx(1)
        if key == ord("q") or key == 27:  # 按Esc或q退出
            cv2.destroyAllWindows()
            break
        elif key == ord("s") or key == 32:  # 按s或空格保存图片，秒级时间戳
            t = time.time()
            save_path = f"../images/background_{deviceIndex}.jpg"
            cv2.imwrite(save_path, image)
            words = f"第{count}张图片保存成功！时间：{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())},保存路径：{save_path}"
            print(
                words,
                flush=True,
            )
            # import datetime
            # DELETE: 删除toast通知
            # toaster = WindowsToaster("Python")
            # newToast = Toast()

            # newToast.text_fields = [words]
            # newToast.on_activated = lambda _: print("Toast clicked!")
            # toaster.show_toast(newToast)
            count += 1
            # break
        elif key == 2490368:  # 按上下调节曝光
            exposure_time_us += max(int(exposure_time_us / 100 * 0.1), 1) * 100
            cam.MV_CC_SetFloatValue("ExposureTime", exposure_time_us)
        elif key == 2621440:
            exposure_time_us -= max(int(exposure_time_us / 100 * 0.1), 1) * 100
            cam.MV_CC_SetFloatValue("ExposureTime", exposure_time_us)
        elif key == 2555904:
            rotate = (rotate + 1) % 4
        elif key == 2424832:
            rotate = (rotate - 1) % 4
        elif key == ord("e"):
            nRet = cam.MV_CC_SetEnumValue(
                "ExposureAuto", 1
            )  # 0：off 1：once 2：Continuous
            if MV_OK != nRet:
                print(f"Set ExposureAuto fail nRet [0x{nRet}]!", flush=True)
            else:  # 只有自动曝光或者自动增益开启后，Brightness亮度值方可设置
                nRet = cam.MV_CC_SetIntValue("Brightness", 160)
                if nRet != MV_OK:
                    print(f"Set BrightnessRet [0x{nRet}]!")
            time.sleep(1)
            cam.MV_CC_GetFloatValue("ExposureTime", exposure_obj)
            exposure_time_us = exposure_obj.fCurValue
            nRet = cam.MV_CC_SetEnumValue("ExposureAuto", 0)

    # 关闭设备
    close_device(cam, data_buf)

def capture_clean(deviceIndex,rotate:int=0,exposure:int=30000):
    # 获得设备信息
    deviceList = MV_CC_DEVICE_INFO_LIST()
    tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE

    # ch: 枚举设备 | en:Enum device
    # nTLayerType[IN] 枚举传输层 ，pstDevList[OUT] 设备列表
    Enum_device(tlayerType, deviceList)
    # print(deviceList)
    exposure_time_us = exposure
    # exposure_auto = 1
    # 获取相机和图像数据缓存区
    cam, data_buf, nPayloadSize = enable_device(deviceIndex, deviceList)  # 选择设备
    cam.MV_CC_SetFloatValue("ExposureTime", exposure_time_us)
    t1 = time.time()
    # cam.MV_CC_SetEnumValue("ExposureMode", MV_EXPOSURE_AUTO_MODE_OFF)
    while True:
        image = get_image(data_buf, nPayloadSize, cam)
        # print(image.shape, flush=True)
        image = cv2.cvtColor(
            image, cv2.COLOR_BGR2RGB
        )  # 默认是BRG，要转化成RGB，颜色才正常
        # 旋转图像
        if rotate == 0:
            pass
        elif rotate == 1:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif rotate == 2:
            image = cv2.rotate(image, cv2.ROTATE_180)
        elif rotate == 3:
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        if time.time() - t1>1:
            close_device(cam, data_buf)
            return image
            # cv2.imwrite(save_path, image)
        # exposure_time = VALUE(MVCC_FLOATVALUE)
    # 关闭设备


cams = {}
deviceList = MV_CC_DEVICE_INFO_LIST()
tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
Enum_device(tlayerType, deviceList)


def init_capture(deviceIndex: int,exposure:int=30000):
    global cams, deviceList, tlayerType
    cams[deviceIndex] = {}
    cams[deviceIndex]['exposure_obj'] = VALUE(MVCC_FLOATVALUE)
    exposure_time_us = exposure
    cams[deviceIndex]['rotate'] = 0
    cams[deviceIndex]['cam'], cams[deviceIndex]['data_buf'], cams[deviceIndex]['nPayloadSize'] = enable_device(deviceIndex, deviceList)  # 选择设备
    ret3 = cams[deviceIndex]['cam'].MV_CC_SetFloatValue("ExposureTime", exposure_time_us)
    cams[deviceIndex]['cam'].MV_CC_SetIntValueEx("Width", 2448)
    ret2 = cams[deviceIndex]['cam'].MV_CC_SetIntValueEx("Height", 2048)
    cams[deviceIndex]['cam'].MV_CC_SetEnumValue("DecimationHorizontal", 2)
    ret = cams[deviceIndex]['cam'].MV_CC_SetEnumValue("DecimationVertical", 2)

    ret4 = cams[deviceIndex]['cam'].MV_CC_SetFloatValue("AcquisitionFrameRate", 8.0)
    # cams[deviceIndex]['cam'].MV_CC_SetEnumValue("PixelFormat", PixelType_Gvsp_YUV422_YUYV_Packed)
    # print(ret, ret2, ret3, ret4)


def release_capture(deviceIndex: int):
    global cams
    close_device(cams[deviceIndex]["cam"], cams[deviceIndex]["data_buf"])


def next_frame(deviceIndex: int,rotate: int=0):
    global cams
    image = get_image(
        cams[deviceIndex]["data_buf"],
        cams[deviceIndex]["nPayloadSize"],
        cams[deviceIndex]["cam"],
    )
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if rotate == 0:
        pass
    elif rotate == 1:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif rotate == 2:
        image = cv2.rotate(image, cv2.ROTATE_180)
    elif rotate == 3:
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return image


def capture_and_save(deviceIndex, path,name:str='capture'):
    deviceList = MV_CC_DEVICE_INFO_LIST()
    tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
    Enum_device(tlayerType, deviceList)
    count = 1
    exposure_obj = VALUE(MVCC_FLOATVALUE)
    exposure_time_us = 90000
    cam, data_buf, nPayloadSize = enable_device(deviceIndex, deviceList)  # 选择设备
    image = get_image(data_buf, nPayloadSize, cam)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 默认是BRG，要转化成RGB，颜色才正常
    image_text = image.copy()
    cam.MV_CC_GetFloatValue("ExposureTime", exposure_obj)
    exposure_time_us = exposure_obj.fCurValue
    cv2.putText(
        image_text,
        f"exposure: {exposure_time_us} us",
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
    )
    t = time.time()
    save_path = f"{path}/{name}_{int(t)}.jpg"
    cv2.imwrite(save_path, image)
    words = f"{count}保存成功！时间：{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())},保存路径：{save_path}"
    print(
        words,
        flush=True,
    )
    close_device(cam, data_buf)
    return save_path

def get_face(deviceIndex: int):
    global cams
    image = get_image(cams[deviceIndex]['data_buf'], cams[deviceIndex]['nPayloadSize'], cams[deviceIndex]['cam'])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cams[deviceIndex]['cam'], cams[deviceIndex]['data_buf'], cams[deviceIndex]['nPayloadSize'] = enable_device(deviceIndex, deviceList)  # 选择设备
    cams[deviceIndex]['cam'].MV_CC_SetEnumValue("DecimationHorizontal", 2)
    cams[deviceIndex]['cam'].MV_CC_SetEnumValue("DecimationVertical", 2)
    name = "del_" + str(deviceIndex) + ".jpg"
    cv2.imwrite(name, image)

if __name__ == "__main__":
    # for i in range(3):
    #     capture(i)
    capture(2)
