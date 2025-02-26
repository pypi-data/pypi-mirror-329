"""原始数据编解码器。

注意：
    1）加密过程总是使用编码方法。
    2）解密过程总是使用解码方法。
"""

from typing import Any
import json
import pickle
import marshal
import msgpack

__all__ = [
    "DataEncoderBase",
    "RawDataEncoder",
    "Utf8DataEncoder",
    "Gb18030DataEncoder",
    "JsonEncoder",
    "PickleEncoder",
    "MarshalEncoder",
    "MsgPackEncoder",
]


class DataEncoderBase(object):
    pass


class Utf8DataEncoder(DataEncoderBase):

    @classmethod
    def encode(cls, data: str) -> bytes:
        return data.encode("utf-8")

    @classmethod
    def decode(cls, data_encoded: bytes) -> str:
        return data_encoded.decode("utf-8")


class Gb18030DataEncoder(DataEncoderBase):

    @classmethod
    def encode(cls, data: str) -> bytes:
        return data.encode("gb18030")

    @classmethod
    def decode(cls, data_encoded: bytes) -> str:
        return data_encoded.decode("gb18030")


class RawDataEncoder(DataEncoderBase):

    @classmethod
    def encode(cls, data: bytes) -> bytes:
        return data

    @classmethod
    def decode(cls, data_encoded: bytes) -> bytes:
        return data_encoded


class JsonEncoder(DataEncoderBase):
    """原始数据使用json进行序列化。"""

    @classmethod
    def encode(cls, data: Any) -> bytes:
        return json.dumps(data).encode("utf-8")

    @classmethod
    def decode(cls, data_encoded: bytes) -> Any:
        return json.loads(data_encoded)


class PickleEncoder(DataEncoderBase):
    """原始数据使用pickle进行序列化。"""

    @classmethod
    def encode(cls, data: Any) -> bytes:
        return pickle.dumps(data)

    @classmethod
    def decode(cls, data_encoded: bytes) -> Any:
        return pickle.loads(data_encoded)


class MarshalEncoder(DataEncoderBase):
    """原始数据使用marshal进行序列化。"""

    @classmethod
    def encode(cls, data: Any) -> bytes:
        return marshal.dumps(data)

    @classmethod
    def decode(cls, data_encoded: bytes) -> Any:
        return marshal.loads(data_encoded)


class MsgPackEncoder(DataEncoderBase):
    """原始数据使用msgpack进行序列化。"""

    @classmethod
    def encode(cls, data: Any) -> bytes:
        return msgpack.dumps(data)

    @classmethod
    def decode(cls, data_encoded: bytes) -> Any:
        return msgpack.loads(data_encoded)
