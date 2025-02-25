from typing import Any, Dict, Optional, Type

from mag_tools.bean.easy_map import EasyMap
from mag_tools.bean.results import Results
from mag_tools.config.sys_config import SysConfig

from mag_com.bean.password import Password
from mag_com.com.safe_com import SafeCom, T


class MagCom:
    __safe_com: SafeCom = None

    @classmethod
    def post(cls, command: str, body: EasyMap[str,Any], clazz: Type[T]) -> Results:
       return cls.__get_safe_com().post(command, body, clazz)

    @classmethod
    def post_with_params(cls, command: str, params: Dict[str, Any], clazz: Type[T]) -> Results:
        return cls.__get_safe_com().post_with_params(command, params, clazz)

    @classmethod
    def download(cls, command: str, file: str):
        return cls.__get_safe_com().download(command, file)

    @classmethod
    def download_to_stream(cls, command: str, stream):
        return cls.__get_safe_com().download_to_stream(command, stream)

    @classmethod
    def get_password_info(cls, client_id: str, platform_id: Optional[str] = None) -> T:
        params = {
            "clientId": client_id,
            "platformId": platform_id if platform_id else 'Cloud'
        }
        results = cls.post_with_params("password/getPasswordInfo", params, Password)
        return results.first

    @classmethod
    def __get_safe_com(cls) -> SafeCom:
        if cls.__safe_com is None:
            cls.__safe_com = SafeCom()
            cls.__safe_com.init(SysConfig.get_map('server'))

        return cls.__safe_com
