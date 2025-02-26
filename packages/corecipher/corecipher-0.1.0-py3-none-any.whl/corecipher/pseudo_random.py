from typing import Optional
from typing import Union
import hashlib
import struct
import functools
import time
from zlib import crc32

__all__ = [
    "PseudoRandomNumberGeneratorBase",
    "HashPseudoRandomNumberGenerator",
    "SHA1PRNG",
    "LCG135RPNG",
    "LCG31RPNG",
]


class PseudoRandomNumberGeneratorBase(object):
    """伪随机数生成器。"""

    def __init__(
        self,
        password: Optional[Union[str, bytes, int, float]] = None,
    ):
        self.password = password

    @classmethod
    def force_bytes(self, password):
        if password is None:
            return b""
        if isinstance(password, bytes):
            return password
        return str(password).encode("utf-8")

    def randint(self, a, b=None):
        """If a<b, then return int number in [a, b). If a>b, then return int number in [b, a)."""
        if b is None:
            return int(self.random() * a)
        else:
            if a > b:
                a, b = b, a
            return int(self.random() * (b - a) + a)

    def choice(self, seq):
        index = self.randint(len(seq))
        return seq[index]

    def choices(self, population, k=1):
        result = []
        for _ in range(k):
            result.append(self.choice(population))
        return result

    def shuffle(self, thelist, x=2):
        length = len(thelist)
        if not isinstance(thelist, list):
            thelist = list(thelist)
        for _ in range(int(length * x)):
            p = self.randint(length)
            q = self.randint(length)
            if p == q:
                q += self.randint(length)
                q %= length
            thelist[p], thelist[q] = thelist[q], thelist[p]
        return thelist

    def get_bytes(self, length=1):
        return bytes(bytearray([self.randint(256) for _ in range(length)]))

    def random(self):
        """return a float number in [0, 1)."""
        raise NotImplementedError()


class RandomBytesPseudoRandomNumberGeneratorBase(PseudoRandomNumberGeneratorBase):
    BASE_BYTES = 8
    BASE = 256**8

    def get_bytes(self, length=1):
        raise NotImplementedError()

    def random(self):
        data = self.get_bytes(self.BASE_BYTES)
        digest = struct.unpack(">Q", data)[0]
        return 1.0 * digest / self.BASE


class HashPseudoRandomNumberGenerator(RandomBytesPseudoRandomNumberGeneratorBase):
    """基于HASH的伪随机数生成器。"""

    default_hash_method = hashlib.sha1

    def __init__(
        self,
        password: Optional[Union[str, bytes, int, float]] = None,
        hash_method=None,
    ):
        super().__init__(password=password)
        self.password = self.force_bytes(self.password)
        self.hash_method = hash_method or self.default_hash_method
        self.seed = self.hash_method(self.password).digest()
        self.seed = self.hash_method(self.seed).digest()
        self.seed_length = len(self.seed)
        self.p = 0

    def get_bytes(self, length=1):
        result = b""
        while True:
            if self.p + length < self.seed_length:
                result += self.seed[self.p : self.p + length]
                self.p += length
                return result
            else:
                result += self.seed[self.p :]
                length -= self.seed_length - self.p
                self.p = 0
                self.seed = self.hash_method(self.seed).digest()


class SHA1PRNG(HashPseudoRandomNumberGenerator):
    """基于sha1的伪随机数生成器。"""

    default_hash_method = hashlib.sha1


LCG135RPNG_DEFAULT_MODULUS = (2**30 - 123) * 0.91  # always NOT change this
LCG135RPNG_DEFAULT_MULTIPLIER = (2**29 - 456) * 0.93  # always NOT change this
LCG135RPNG_DEFAULT_INCREMENT = (2**28 - 789) * 0.95  # always NOT change this


class LCG135RPNG(PseudoRandomNumberGeneratorBase):
    """自定义参数的线性同余生成器。"""

    def __init__(
        self,
        password=None,
        a=LCG135RPNG_DEFAULT_MULTIPLIER,
        c=LCG135RPNG_DEFAULT_INCREMENT,
        m=LCG135RPNG_DEFAULT_MODULUS,
    ):
        super().__init__(password=password)
        self.seed = self.get_seed(password)
        self.a = a
        self.c = c
        self.m = m

    @classmethod
    def get_seed(cls, seed, **kwargs):
        if seed is None:
            return time.time()
        if isinstance(seed, str):
            seed = seed.encode("utf-8")
        if isinstance(seed, bytes):
            seed = int.from_bytes(hashlib.sha512(seed).digest(), "big")
        if isinstance(seed, (int, float)):
            return seed
        else:
            msg = "Random seed's type must be in (str, bytes, int, float), but got type {type}.".format(
                type=type(seed)
            )
            raise RuntimeError(msg)

    def random(self):
        """return a float number in [0, 1)."""
        r = (self.a * self.seed + self.c) % self.m
        p = r / self.m
        self.seed = r
        return p


LCG31_RANDOM_DEFAULT_MODULUS = 2**31
LCG31_RANDOM_DEFAULT_MULTIPLIER = 1103515245
LCG31_RANDOM_DEFAULT_INCREMENT = 12345


class LCG31RPNG(PseudoRandomNumberGeneratorBase):
    """线性同余生成器（取模2**31）。"""

    def __init__(
        self,
        password=None,
        a=LCG31_RANDOM_DEFAULT_MULTIPLIER,
        c=LCG31_RANDOM_DEFAULT_INCREMENT,
        m=LCG31_RANDOM_DEFAULT_MODULUS,
    ):
        super().__init__(password=password)
        self.seed = self.get_seed(self.password)
        self.a = a
        self.c = c
        self.m = m

    @classmethod
    def get_seed(cls, seed, **kwargs):
        modulus = 2**32
        if seed is None:
            return int(time.time()) % modulus
        if isinstance(seed, int):
            return int(seed) % modulus
        if isinstance(seed, float):
            return int(seed) % modulus
        if isinstance(seed, str):
            seed = seed.encode("utf-8")
        if isinstance(seed, bytes):
            return crc32(seed) % modulus
        else:
            msg = "Random seed's type must be in (str, bytes, int, float), but got type {}.".format(
                type(seed)
            )
            raise ValueError(msg)

    def random(self):
        r = (self.a * self.seed + self.c) % self.m
        p = r / self.m
        self.seed = r
        return p
