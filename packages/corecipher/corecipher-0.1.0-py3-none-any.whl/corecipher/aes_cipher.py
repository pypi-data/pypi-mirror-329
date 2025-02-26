from typing import Optional
from typing import Type
import os
import json
import binascii
from Crypto.Cipher import AES
from .pseudo_random import SHA1PRNG
from .data_encoder import DataEncoderBase
from .result_encoder import ResultEncoderBase
from .pseudo_random import PseudoRandomNumberGeneratorBase
from .cipher_base import CipherBase
from .padding import PaddingBase
from .padding import Pkcs5Padding
from .keygen import KeyGeneratorBase
from .keygen import SHA1PRNGKeyGenerator
from .keygen import MysqlCompatibleKeyGenerator

__all__ = [
    "AESCipher",
    "GCMAESCipher",
    "CTRAESCipher",
    "ECBAESCipher",
    "MysqlCompatibleAESCipher",
]


class AESCipher(CipherBase):
    """AES基础类

    主要提供了：
    1）密钥转化器，默认使用SHA1PRNG。

    """

    default_key_generator_class: Type[KeyGeneratorBase] = SHA1PRNGKeyGenerator
    default_key_size = AES.block_size

    def __init__(
        self,
        # 密钥
        password: str,
        # 数据编解码器
        data_encoder: Optional[DataEncoderBase] = None,
        # 结果编解码器
        result_encoder: Optional[ResultEncoderBase] = None,
        # 密钥转化器
        key_generator_class: Optional[Type[KeyGeneratorBase]] = None,
        key_size: Optional[int] = None,
    ):
        super().__init__(
            password=password,
            data_encoder=data_encoder,
            result_encoder=result_encoder,
        )
        # 获取密钥转化器类
        self.key_generator_class = key_generator_class
        if not self.key_generator_class:
            self.key_generator_class = self.default_key_generator_class
        # 获取密钥大小
        self.key_size = key_size
        if not self.key_size:
            self.key_size = self.default_key_size
        # 获取密钥转化器
        self.key_generator = self.key_generator_class(
            password=self.password,
            key_size=self.key_size,
        )
        # 完成密钥转化
        self.key = self.key_generator.get_key()


class CTRAESCipher(AESCipher):
    """AES加解密码器，使用CTR模式。

    CTR模式在加密后会产生nonce，需要与结果一起发送到解密端。
    CTR模式加密结果的数据结构为：
        {
            "cipher_text": cipher_text,
            "nonce": cipher.nonce,
        }
    将该结构使用json序列化后，形成最终的结果字节流。

    另外，CTR模式不需要对加密数据进行填充。
    """

    def do_encrypt(self, data: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CTR)
        cipher_text = cipher.encrypt(data)
        nonce = cipher.nonce
        return json.dumps(
            {
                "cipher_text": binascii.hexlify(cipher_text).decode("utf-8"),
                "nonce": binascii.hexlify(nonce).decode("utf-8"),
            }
        ).encode("utf-8")

    def do_decrypt(self, data: bytes) -> bytes:
        info = json.loads(data)
        cipher_text = binascii.unhexlify(info["cipher_text"].encode("utf-8"))
        nonce = binascii.unhexlify(info["nonce"].encode("utf-8"))
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=nonce)
        return cipher.decrypt(cipher_text)


class GCMAESCipher(AESCipher):
    """AES加解密码器，使用GCM模式。"""

    default_random_header_size: int = 64

    def __init__(
        self,
        password: str,
        data_encoder: Optional[DataEncoderBase] = None,
        result_encoder: Optional[ResultEncoderBase] = None,
        key_generator_class: Optional[Type[KeyGeneratorBase]] = None,
        key_size: Optional[int] = None,
        header: Optional[str] = None,
        random_header_size: Optional[int] = None,
    ):
        super().__init__(
            password=password,
            data_encoder=data_encoder,
            result_encoder=result_encoder,
            key_generator_class=key_generator_class,
            key_size=key_size,
        )
        self.random_header_size = random_header_size or self.default_random_header_size
        self.header = header

    def do_encrypt(self, data: bytes) -> bytes:
        header = self.header or os.urandom(self.random_header_size)
        cipher = AES.new(self.key, AES.MODE_GCM)
        cipher.update(header)
        cipher_text, tag = cipher.encrypt_and_digest(data)
        nonce = cipher.nonce
        return json.dumps(
            {
                "cipher_text": binascii.hexlify(cipher_text).decode("utf-8"),
                "nonce": binascii.hexlify(nonce).decode("utf-8"),
                "header": binascii.hexlify(header).decode("utf-8"),
                "tag": binascii.hexlify(tag).decode("utf-8"),
            }
        ).encode("utf-8")

    def do_decrypt(self, data: bytes) -> bytes:
        info = json.loads(data)
        cipher_text = binascii.unhexlify(info["cipher_text"].encode("utf-8"))
        nonce = binascii.unhexlify(info["nonce"].encode("utf-8"))
        header = binascii.unhexlify(info["header"].encode("utf-8"))
        tag = binascii.unhexlify(info["tag"].encode("utf-8"))
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        cipher.update(header)
        return cipher.decrypt_and_verify(cipher_text, tag)


class ECBAESCipher(AESCipher):

    default_padding_class = Pkcs5Padding

    def __init__(
        self,
        # 密钥
        password: str,
        # 数据编解码器
        data_encoder: Optional[DataEncoderBase] = None,
        # 结果编解码器
        result_encoder: Optional[ResultEncoderBase] = None,
        # 密钥转化器
        key_generator_class: Optional[Type[PseudoRandomNumberGeneratorBase]] = None,
        key_size: Optional[int] = None,
        # 数据填充器
        padding_class: Optional[Type[PaddingBase]] = None,
    ):
        super().__init__(
            password=password,
            data_encoder=data_encoder,
            result_encoder=result_encoder,
            key_generator_class=key_generator_class,
            key_size=key_size,
        )
        self.padding_class = padding_class or self.default_padding_class
        self.padding_device = self.padding_class()

    def do_encrypt(self, data: bytes) -> bytes:
        data = self.padding_device.pad(data, size=AES.block_size)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(data)

    def do_decrypt(self, cipher_text: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_ECB)
        data = cipher.decrypt(cipher_text)
        return self.padding_device.unpad(data, size=AES.block_size)


class MysqlCompatibleAESCipher(ECBAESCipher):
    default_key_generator_class: Type[KeyGeneratorBase] = MysqlCompatibleKeyGenerator
