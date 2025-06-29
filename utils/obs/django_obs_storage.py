import os
import posixpath
from obs import PutObjectHeader
from django.core.files import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.conf import settings
from django.utils.encoding import force_str

from .obs_client import obs_manager

@deconstructible
class HuaweiOBSStorage(Storage):
    """
    华为云对象存储服务(OBS)的Django存储后端
    用于替代默认的FileSystemStorage，将文件存储到华为云OBS
    """
    
    def __init__(self):
        """
        初始化OBS存储
        
        :param bucket_name: OBS存储桶名称，如不提供则使用settings中的默认值
        :param location: 文件存储的基本路径，类似文件系统中的目录
        """
        self.bucket_name = settings.HUAWEI_OBS_CONFIG.get('BUCKET_NAME', None) # OBS桶名称
        self.access_key_id = settings.HUAWEI_OBS_CONFIG.get('ACCESS_KEY_ID', None) # 访问密钥ID
        self.secret_access_key = settings.HUAWEI_OBS_CONFIG.get('SECRET_ACCESS_KEY', None) # 访问密钥
        self.endpoint_url = settings.HUAWEI_OBS_CONFIG.get('ENDPOINT_URL', None) # 终端节点
        self.region_name = settings.HUAWEI_OBS_CONFIG.get('REGION_NAME', None) # 区域名称
        
    def _normalize_name(self, name):
        """
        标准化文件名，确保文件名是有效的OBS对象键
        
        :param name: 原始文件名
        :return: 标准化后的文件名
        """
        # 删除开头的/或./
        name = name.lstrip('./\\')
            
        # 规范化路径分隔符
        return name.replace('\\', '/')
    
    def _save(self, name, content):
        """
        保存文件到OBS
        
        :param name: 保存的文件名
        :param content: 文件内容（一个File对象）
        :return: 保存后的文件名
        """
        name = self._normalize_name(name)
        headers = PutObjectHeader()
        headers.contentType = getattr(content, 'content_type', 'application/octet-stream')
        
        # 读取文件内容
        if hasattr(content, 'chunks'):
            file_content = b''.join(chunk for chunk in content.chunks())
        else:
            content.seek(0)
            file_content = content.read()
        
        # 上传到OBS
        try:
            with obs_manager.get_client() as client:
                resp = client.putObject(
                    bucketName=self.bucket_name,
                    objectKey=name,
                    content=file_content,
                    headers=headers
                )
            
            if resp.status >= 300:
                raise IOError(f"上传文件到OBS失败: {resp.errorCode} - {resp.errorMessage}")
                
            return name
        except Exception as e:
            raise IOError(f"上传文件到OBS时发生错误: {str(e)}")
    
    def exists(self, name):
        """
        检查文件是否存在于OBS中
        
        :param name: 文件名
        :return: 如果文件存在返回True，否则返回False
        """
        name = self._normalize_name(name)
        
        try:
            with obs_manager.get_client() as client:
                resp = client.getObjectMetadata(
                    bucketName=self.bucket_name,
                    objectKey=name
                )
                
            return resp.status < 300
        except Exception:
            return False

    def url(self, name):
        """
        获取文件的URL
        
        :param name: 文件名
        :return: 文件的URL
        """
        name = self._normalize_name(name)
        return obs_manager.generate_signed_url(name)

    def _open(self, name, mode='rb'):
        """
        打开文件,返回一个File对象
        
        :param name: 文件名
        :param mode: 打开模式
        :return: 文件对象
        """
        name = self._normalize_name(name)
        
        try:
            with obs_manager.get_client() as client:
                resp = client.getObject(
                    bucketName=self.bucket_name,
                    objectKey=name,
                    loadStreamInMemory=True
                )
                
            if resp.status >= 300:
                raise IOError(f"打开文件失败: {resp.errorCode} - {resp.errorMessage}")
                
            return File(resp.body.buffer)
        except Exception as e:
            raise IOError(f"打开文件时发生错误: {str(e)}")

    def delete(self, name):
        """
        删除文件
        
        :param name: 文件名
        """
        name = self._normalize_name(name)
        
        try:
            with obs_manager.get_client() as client:
                resp = client.deleteObject(
                    bucketName=self.bucket_name,
                    objectKey=name,
                    versionId='null'
                )
                
            if resp.status >= 300:
                raise IOError(f"删除文件失败: {resp.errorCode} - {resp.errorMessage}")
                
        except Exception as e:
            raise IOError(f"删除文件时发生错误: {str(e)}")
    

# 默认OBS存储实例，可以在Django设置中配置
obs_storage = HuaweiOBSStorage()
