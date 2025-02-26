from typing import Optional
from typing import Union
from .pseudo_random import SHA1PRNG

__all__ = [
    "KeyGeneratorBase",
    "SHA1PRNGKeyGenerator",
    "MysqlCompatibleKeyGenerator",
]


class KeyGeneratorBase(object):
    default_key_size: int = 16

    def __init__(
        self,
        password: Union[str, bytes, int, float],
        key_size: Optional[int] = None,
    ):
        self.password = password
        self.key_size = key_size or self.default_key_size

    def get_key(self):
        raise NotImplementedError()

    @classmethod
    def force_bytes(self, password):
        if isinstance(password, bytes):
            return password
        return str(password).encode("utf-8")


class SHA1PRNGKeyGenerator(KeyGeneratorBase):
    def get_key(self):
        password = self.force_bytes(self.password)
        return SHA1PRNG(password=password).get_bytes(self.key_size)


class MysqlCompatibleKeyGenerator(KeyGeneratorBase):
    def get_key(self):
        password = self.force_bytes(self.password)
        final_key = bytearray(self.key_size)
        for i, c in enumerate(password):
            final_key[i % self.key_size] ^= c
        return bytes(final_key)
