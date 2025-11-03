"""Режимы шифрования"""
import os
from abc import ABC, abstractmethod


class BlockCipherMode(ABC):
    """Абстрактный базовый класс для режимов шифрования с IV"""

    BLOCK_SIZE = 16

    def __init__(self, key_hex: str, iv_hex: str = None):
        self.aes = self._create_aes(key_hex)
        self.iv = self._process_iv(iv_hex)

    def _create_aes(self, key_hex: str):
        from ..crypto.aes import AES128
        key_hex = key_hex.lstrip('@')

        if len(key_hex) != 32:
            raise ValueError(f"Ключ должен быть 16 байт (32 hex символа). Получено: {len(key_hex)} символов")

        try:
            key_bytes = bytes.fromhex(key_hex)
            return AES128(key_bytes)
        except ValueError as e:
            raise ValueError(f"Неверный формат ключа: {e}")

    def _process_iv(self, iv_hex: str = None) -> bytes:
        """Обрабатывает IV: генерирует новый или парсит переданный"""
        if iv_hex is None:
            # Генерация случайного IV
            return os.urandom(16)
        else:
            # Парсинг переданного IV
            try:
                iv_bytes = bytes.fromhex(iv_hex)
                if len(iv_bytes) != 16:
                    raise ValueError("IV должен быть 16 байт (32 hex символа)")
                return iv_bytes
            except ValueError as e:
                raise ValueError(f"Неверный формат IV: {e}")

    def _split_into_blocks(self, data: bytes) -> list:
        """Разбивает данные на блоки фиксированного размера"""
        blocks = []
        for i in range(0, len(data), self.BLOCK_SIZE):
            block = data[i:i + self.BLOCK_SIZE]
            blocks.append(block)
        return blocks

    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        pass