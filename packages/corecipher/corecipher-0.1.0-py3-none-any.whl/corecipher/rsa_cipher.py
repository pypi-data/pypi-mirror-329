from typing import Optional
import base64
import rsa
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5

from .cipher_base import CipherBase
from .data_encoder import DataEncoderBase
from .result_encoder import ResultEncoderBase

__all__ = [
    "RSACipher",
]


class RSACipher(CipherBase):
    """RSA加解密器。

    注意：
        1）加密时初始化参数password表示公钥。
        2）解密时初始化参数password表示私钥。
        3）RSACipher默认使用PKCS1_OAEP封装。
    """

    default_cipher_module = PKCS1_OAEP

    def __init__(
        self,
        password: str,
        passphrase: Optional[str] = None,
        data_encoder: Optional[DataEncoderBase] = None,
        result_encoder: Optional[ResultEncoderBase] = None,
        cipher_module=None,
    ):
        super().__init__(
            password=password,
            data_encoder=data_encoder,
            result_encoder=result_encoder,
        )
        self.passphrase = passphrase
        self.cipher_module = cipher_module or self.default_cipher_module

    @classmethod
    def get_public_key(cls, key, passphrase=None):
        if isinstance(key, RsaKey):
            if hasattr(key, "public_key"):
                return key.public_key()
            else:
                return key.publickey()
        text = key
        if isinstance(key, (rsa.PublicKey, rsa.PrivateKey)):
            text = text.save_pkcs1()
        # 特殊处理没有封头、封尾的public key
        if isinstance(text, str):
            text = text.strip()
            if not text.startswith("-----BEGIN"):
                text = (
                    "-----BEGIN PUBLIC KEY-----\n"
                    + text
                    + "\n-----END PUBLIC KEY-----\n"
                )
            text = text.strip()
        if isinstance(text, bytes):
            text = text.strip()
            if not text.startswith(b"-----BEGIN"):
                text = (
                    b"-----BEGIN PUBLIC KEY-----\n"
                    + text
                    + b"\n-----END PUBLIC KEY-----\n"
                )
            text = text.strip()
        pk = RSA.import_key(text)
        if hasattr(pk, "public_key"):
            pk = pk.public_key()
        else:
            pk = pk.publickey()
        return pk

    @classmethod
    def get_private_key(cls, key, passphrase=None):
        if isinstance(key, RsaKey):
            return key
        text = key
        if isinstance(key, rsa.PrivateKey):
            text = text.save_pkcs1()
        try:
            text = text.strip()
            sk = RSA.import_key(text, passphrase=passphrase)
        except Exception:
            if isinstance(text, str):
                text = text.strip().encode("utf-8")
            text = base64.decodebytes(text)
            sk = RSA.import_key(text, passphrase=passphrase)
        return sk

    def do_encrypt(self, data: bytes) -> bytes:
        key = self.get_public_key(self.password)
        gen = self.cipher_module.new(key)
        return gen.encrypt(data)

    def do_decrypt(self, data: bytes) -> bytes:
        key = self.get_private_key(self.password)
        gen = self.cipher_module.new(key)
        return gen.decrypt(data)
