
"""Реализация режима ECB"""
from ..crypto.aes import AES128
from ..crypto.padding import PKCS7Padding


class ECBMode:
    """Реализация режима Electronic Codebook (ECB)"""

    BLOCK_SIZE = 16

    def __init__(self, key_hex: str):
        self.aes = AES128(self._validate_key(key_hex))
        self.padding = PKCS7Padding

    def _validate_key(self, key_hex: str) -> bytes:
        """Проверка и конвертация ключа"""
        key_hex = key_hex.lstrip('@')

        if len(key_hex) != 32:
            raise ValueError(f"Ключ должен быть 16 байт (32 hex символа). Получено: {len(key_hex)} символов")

        try:
            return bytes.fromhex(key_hex)
        except ValueError as e:
            raise ValueError(f"Неверный формат ключа: {e}")

    def _split_into_blocks(self, data: bytes) -> list:
        """Разбивает данные на блоки фиксированного размера"""
        blocks = []
        for i in range(0, len(data), self.BLOCK_SIZE):
            block = data[i:i + self.BLOCK_SIZE]
            blocks.append(block)
        return blocks

    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных в режиме ECB"""
        try:
            # Добавляем PKCS7 padding
            padded_data = self.padding.pad(data)

            # Разбиваем на блоки
            blocks = self._split_into_blocks(padded_data)

            # Шифруем каждый блок отдельно
            encrypted_blocks = []
            for block in blocks:
                encrypted_block = self.aes.encrypt_block(block)
                encrypted_blocks.append(encrypted_block)

            # Собираем все блоки вместе
            encrypted_data = b''.join(encrypted_blocks)
            return encrypted_data

        except Exception as e:
            raise Exception(f"Ошибка при шифровании: {e}")

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Дешифрование данных в режиме ECB"""
        try:
            # Проверяем что данные кратны размеру блока
            if len(encrypted_data) % self.BLOCK_SIZE != 0:
                raise ValueError("Размер зашифрованных данных должен быть кратен размеру блока")

            # Разбиваем на блоки
            blocks = self._split_into_blocks(encrypted_data)

            # Дешифруем каждый блок отдельно
            decrypted_blocks = []
            for block in blocks:
                decrypted_block = self.aes.decrypt_block(block)
                decrypted_blocks.append(decrypted_block)

            # Собираем все блоки вместе
            decrypted_data = b''.join(decrypted_blocks)

            # Убираем padding
            unpadded_data = self.padding.unpad(decrypted_data)
            return unpadded_data

        except Exception as e:
            raise Exception(f"Ошибка при дешифровании: {e}")