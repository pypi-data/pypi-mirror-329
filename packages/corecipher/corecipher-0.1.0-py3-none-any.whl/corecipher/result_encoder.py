"""结果编解码器。

注意：
    1）加密过程总是使用编码方法。
    2）解密过程总是使用解码方法。
"""

import base64
import binascii

__all__ = [
    "ResultEncoderBase",
    "RawResultEncoder",
    "Utf8ResultEncoder",
    "Base64ResultEncoder",
    "URLSafeBase64ResultEncoder",
    "HexlifyResultEncoder",
]


class ResultEncoderBase(object):
    """原始加密结果编解码器。"""

    @classmethod
    def encode(cls, data):
        """对原始加密结果进行编码，得到最终结果。"""
        raise NotImplementedError()

    @classmethod
    def decode(cls, result):
        """对编码后的加密结果进行解码，得到原始加密结果。对原始加密结果进行解码，得到明文内容。"""
        raise NotImplementedError()


class RawResultEncoder(ResultEncoderBase):
    """不进行任何编解码操作，直接返回原始加密结果。"""

    @classmethod
    def encode(cls, data: bytes) -> bytes:
        return data

    @classmethod
    def decode(cls, result: bytes) -> bytes:
        return result


class Utf8ResultEncoder(ResultEncoderBase):
    """原始加密结果是utf8编码的字节流，经过编码后的加密结果是字符串。"""

    @classmethod
    def encode(cls, data: bytes) -> str:
        return data.decode("utf-8")

    @classmethod
    def decode(cls, result: str) -> bytes:
        return result.encode("utf-8")


class Base64ResultEncoder(ResultEncoderBase):
    """原始加密结果进行base64编码。"""

    @classmethod
    def encode(cls, data: bytes) -> str:
        return "".join(base64.encodebytes(data).decode("utf-8").splitlines())

    @classmethod
    def decode(cls, result: str) -> bytes:
        return base64.decodebytes(result.encode("utf-8"))


class URLSafeBase64ResultEncoder(ResultEncoderBase):
    """原始加密结果进行url-safe-base64编码。"""

    @classmethod
    def encode(cls, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8")

    @classmethod
    def decode(cls, result: str) -> bytes:
        return base64.urlsafe_b64decode(result.encode("utf-8"))


class HexlifyResultEncoder(ResultEncoderBase):
    """原始加密结果进行hexlify编码。"""

    @classmethod
    def encode(cls, data: bytes) -> str:
        return binascii.hexlify(data).decode("utf-8")

    @classmethod
    def decode(cls, result: str) -> bytes:
        return binascii.unhexlify(result.encode("utf-8"))
