from .cipher_base import CipherBase
from .pseudo_random import LCG135RPNG
from .data_encoder import RawDataEncoder
from .result_encoder import RawResultEncoder

__all__ = [
    "IvCipher",
]


class IvCipher(CipherBase):
    """Int value encryption and decryption cipher.

    Example:

    In [38]: from fastutils import corecipher

    In [39]: cipher = corecipher.IvCipher(password='hello')

    In [40]: for i in range(10):
        ...:     print(i, cipher.encrypt(i))
        ...:
    0 0
    1 97
    2 112
    3 204
    4 205
    5 253
    6 294
    7 339
    8 364
    9 447
    """

    default_random_generator_class = LCG135RPNG
    default_data_encoder = RawDataEncoder
    default_result_encoder = RawResultEncoder

    def __init__(
        self,
        password,
        data_encoder=None,
        result_encoder=None,
        random_generator_class=None,
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
        # 生成随机向量
        self.iv_params = self.get_iv_params()

    def get_iv_params(self):
        n = self.random_generator.randint(1024, 9999)
        iv = [self.random_generator.randint(1, 100) for _ in range(n)]
        return n, iv

    def do_encrypt(self, number: int) -> int:
        flag = False
        if number < 0:
            number = -1 * number
            flag = True
        n, iv = self.iv_params
        s = sum(iv)
        a = number // n
        b = number % n
        r = a * s + sum(iv[:b])
        if flag:
            r = -1 * r
        return r

    def do_decrypt(self, number: int) -> int:
        flag = False
        if number < 0:
            number = -1 * number
            flag = True
        n, iv = self.iv_params
        s = sum(iv)
        a = number // s
        t = s * a
        if t == number:
            r = a * n
        else:
            for delta in range(n):
                t += iv[delta]
                if t == number:
                    r = a * n + delta + 1
                    break
            if t != number:
                raise RuntimeError(
                    "IvCipher.do_decrypt failed: number={}".format(number)
                )
        if flag:
            r = -1 * r
        return r
