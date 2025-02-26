from .mapping_cipher import MappingCipher
from .pseudo_random import LCG135RPNG
from .data_encoder import RawDataEncoder
from .result_encoder import RawResultEncoder

__all__ = [
    "M1Cipher",
    "S1Cipher",
]


class M1Cipher(MappingCipher):
    """Turn every byte to another byte randomly by the password.

    b'\x00' -> b'\x8f'
    b'\x01' -> b'\x8d'
    ...
    b'\xff' -> b'\xd8'
    """

    def get_seeds(self):
        seeds = list(range(256))
        self.random_generator.shuffle(seeds)
        return [bytes([x]) for x in seeds]


class S1Cipher(M1Cipher):
    """兼容`zenutils.corecipher.S1Cipher`。"""

    default_random_generator_class = LCG135RPNG
    default_data_encoder = RawDataEncoder
    default_result_encoder = RawResultEncoder
