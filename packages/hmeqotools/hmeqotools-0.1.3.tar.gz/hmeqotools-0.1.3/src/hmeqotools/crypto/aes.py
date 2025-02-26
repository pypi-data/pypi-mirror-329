from __future__ import annotations

import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from hmeqotools.crypto.padding import *


class AES(Cipher):
    modes = modes

    block_size = 16

    def __init__(self, key: bytes, mode: modes.Mode, block_size=block_size):
        super().__init__(algorithms.AES(key), mode, default_backend())
        self.key = key
        self.block_size = block_size

    @classmethod
    def generate_key(cls):
        return os.urandom(cls.block_size)

    @classmethod
    def generate(cls, mode: modes.Mode | None = None):
        return cls(cls.generate_key(), mode or modes.ECB())

    @classmethod
    def pad(cls, b: bytes):
        """padding bytes"""
        return pad(b, cls.block_size)

    @staticmethod
    def unpad(b: bytes):
        """unpadding bytes"""
        return unpad(b)

    def encrypt(self, data: bytes):
        """Encrypt bytes, automatic padding data"""
        encryptor = self.encryptor()
        encrypted = encryptor.update(self.pad(data)) + encryptor.finalize()
        return base64.b64encode(encrypted)

    def decrypt(self, data: bytes):
        """Decrypt bytes, automatic unpadding data"""
        a = base64.b64decode(data)
        decryptor = self.decryptor()
        decrypted = decryptor.update(a) + decryptor.finalize()
        return self.unpad(decrypted)


def main():
    key = b"1234567890123456"
    # key = AES.generate_key()
    aes = AES(key, AES.modes.ECB())
    a = aes.encrypt(b"123")
    b = aes.decrypt(a)
    print(a, b)


if __name__ == "__main__":
    main()
