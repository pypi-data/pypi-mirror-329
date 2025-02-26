import string
from .mapping_cipher import MappingCipher
from .pseudo_random import LCG135RPNG
from .data_encoder import RawDataEncoder
from .result_encoder import RawResultEncoder
from .result_encoder import Utf8ResultEncoder

__all__ = [
    "M2Cipher",
]


class M2Cipher(MappingCipher):
    """Turn every byte to two ascii_lowercase str randomly by the password.

    b'\x00' -> "si"
    b'\x01' -> "xs"
    ...
    b'\xff' -> "xy"
    """

    default_result_encoder = Utf8ResultEncoder

    def get_seeds(self):
        letters = string.ascii_lowercase
        seeds = []
        for a in letters:
            for b in letters:
                seeds.append(a + b)
        self.random_generator.shuffle(seeds)
        seeds = [x.encode() for x in seeds[:256]]
        return seeds
