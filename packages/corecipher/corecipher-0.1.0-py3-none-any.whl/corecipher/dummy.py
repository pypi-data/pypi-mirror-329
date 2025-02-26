from .cipher_base import CipherBase

__all__ = [
    "DummyCipher",
]


class DummyCipher(CipherBase):
    """不进行实际加密的加密类。仅用于测试。"""

    def do_encrypt(self, data_encoded: bytes) -> bytes:
        return data_encoded

    def do_decrypt(self, result: bytes) -> bytes:
        return result
