from typing import Optional
import os

from Crypto.Cipher import PKCS1_OAEP

from .cipher_base import CipherBase
from .rsa_cipher import RSACipher
from .aes_cipher import GCMAESCipher
from .data_encoder import RawDataEncoder
from .data_encoder import DataEncoderBase
from .result_encoder import ResultEncoderBase
from .result_encoder import Utf8ResultEncoder
from .result_encoder import Base64ResultEncoder

__all__ = [
    "RESCipher",
]


class RESCipher(CipherBase):
    """RSA+AES加解密器。

    加密过程：
        1）随机生成256位（32字节）数据加密密钥tmpkey。
        2）将tmpkey使用RSACipher和公钥进行加密，得到tmpkey加密结果。
        3）将数据使用GCMCipher和tmpkey进行加密，得到data加密结果
        4）使用点号连接tmpkey加密结果和data加密结果，得到最终加密结果：tmpkey加密结果 + "." + data加密结果

    注意：
        1）加密时初始化参数password表示公钥。
        2）解密时初始化参数password表示私钥。
        3）RSACipher默认使用PKCS1_OAEP封装。
    """

    default_rsa_cipher_module = PKCS1_OAEP
    default_result_encoder = Utf8ResultEncoder
    tmp_key_size: int = 32

    def __init__(
        self,
        password: str,
        passphrase: Optional[str] = None,
        data_encoder: Optional[DataEncoderBase] = None,
        result_encoder: Optional[ResultEncoderBase] = None,
        rsa_cipher_module=None,
    ):
        super().__init__(
            password=password,
            data_encoder=data_encoder,
            result_encoder=result_encoder,
        )
        self.passphrase = passphrase
        self.rsa_cipher_module = rsa_cipher_module or self.default_rsa_cipher_module

    def do_encrypt(self, data: bytes) -> bytes:
        tmpkey = os.urandom(self.tmp_key_size)
        tmpkey_cipher = RSACipher(
            password=self.password,
            data_encoder=RawDataEncoder,
            result_encoder=Base64ResultEncoder,
        )
        tmpkey_cipher_text = tmpkey_cipher.encrypt(tmpkey)
        data_cipher = GCMAESCipher(
            password=tmpkey,
            data_encoder=RawDataEncoder,
            result_encoder=Base64ResultEncoder,
        )
        data_cipher_text = data_cipher.encrypt(data)
        return ".".join([tmpkey_cipher_text, data_cipher_text]).encode("utf-8")

    def do_decrypt(self, data: bytes) -> bytes:
        data = data.decode("utf-8")
        tmpkey_cipher_text, data_cipher_text = data.split(".")
        tmpkey_cipher = RSACipher(
            password=self.password,
            data_encoder=RawDataEncoder,
            result_encoder=Base64ResultEncoder,
        )
        tmpkey = tmpkey_cipher.decrypt(tmpkey_cipher_text)
        data_cipher = GCMAESCipher(
            password=tmpkey,
            data_encoder=RawDataEncoder,
            result_encoder=Base64ResultEncoder,
        )
        return data_cipher.decrypt(data_cipher_text)
