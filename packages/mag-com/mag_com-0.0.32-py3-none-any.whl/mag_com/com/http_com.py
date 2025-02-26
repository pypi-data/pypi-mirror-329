import requests
from typing import Optional, Dict, Any

from mag_tools.exception.app_exception import AppException
from mag_tools.log.logger import Logger
from mag_tools.utils.data.map_utils import MapUtils


class HttpCom:
    def __init__(self):
        # 初始化一个用于HTTP请求的会话
        self.session = requests.Session()

    def __del__(self):
        # 当对象被销毁时关闭会话
        self.session.close()

    def url(self, url: str) -> Optional[str]:
        # 发送GET请求到指定的URL
        return self.__send(False, url, {}, None, None)

    def get(self, url: str, headers: Dict[str, str] = {}, params: Dict[str, Any] = {}) -> Optional[str]:
        # 发送带有请求头和参数的GET请求
        return self.__send(False, url, headers, params, None)

    def post_with_param(self, url: str, headers: Dict[str, str] = {}, params: Dict[str, Any] = {}) -> Optional[str]:
        # 发送带有请求头和参数的POST请求
        return self.__send(True, url, headers, params, None)

    def post_with_data(self, url: str, headers: Dict[str, str] = {}, data: Optional[str] = None) -> Optional[str]:
        # 发送带有请求头和数据的POST请求
        return self.__send(True, url, headers, None, data)

    def download_to_file(self, url: str, file: str):
        # 从URL下载内容并保存到文件
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        with open(file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def download_to_stream(self, url: str, stream):
        # 从URL下载内容并写入流
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=8192):
            stream.write(chunk)

    def __send(self, is_post: bool, url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]], data: Optional[str]) -> Optional[str]:
        response = None
        try:
            if is_post:
                # 发送POST请求
                response = self.session.post(url, headers=headers, params=params, data=data)
            else:
                # 发送GET请求
                response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            if response is not None:
                res_map = MapUtils.bytes_to_map(response.content)
                Logger.error(f"Request failed: {str(res_map) if res_map else str(e)}")
                raise AppException(res_map.get('error'))
            else:
                Logger.error(f"Request failed: {str(e)}")
                raise e
