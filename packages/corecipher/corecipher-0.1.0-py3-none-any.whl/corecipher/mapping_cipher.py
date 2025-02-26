import binascii
import json
from .cipher_base import CipherBase
from .pseudo_random import SHA1PRNG

__all__ = [
    "MappingCipher",
]


class MappingCipher(CipherBase):
    """Turn every byte to another value.

    0 -> b'randseed01'
    1 -> b'randseed02'
    ... -> ...
    255 -> b'randseed03'

    """

    default_random_generator_class = SHA1PRNG

    def __init__(
        self,
        password,
        random_generator_class=None,
        data_encoder=None,
        result_encoder=None,
    ):
        super().__init__(
            password=password,
            data_encoder=data_encoder,
            result_encoder=result_encoder,
        )
        # 构建随机数生成器
        self.random_generator_class = random_generator_class
        if not self.random_generator_class:
            self.random_generator_class = self.default_random_generator_class
        self.random_generator = self.random_generator_class(password=password)
        # 生成加密种子数据
        self.seeds = self.try_to_load_seeds(password)
        if not self.seeds:
            self.seeds = self.get_seeds()
        # 生成加密映射表
        self.encrypt_mapping = self.get_encrypt_mapping()
        self.decrypt_mapping = self.get_decrypt_mapping()

    def get_encrypt_mapping(self):
        mapping = {}
        for i in range(256):
            mapping[bytes([i])] = self.seeds[i]
        return mapping

    def get_decrypt_mapping(self):
        mapping = {}
        for i in range(256):
            mapping[self.seeds[i]] = bytes([i])
        return mapping

    def do_encrypt(self, data: bytes):
        if data is None:
            return None
        result = b"".join([self.encrypt_mapping[bytes([c])] for c in data])
        return result

    def do_decrypt(self, data: bytes):
        if data is None:
            return None
        result = b""
        data_length = len(data)
        max_seed_length = max([len(x) for x in self.decrypt_mapping.keys()])
        start = 0
        while start < data_length:
            found = False
            for seed_length in range(1, max_seed_length + 1):
                seed = data[start : start + seed_length]
                if seed in self.decrypt_mapping:
                    result += self.decrypt_mapping[seed]
                    start += seed_length
                    found = True
                    break
            if not found:
                raise RuntimeError("decrypt failed...")
        return result

    def dumps(self):
        seeds = [binascii.hexlify(x).decode() for x in self.seeds]
        data = json.dumps(seeds)
        data = binascii.hexlify(data.encode("utf-8")).decode("utf-8")
        return data

    @classmethod
    def loads(cls, data, **kwargs):
        return cls(password=data, **kwargs)

    @classmethod
    def try_to_load_seeds(cls, data):
        try:
            data = binascii.unhexlify(data.encode("utf-8"))
            seeds = json.loads(data)
            seeds = [binascii.unhexlify(x.encode("utf-8")) for x in seeds]
            return seeds
        except Exception:
            return None

    @classmethod
    def password_to_key(cls, password):
        cipher = cls(password=password)
        return cipher.dumps()

    def get_seeds(self):
        raise NotImplementedError()
