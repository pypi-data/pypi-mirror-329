from typing import Any
from typing import Optional
from typing import Type
from .data_encoder import DataEncoderBase
from .data_encoder import Utf8DataEncoder
from .data_encoder import JsonEncoder
from .result_encoder import ResultEncoderBase
from .result_encoder import Base64ResultEncoder
from .pseudo_random import PseudoRandomNumberGeneratorBase
from .pseudo_random import SHA1PRNG


__all__ = [
    "CipherBase",
]


class CipherBase(object):
    """加解密器基础类。

    注意：
        1）password表示密钥，一般为字符串类型，但不同的加解密器可以支持更灵活的类型。
        2）data_encoder表示原始明文数据如何编码为可实际加密的bytes类型，以及如何解码实际解密的bytes类型从而得到原始明文数据。
        3）result_encoder表示加密结果如何转化为外部程序可以使用的类型，一般为字符串类型，但也可以支持更灵活的类型。
    """

    default_data_encoder = Utf8DataEncoder
    default_result_encoder = Base64ResultEncoder

    def __init__(
        self,
        password: str,
        data_encoder: Optional[DataEncoderBase] = None,
        result_encoder: Optional[ResultEncoderBase] = None,
    ):
        self.password = password
        self.data_encoder = data_encoder or self.default_data_encoder
        self.result_encoder = result_encoder or self.default_result_encoder

    def encrypt(self, data: Any) -> str:
        data_encoded = self.data_encoder.encode(data)
        result_raw = self.do_encrypt(data_encoded)
        result = self.result_encoder.encode(result_raw)
        return result

    def decrypt(self, result):
        result_raw = self.result_encoder.decode(result)
        data_encoded = self.do_decrypt(result_raw)
        data = self.data_encoder.decode(data_encoded)
        return data

    def do_encrypt(self, data_encoded: bytes) -> bytes:
        raise NotImplementedError()

    def do_decrypt(self, result: bytes) -> bytes:
        raise NotImplementedError()
