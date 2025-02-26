from .mapping_cipher import MappingCipher
from .pseudo_random import LCG135RPNG
from .data_encoder import RawDataEncoder
from .result_encoder import RawResultEncoder

__all__ = [
    "M12Cipher",
    "S12Cipher",
]


class M12Cipher(MappingCipher):
    """将每个字节转换为两个保持顺序的随机字节。

    b'\x00' -> b"\x01\x0d"
    b'\x01' -> b"\x01\x1a"
    ...
    b'\xff' -> b"\xef\xcc"
    """

    def get_seeds(self):
        v = self.random_generator.get_bytes(256)
        v = list(v)
        values = list(range(256))
        delta = 0
        for index in range(256):
            delta += v[index]
            values[index] += delta
        seeds = []
        for code in range(256):
            value = values[code]
            high = value // 256
            low = value % 256
            seeds.append(bytes([high, low]))
        return seeds


class S12Cipher(M12Cipher):
    """兼容`zenutils.corecipher.S12Cipher`。"""

    default_random_generator_class = LCG135RPNG
    default_data_encoder = RawDataEncoder
    default_result_encoder = RawResultEncoder
