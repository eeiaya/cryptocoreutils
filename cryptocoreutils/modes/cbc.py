"""Реализация режима CBC"""
from . import BlockCipherMode
from ..crypto.padding import PKCS7Padding

class CBCMode(BlockCipherMode):
    """Реализация режима Cipher Block Chaining (CBC)"""

    def __init__(self, key_hex: str, iv_hex: str = None):
        super().__init__(key_hex, iv_hex)
        self.padding = PKCS7Padding

    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных в режиме CBC"""
        try:
            # Проверяем что данные не пустые
            if not data:
                raise ValueError("Данные для шифрования не могут быть пустыми")

            # Добавляем PKCS7 padding
            padded_data = self.padding.pad(data)
            blocks = self._split_into_blocks(padded_data)

            encrypted_blocks = []
            previous_block = self.iv  # Первый блок XOR с IV

            for block in blocks:
                # XOR с предыдущим зашифрованным блоком (или IV для первого блока)
                xor_block = bytes(a ^ b for a, b in zip(block, previous_block))
                encrypted_block = self.aes.encrypt_block(xor_block)
                encrypted_blocks.append(encrypted_block)
                previous_block = encrypted_block  # Для следующего блока

            # Возвращаем IV + зашифрованные данные
            return self.iv + b''.join(encrypted_blocks)

        except Exception as e:
            raise Exception(f"Ошибка при шифровании CBC: {e}")

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Дешифрование данных в режиме CBC"""
        try:
            # Проверяем что данные не пустые
            if not encrypted_data:
                raise ValueError("Данные для дешифрования не могут быть пустыми")

            # Проверяем минимальный размер (IV + хотя бы один блок)
            if len(encrypted_data) < 32:  # 16 байт IV + 16 байт данных
                raise ValueError("Данные слишком короткие для CBC режима")

            # Извлекаем IV и зашифрованные данные
            iv = encrypted_data[:16]
            ciphertext_data = encrypted_data[16:]

            # Проверяем что данные кратны размеру блока
            if len(ciphertext_data) % self.BLOCK_SIZE != 0:
                raise ValueError("Размер зашифрованных данных должен быть кратен размеру блока")

            ciphertext_blocks = self._split_into_blocks(ciphertext_data)
            decrypted_blocks = []
            previous_block = iv

            for block in ciphertext_blocks:
                decrypted_block = self.aes.decrypt_block(block)
                # XOR с предыдущим зашифрованным блоком (или IV для первого блока)
                plaintext_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
                decrypted_blocks.append(plaintext_block)
                previous_block = block  # Для следующего блока

            decrypted_data = b''.join(decrypted_blocks)

            # Убираем padding
            unpadded_data = self.padding.unpad(decrypted_data)
            return unpadded_data

        except Exception as e:
            raise Exception(f"Ошибка при дешифровании CBC: {e}")