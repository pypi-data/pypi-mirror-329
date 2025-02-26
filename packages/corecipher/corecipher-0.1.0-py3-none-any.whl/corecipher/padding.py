import os

__all__ = [
    "PaddingBase",
    "Pkcs5Padding",
    "ISO10126Padding",
    "ANSIX923Padding",
]


class PaddingBase(object):
    @classmethod
    def pad(cls, data: bytes, size: int) -> bytes:
        pass

    @classmethod
    def unpad(cls, data: bytes, size: int) -> bytes:
        pass


class Pkcs5Padding(PaddingBase):
    @classmethod
    def pad(cls, data: bytes, size: int) -> bytes:
        padsize = size - len(data) % size
        return data + bytes([padsize] * padsize)

    @classmethod
    def unpad(cls, data: bytes, size: int) -> bytes:
        padsize = data[-1]
        return data[: -1 * padsize]


class ISO10126Padding(PaddingBase):
    @classmethod
    def pad(cls, data: bytes, size: int) -> bytes:
        padsize = size - len(data) % size
        return data + os.urandom(padsize - 1) + bytes([padsize])

    @classmethod
    def unpad(cls, data: bytes, size: int) -> bytes:
        padsize = data[-1]
        return data[: -1 * padsize]


class ANSIX923Padding(PaddingBase):
    @classmethod
    def pad(cls, data: bytes, size: int) -> bytes:
        padsize = size - len(data) % size
        return data + bytes([0] * (padsize - 1)) + bytes([padsize])

    @classmethod
    def unpad(cls, data: bytes, size: int) -> bytes:
        padsize = data[-1]
        return data[: -1 * padsize]
