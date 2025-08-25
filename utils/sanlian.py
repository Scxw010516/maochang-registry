import cv2
import os
import tempfile
import requests
import json
import datetime
import random
def get_current_timestamp():
    """
    生成当前时间戳
    
    Returns:
        str: 格式化的时间戳字符串，格式为 "YYYY-MM-DD HH:MM:SS"
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_sanlian_token():
    """
    获取三联的token
    """
    try:
        token_data = {
            "client_id": "SF_inspection",
            "client_secret": "yN8-wA3=oR2^yM1&xJ5;zU4&a",
            "username":"kdA",
            "accountId": "1789897953700315136",
            "nonce": str(random.randint(1000, 9999)),
            "timestamp": get_current_timestamp()  # 自动生成当前时间戳
        }
        response = requests.post(
            "https://sanlianjituan.test.kdcloud.com/kapi/oauth2/getToken", 
            json=token_data,
        )
        print(f"获取三联token响应: {response.json()}")
        # 直接返回token，如果任何环节出错则抛出异常
        if response.json().get("errorCode") != '0':
            raise ValueError("获取三联token失败")
        token = response.json().get("data").get("access_token")
        return token
    except Exception:
        # 重新抛出异常，让调用者处理
        raise

def update_sanlian_eyeglass(token, data):
    """
    更新三联眼镜信息
    """
    try:
        def safe_int(value, default=0):
            """安全地将值转换为整数，如果值为None则返回默认值"""
            if value is None:
                return default
            if type(value) == int:
                return value
            return int(value)

        def safe_str(value, default=""):
            """安全地将值转换为字符串，如果值为None则返回默认值"""
            if value is None:
                return default
            if type(value) == str:
                return value
            return str(value)
        print(data)
        data ={
            "number": safe_str(data["sku"]),
            "createorg_number": "1",
            "shcp_textfield": safe_str(data["brand"]),
            "shcp_model": safe_str(data["model_type"]),
            "shcp_price1": data["price"],
            "shcp_materialquality": safe_str(data["material"]),
            "shcp_color": safe_str(data["color"]),
            "shcp_shape": safe_str(data["shape"]),
            "shcp_nosepad": data["isnosepad"],
            "shcp_stocks": safe_int(data["stock"]),
            "shcp_radian": safe_int(data["lens_radian"]),
            "shcp_width": safe_int(data["lens_width_st"]),
            "shcp_nosepadwidth": safe_int(data["bridge_width_st"]),
            "shcp_leglength": safe_int(data["temple_length_st"]),
            "shcp_weight": safe_int(data["weight"]),
            "shcp_style": ",1,",
            "shcp_frameheight": safe_str(data["frame_height"]),
            "shcp_glass_width": safe_int(data["frame_width"]),
            "shcp_leftpile_heigth": safe_int(data["pile_height_left"]),
            "shcp_rightpile_heigth": safe_int(data["pile_height_right"]),
            "shcp_frame_width": safe_int(data["frame_width"]),
            "shcp_leftring_width": safe_int(data["lens_width_left"]),
            "shcp_rightring_width": safe_int(data["lens_width_right"]),
            "shcp_leftring_heigth": safe_int(data["lens_height_left"]),
            "shcp_rightring_heigth": safe_int(data["lens_height_right"]),
            "shcp_leftring_length": safe_int(data["lens_diagonal_left"]),
            "shcp_rightring_length": safe_int(data["lens_diagonal_right"]),
            "shcp_rightring_area": safe_int(data["lens_area_right"]),
            "shcp_integerfield": safe_int(data["lens_area_left"]),
            "shcp_nosepadwidth1": safe_int(data["bridge_width"]),
            "shcp_lowangle": safe_int(data["vertical_angle"]),
            "shcp_frontangle": safe_int(data["forward_angle"]),
            "shcp_legangle": safe_int(data["temple_angle"]),
            "shcp_anglelength": safe_int(data["drop_length"]),
            "shcp_facecurveness": safe_int(data["face_angle"]),
            "shcp_integerfield3": safe_int(data["sagittal_angle_left"]),
            "shcp_rightlow_angle": safe_int(data["sagittal_angle_right"]),
            "shcp_integerfield1": safe_int(data["temple_length_left"]),
            "shcp_rightleg_length": safe_int(data["temple_length_right"]),
            "shcp_integerfield2": safe_int(data["temporal_width"]),
            "shcp_integerfield4": safe_int(data["spread_angle_left"]),
            "shcp_rightleg_angle": safe_int(data["spread_angle_right"]),
            "shcp_pilelength": safe_int(data["pile_distance"]),
        }
        response = requests.post(
            "https://sanlianjituan.test.kdcloud.com/kapi/v2/shcp/basedata/bd_material/updateSFinfo",
            headers={"Content-Type": "application/json", "accesstoken": token},
            json={"data": data}
        )
        print(f"更新镜架信息响应: {response.json()}")
    except Exception as e:
        print(f"更新镜架信息错误: {e}")
        raise