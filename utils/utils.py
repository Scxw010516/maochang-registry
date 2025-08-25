import os
import re
import time
from typing import Optional
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, HttpRequest
from urllib.parse import urljoin

from config.env import IMAGE_URL, IMAGE_PATH, TEMP_PATH, ATTACHMENT_PATH
from utils.file import mkdir
from utils.jwts import parse_payload
from utils.obs.obs_client import generate_signed_url


# 获取用户ID
def uid(request):
    # 从请求头中获取token值
    access_token = request.headers['Authorization']
    # 字符串替换
    access_token = access_token.replace('Bearer ', "")
    # JWT解密
    result = parse_payload(access_token)
    # 结果标识
    code = result['code']
    if code != 0:
        return 0
    # 用户ID
    userId = result['data']['userId']
    # 返回结果
    return userId


# 判断变量类型的函数
def typeof(value):
    type = None
    if isinstance(value, int):
        type = "int"
    elif isinstance(value, str):
        type = "str"
    elif isinstance(value, float):
        type = "float"
    elif isinstance(value, list):
        type = "list"
    elif isinstance(value, tuple):
        type = "tuple"
    elif isinstance(value, dict):
        type = "dict"
    elif isinstance(value, set):
        type = "set"
    return type


# 返回变量类型
def getType(value):
    arr = {"int": "整数", "float": "浮点", "str": "字符串", "list": "列表", "tuple": "元组", "dict": "字典", "set": "集合"}
    vartype = typeof(value)
    if not (vartype in arr):
        return "未知类型"
    return arr[vartype]


# 获取图片地址
# def getImageURL(path):
#     return urljoin(IMAGE_URL, path)

def getImageURL(request: HttpRequest,path:Optional[str]):
    # 生成签名URL
    return generate_signed_url(path)


def saveImage(url, dirname):
    # 判断文件地址是否为空
    if not url:
        return "文件地址不能为空"
    # 判断是否是本站图片
    if url.find(IMAGE_URL) != -1:
        # 本站图片
        if url.find("temp") != -1:
            # 临时图片
            path = IMAGE_PATH + "/" + dirname + "/" + time.strftime('%Y%m%d')
            # 创建存储目录
            mkdir(path)
            # 原始图片地址
            oldPath = url.replace(IMAGE_URL, ATTACHMENT_PATH)
            # 目标目录地址
            newPath = IMAGE_PATH + "/" + dirname + oldPath.replace(TEMP_PATH, "")
            # 移动文件
            os.rename(oldPath, newPath)
            # 返回结果
            return newPath.replace(ATTACHMENT_PATH, "")
        else:
            # 非临时图片
            return url.replace(IMAGE_URL, "")
    else:
        # 远程图片
        print("远程图片处理")
    # 返回空字符串
    return ""


# 保存富文本内容
def saveEditContent(content, title, dirname):
    # 正则取出富文本图片地址
    urlList = re.findall('img src="(.*?)"', content, re.S)
    # 遍历图片地址
    for url in urlList:
        # 保存图片至本地
        image = saveImage(url, dirname)
        if image:
            content = content.replace(url, "[IMG_URL]" + image)

    # 设置alt标题
    if content.find("alt=\"\"") and title != "":
        content = content.replace("alt=\"\"", "alt=\"" + title + "\"")
    # 返回结果
    return content

# 获取全局计算状态
def getGlobalCalculationState(item):
    all_calculate_state = 3
    if not item:
        all_calculate_state = 3
    try:
        # 修改访问方式，支持字典和对象
        def get_state(attr):
            if isinstance(item, dict):
                return item.get(attr, 0)
            else:
                return getattr(item, attr, 0)
        
        if (
            get_state('pixel_measurement_state') == 2 and
            get_state('millimeter_measurement_state') == 2 and
            get_state('calculation_state') == 2 and
            get_state('coordinate_state') == 2 and
            get_state('image_mask_state') == 2 and
            get_state('image_seg_state') == 2 and
            get_state('image_beautify_state') == 2
        ):
            # 当所有计算都成功时，计算状态为计算成功
            all_calculate_state = 2
        elif (
            get_state('pixel_measurement_state') == 1 or
            get_state('millimeter_measurement_state') == 1 or
            get_state('calculation_state') == 1 or
            get_state('coordinate_state') == 1 or
            get_state('image_mask_state') == 1 or
            get_state('image_seg_state') == 1 or
            get_state('image_beautify_state') == 1
        ):
            # 当有一个为计算中时，计算状态为计算中
            all_calculate_state = 1
        elif (
            get_state('pixel_measurement_state') == 0 or
            get_state('millimeter_measurement_state') == 0 or
            get_state('calculation_state') == 0 or
            get_state('coordinate_state') == 0 or
            get_state('image_mask_state') == 0 or
            get_state('image_seg_state') == 0 or
            get_state('image_beautify_state') == 0
        ):
            # 当有一个为待计算时，计算状态为待计算
            all_calculate_state = 0
    except Exception as e:
        all_calculate_state = 3   
        print(e)
    return all_calculate_state

