import json
from dataclasses import dataclass, field
from urllib.parse import urljoin

import requests
from typing import Optional, Dict, Any, Type, TypeVar

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from mag_tools.utils.data.map_utils import MapUtils
from mag_tools.bean.easy_map import EasyMap
from mag_tools.bean.results import Results
from mag_tools.jsonparser.json_parser import JsonParser
from mag_tools.model.client_type import ClientType
from mag_tools.model.user_type import UserType
from mag_com.com.http_com import HttpCom

T = TypeVar('T')

@dataclass
class SafeCom:
    __inited: bool = False
    __session: Session = None
    __host: Optional[str] = None
    __port: Optional[int] = None
    __service_id: Optional[str] = None
    __client_type: Optional[ClientType] = ClientType.WINDOWS
    __user_type: Optional[UserType] = UserType.PERSON
    __app_id: Optional[str] = None
    __is_ssl: bool = False
    __headers: Dict[str, str] = field(default_factory=lambda:{
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        })

    def init(self, prop: Dict[str, Any]):
        self.__session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.__session.mount('http://', HTTPAdapter(max_retries=retries))

        self.__host = prop.get("host", "")
        self.__port = prop.get("port", 80)
        self.__service_id = prop.get("service_id", "")
        self.__is_ssl = prop.get("ssl", False)
        self.__client_type = ClientType.of_code(prop.get("clientType", "Windows"))
        self.__user_type = UserType.of_code(prop.get("userType", "Person"))
        self.__app_id = prop.get("appId", "")

        if not self.__host or self.__port <= 0:
            self.__inited = False
            raise Exception("未设置服务器地址")
        self.__inited = True

    def post(self, command: str, body: EasyMap[str,Any], clazz: Optional[Type[T]]) -> Optional[Results]:
        if not self.__inited:
            raise Exception("SafeCom not initialized")

        url = self.__get_url(command)
        self.__headers["Content-Type"] = "application/json"

        try:
            body_map = body.keys_to_hump()

            response_str = HttpCom().post_with_data(url, self.__headers, JsonParser.from_bean(body_map))
            return JsonParser.to_results(response_str, clazz)
        except requests.RequestException as e:
            return Results.fail(str(e))

    def post_with_params(self, command: str, params: Dict[str, Any], clazz: Optional[Type[T]]) -> Optional[Results[T]]:
        if not self.__inited:
            raise Exception("SafeCom not initialized")

        url = self.__get_url(command)
        self.__headers["Content-Type"] = "application/x-www-form-urlencoded"

        try:
            response_str = HttpCom().post_with_param(url, self.__headers, params)
            return JsonParser.to_results(response_str, clazz)
        except requests.RequestException as e:
            return Results.fail(str(e))

    def download(self, command: str, file: str):
        if not self.__inited:
            raise Exception("SafeCom not initialized")

        url = self.__get_url(command)

        response = self.__session.get(url, stream=True)
        response.raise_for_status()

        with open(file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def download_to_stream(self, command: str, stream):
        if not self.__inited:
            raise Exception("SafeCom not initialized")

        url = self.__get_url(command)

        response = self.__session.get(url, stream=True)
        response.raise_for_status()

        for chunk in response.iter_content(chunk_size=8192):
            stream.write(chunk)

    def add_header(self, key: str, value: str):
        self.__headers[key] = value

    def erase_header(self, key: str):
        if key in self.__headers:
            del self.__headers[key]

    # @property
    # def client_type(self) -> ClientType:
    #     return self.__client_type
    #
    # @property
    # def user_type(self) -> UserType:
    #     return self.__user_type
    #
    # @property
    # def app_id(self) -> str:
    #     return self.__app_id

    def __get_url(self, command: str) -> str:
        protocol = "https" if self.__is_ssl else "http"
        base_url = f"{protocol}://{self.__host}:{self.__port}/"

        return urljoin(base_url, command)