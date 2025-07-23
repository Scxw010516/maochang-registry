import traceback
import atexit
import numpy as np
import cv2
from contextlib import contextmanager
from typing import Optional
from obs import ObsClient
from django.conf import settings
from django.core.cache import cache

class ObsClientManager:
    """华为云对象存储服务(OBS)客户端管理类"""
    
    def __init__(self):
        # 从设置中获取配置，提供默认值防止异常
        self.access_key = settings.HUAWEI_OBS_CONFIG.get('ACCESS_KEY_ID', None)
        self.secret_key = settings.HUAWEI_OBS_CONFIG.get('SECRET_ACCESS_KEY', None)
        self.server = settings.HUAWEI_OBS_CONFIG.get('ENDPOINT_URL', None)
        self.bucket_name = settings.HUAWEI_OBS_CONFIG.get('BUCKET_NAME', None)
        
        # 验证配置的有效性
        self._validate_config()
        
        # 客户端实例，延迟初始化
        self._client = None
        
        # 缓存设置
        self.cache_ratio = 0.8  # 缓存时间为URL有效期的80%
    
    def _validate_config(self):
        """验证配置是否完整"""
        if not all([self.access_key, self.secret_key, self.server, self.bucket_name]):
            error_msg = "OBS配置不完整，请检查访问密钥、服务器地址和存储桶名称设置"
            raise ValueError(error_msg)
    
    @property
    def client(self):
        """懒加载方式获取 ObsClient 实例"""
        if self._client is None:
            self._client = ObsClient(
                access_key_id=self.access_key,
                secret_access_key=self.secret_key,
                server=self.server
            )
        return self._client
    
    def close(self):
        """关闭 OBS 客户端连接，释放资源"""
        if self._client is not None:
            self._client.close()
            self._client = None
    
    @contextmanager
    def get_client(self):
        """上下文管理器，确保客户端使用完毕后关闭"""
        try:
            yield self.client
        finally:
            pass  # 在此处不关闭连接，因为我们希望复用连接提高性能
    
    def generate_signed_url(self, object_key: Optional[str], expiration: int = 5400) -> Optional[str]:
        """
        生成临时签名的文件访问URL
        :param object_key: 文件在OBS中的对象键（路径）
        :param expiration: URL有效时间，单位为秒，默认5400秒（1.5小时）
        :return: 临时签名的URL或None（生成失败）
        """

        if not object_key:
            return None
            
        try:
            # 检查缓存
            cached_url = cache.get(object_key)
            if cached_url:
                return cached_url

            # 缓存未命中，生成新的签名URL
            with self.get_client() as client:
                response = client.createSignedUrl(
                    method='GET',
                    bucketName=self.bucket_name,
                    objectKey=object_key,
                    expires=expiration
                )
                
            if response.get('signedUrl'):
                signed_url = response['signedUrl']
                # 缓存时间为有效期的80%，确保客户端获取的URL有足够的有效期
                cache_timeout = int(expiration * self.cache_ratio)
                cache.set(object_key, signed_url, timeout=cache_timeout)
                return signed_url
            else:
                return None
        except Exception:
            print(traceback.format_exc())
            return None

    def get_image_object(self, object_key: Optional[str]) -> Optional[bytes]:
        """
        获取图片对象
        :param object_key: 文件在OBS中的对象键（路径）
        :return: 图片对象的字节数据或None（获取失败）
        """
        if not object_key:
            return None
            
        try:
            with self.get_client() as client:
                # 使用loadStreamInMemory=True参数来获取对象内容，将其加载到内存中
                response = client.getObject(
                    bucketName=self.bucket_name,
                    objectKey=object_key,
                    loadStreamInMemory=True
                )
            
            if response.status < 300:
                # 获取成功，使用Opencv读取图片数据
                np_array = np.frombuffer(response.body.buffer, np.uint8)
                img = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
                return img
            else:
                return None
        except Exception:
            print(traceback.format_exc())
            return None

    def get_image_object_raw(self, object_key: Optional[str]) -> Optional[bytes]:
        """
        获取图片对象
        :param object_key: 文件在OBS中的对象键（路径）
        :return: 图片对象的原始字节数据或None（获取失败）
        """
        if not object_key:
            return None
            
        try:
            with self.get_client() as client:
                # 使用loadStreamInMemory=True参数来获取对象内容，将其加载到内存中
                response = client.getObject(
                    bucketName=self.bucket_name,
                    objectKey=object_key,
                    loadStreamInMemory=True
                )
            if response.status< 300:
                # 获取成功，返回图片对象的原始字节数据
                return response.body.buffer
            else:
                return None
        except Exception:
            print(traceback.format_exc())
            return None

    def get_image_object_as_3channel_bytes(self, object_key: Optional[str]) -> Optional[bytes]:
        """
        获取图片对象并强制转换为3通道，然后重新编码为字节数据
        :param object_key: 文件在OBS中的对象键（路径）
        :param format: 输出png图像格式
        :return: 3通道图片的原始字节数据或None（获取失败）
        """
        if not object_key:
            return None
            
        try:
            with self.get_client() as client:
                # 获取原始图片数据
                response = client.getObject(
                    bucketName=self.bucket_name,
                    objectKey=object_key,
                    loadStreamInMemory=True
                )
            
            if response.status < 300:
                # 解码图片
                np_array = np.frombuffer(response.body.buffer, np.uint8)
                img = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
                
                if img is None:
                    return None
                    
                # 转换为3通道
                if len(img.shape) == 2:  # 灰度图
                    img_3channel = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                elif len(img.shape) == 3 and img.shape[2] == 4:  # 4通道图
                    img_3channel = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                elif len(img.shape) == 3 and img.shape[2] == 3:  # 已经是3通道
                    img_3channel = img
                else:
                    # 处理其他情况
                    img_3channel = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                
                # 重新编码为字节数据
                success, encoded_img = cv2.imencode(".png", img_3channel)
                if success:
                    return encoded_img.tobytes()
                else:
                    return None
            else:
                return None
        except Exception:
            print(traceback.format_exc())
            return None

# 创建全局OBS客户端管理器实例
obs_manager = ObsClientManager()

# 为兼容原有代码，提供的便捷函数
def generate_signed_url(object_key: Optional[str], expiration: int = 5400) -> Optional[str]:
    """
    生成临时签名的文件访问URL (兼容原有代码的接口)
    :param object_key: 文件在OBS中的对象键（路径）
    :param expiration: URL有效时间，单位为秒，默认5400秒（1.5小时）
    :return: 临时签名的URL
    """
    return obs_manager.generate_signed_url(object_key, expiration)

def get_image_object(object_key: Optional[str]) -> Optional[bytes]:
    """
    获取图片对象 (兼容原有代码的接口)
    :param object_key: 文件在OBS中的对象键（路径）
    :return: 图片对象的字节数据
    """
    return obs_manager.get_image_object(object_key)

def get_image_object_raw(url: str) -> Optional[bytes]:
    """
    获取图片对象 (兼容原有代码的接口)
    :param object_key: 文件在OBS中的对象键（路径）
    :return: 图片对象的字节数据
    """
    return obs_manager.get_image_object_raw(url)
# 应用退出时关闭连接
atexit.register(obs_manager.close)

def get_image_object_as_3channel_bytes(url: str) -> Optional[bytes]:
    """
    获取图片对象 (兼容原有代码的接口)强制转换为3通道，然后重新编码为字节数据
    :param object_key: 文件在OBS中的对象键（路径）
    :return: 图片对象的字节数据
    """
    return obs_manager.get_image_object_as_3channel_bytes(url)
# 应用退出时关闭连接
atexit.register(obs_manager.close)


if __name__ == "__main__":
    # 测试生成签名URL
    test_object_key = "test/example.jpg"  # 测试用的示例对象键
    try:
        signed_url = generate_signed_url(test_object_key)
        print("签名URL:", signed_url)
        
        # 测试缓存机制是否工作
        cached_url = generate_signed_url(test_object_key)
        print("缓存URL:", cached_url)
        
    except Exception:
        print("生成签名URL时发生错误:", traceback.format_exc())