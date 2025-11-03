
"""Реализация AES"""
from Crypto.Cipher import AES


class AES128:
    """Реализация AES-128"""

    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError("Ключ должен быть 16 байт")
        self.key = key

    def encrypt_block(self, block: bytes) -> bytes:
        """Шифрование одного блока"""
        if len(block) != 16:
            raise ValueError("Размер блока должен быть 16 байт")
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(block)

    def decrypt_block(self, block: bytes) -> bytes:
        """Дешифрование одного блока"""
        if len(block) != 16:
            raise ValueError("Размер блока должен быть 16 байт")
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.decrypt(block)