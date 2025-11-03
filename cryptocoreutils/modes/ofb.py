"""Реализация режима OFB"""
from . import BlockCipherMode


class OFBMode(BlockCipherMode):
    """Реализация режима Output Feedback (OFB)"""

    def __init__(self, key_hex: str, iv_hex: str = None):
        super().__init__(key_hex, iv_hex)

    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных в режиме OFB"""
        try:
            if not data:
                raise ValueError("Данные для шифрования не могут быть пустыми")

            encrypted_blocks = []
            keystream_block = self.iv  # Начинаем с IV

            # Генерируем keystream и применяем XOR
            for i in range(0, len(data), self.BLOCK_SIZE):
                block = data[i:i + self.BLOCK_SIZE]

                # Генерируем следующий блок keystream
                keystream_block = self.aes.encrypt_block(keystream_block)

                # XOR с открытым текстом
                encrypted_block = bytes(a ^ b for a, b in zip(block, keystream_block))
                encrypted_blocks.append(encrypted_block)

            # Возвращаем IV + зашифрованные данные
            return self.iv + b''.join(encrypted_blocks)

        except Exception as e:
            raise Exception(f"Ошибка при шифровании OFB: {e}")

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Дешифрование данных в режиме OFB"""
        try:
            if not encrypted_data:
                raise ValueError("Данные для дешифрования не могут быть пустыми")

            if len(encrypted_data) < 16:
                raise ValueError("Данные слишком короткие для OFB режима")

            # Извлекаем IV и зашифрованные данные
            iv = encrypted_data[:16]
            ciphertext_data = encrypted_data[16:]

            decrypted_blocks = []
            keystream_block = iv

            # Генерируем тот же keystream и применяем XOR
            for i in range(0, len(ciphertext_data), self.BLOCK_SIZE):
                block = ciphertext_data[i:i + self.BLOCK_SIZE]

                # Генерируем следующий блок keystream
                keystream_block = self.aes.encrypt_block(keystream_block)

                # XOR с шифртекстом (тот же процесс что и шифрование)
                decrypted_block = bytes(a ^ b for a, b in zip(block, keystream_block))
                decrypted_blocks.append(decrypted_block)

            # OFB не требует паддинга
            return b''.join(decrypted_blocks)

        except Exception as e:
            raise Exception(f"Ошибка при дешифровании OFB: {e}")