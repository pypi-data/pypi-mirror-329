from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import hashlib
import base64

from mag_tools.exception.app_exception import AppException
from mag_tools.utils.security.password_utils import PasswordUtils


@dataclass
class Password:
    user_sn: Optional[int] = field(default=None, metadata={"description": "用户序号"})
    hash: Optional[str] = field(default=None, metadata={"description": "密码：登录密码+Salt的N次哈希值，N为hashCount"})
    secret: Optional[str] = field(default=None, metadata={"description": "密钥"})
    hash_count: Optional[int] = field(default=None, metadata={"description": "登录密码+Salt的哈希次数"})
    salt: Optional[str] = field(default=None, metadata={"description": "登录密码盐(Base64编码)"})
    make_time: datetime = field(default_factory=datetime.now, metadata={"description": "密码生成时间"})
    error_count: int = field(default=0, metadata={"description": "密码错误次数"})
    next_change_time: Optional[datetime] = field(default=None, metadata={"description": "下次修改密码时间"})

    @staticmethod
    def init(password: str) -> 'Password':
        """
        根据密码文本初始化一个Password密码
        :param password: 密码文本
        :return: Password密码
        """
        salt = PasswordUtils.make_salt()
        hash_count = PasswordUtils.make_initial_hash_times()
        hash_value = PasswordUtils.sha256_password(password, salt, hash_count)
        return Password(salt=salt, hash_count=hash_count, hash=hash_value)

    def verify_password(self, hash_of_n_1: str) -> bool:
        """
        验证密码是否通过
        :param hash_of_n_1: 密码+Salt的N-1次哈希(十六进制)
        :return: 是否通过验证
        """
        return self.verify_password_with_alg(hash_of_n_1, 'sha256')

    def verify_password_with_alg(self, hash_of_n_1: str, alg: str) -> bool:
        """
        验证密码是否通过
        :param hash_of_n_1: 密码+Salt的N-1次哈希(十六进制)
        :param alg: 哈希算法
        :return: 是否通过验证
        """
        try:
            self.check_password()
            ba_hash_of_n_1 = base64.b16decode(hash_of_n_1.upper())
            ba_hash_of_n = hashlib.new(alg, ba_hash_of_n_1).digest()
            is_ok = base64.b16encode(ba_hash_of_n).decode().lower() == self.hash
        except AppException:
            is_ok = False

        if is_ok:
            self.hash = hash_of_n_1
            self.hash_count -= 1
            self.error_count = 0
        else:
            self.error_count += 1

        return is_ok

    def verify_secret(self, crypt_password_encoder, secret: str) -> bool:
        """
        验证密钥是否匹配
        :param crypt_password_encoder: 密钥加密器
        :param secret: 密钥
        :return: 是否匹配
        """
        is_ok = crypt_password_encoder.verify(secret, self.secret)
        self.error_count = 0 if is_ok else self.error_count + 1
        return is_ok

    def check_password(self):
        """
        检查密码是否规范
        """
        if not self.hash:
            raise ValueError("密码的摘要不能为空")
        if not self.salt:
            raise ValueError("密码的SALT不能为空")
        if self.hash_count < 1000:
            raise ValueError("密码的Hash次数不能太小")
        if self.hash_count > 10000000:
            raise ValueError("密码的Hash次数不宜太大")

    def check_secret(self):
        """
        检查密钥是否规范
        """
        if not self.secret:
            raise ValueError("密钥不能为空")
        if len(self.secret) < 8:
            raise ValueError("密钥长度不能小于8")

    def encode_password(self, password_encoder):
        """
        加密密钥
        如密钥存在，则替换为加密格式；如不存在，则忽略
        """
        if self.secret:
            self.secret = password_encoder.encode(self.secret)

    def is_empty(self) -> bool:
        """
        判定密码是否为空
        只要密码+Salt的哈希值、Salt或哈希次数有一个为空，则密码为空
        """
        return (not self.hash or not self.hash.strip() or
                not self.salt or not self.salt.strip() or
                self.hash_count is None) and self.secret is None