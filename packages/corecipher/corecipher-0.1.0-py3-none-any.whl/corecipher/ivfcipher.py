from .ivcipher import IvCipher
from .result_encoder import Utf8ResultEncoder

__all__ = [
    "IvfCipher",
]


class IvfCipher(IvCipher):
    """Float value encryption and decryption cipher.

    Example:

    In [41]: from fastutils import corecipher

    In [42]: cipher = corecipher.IvfCipher(password='hello')

    In [43]: for i in range(10):
        ...:     print(i, cipher.encrypt(i), type(cipher.encrypt(i)))
        ...:
        ...:
    0 +0000000000000000000000 <class 'str'>
    1 +0000000000005004032834 <class 'str'>
    2 +0000000000010008064455 <class 'str'>
    3 +0000000000015012094180 <class 'str'>
    4 +0000000000020016127691 <class 'str'>
    5 +0000000000025020160338 <class 'str'>
    6 +0000000000030024191109 <class 'str'>
    7 +0000000000035028221552 <class 'str'>
    8 +0000000000040032254031 <class 'str'>
    9 +0000000000045036286491 <class 'str'>
    """

    def __init__(
        self,
        password,
        int_digits=12,
        float_digits=4,
        random_generator_class=None,
        data_encoder=None,
        result_encoder=None,
    ):
        """password is required.
        int_digits is the max length of int part value. Add 0 padding to left.
        float_digits is the max length of float part value. Add 0 padding to right.
        """
        super().__init__(
            password=password,
            random_generator_class=random_generator_class,
            data_encoder=data_encoder,
            result_encoder=result_encoder,
        )
        self.int_digits = int_digits
        self.float_digits = float_digits
        self.module = 10 ** (float_digits * 2)
        self.max_value_length = float_digits * 2 + self.int_digits + 2
        self.max = 10**self.max_value_length - 1
        self.value_template = "{:0%dd}" % self.max_value_length

    def do_encrypt(self, number: float) -> str:
        number = int(number * self.module)
        number = super().do_encrypt(number)
        if number >= 0:
            return "+" + self.value_template.format(number)
        else:
            return "*" + self.value_template.format(self.max - abs(number))

    def do_decrypt(self, number: str) -> float:
        sign = number[0]
        number = int(number[1:])
        if sign == "*":
            number = self.max - number
        number = super().do_decrypt(number)
        number = round(number / self.module, self.float_digits)
        if self.float_digits == 0:
            number = int(number)
        if sign == "*":
            return -1 * number
        else:
            return number
