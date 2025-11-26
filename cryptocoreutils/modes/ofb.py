"""Реализация режима OFB"""
from . import BlockCipherMode


class OFBMode(BlockCipherMode):
    """Реализация режима Output Feedback (OFB)"""

    def __init__(self, key_hex: str, iv_hex: str = None):
        super().__init__(key_hex, iv_hex)
        self.iv_was_provided_externally = (iv_hex is not None)

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

                # XOR с открытым текстом (только для нужного количества байт)
                encrypted_block = bytes(a ^ b for a, b in zip(block, keystream_block[:len(block)]))
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

            # Унифицированная логика извлечения IV
            if self.iv_was_provided_externally:
                iv = self.iv
                ciphertext_data = encrypted_data
            else:
                # IV не передан - извлекаем из данных
                if len(encrypted_data) < 17:  # Минимум 16 байт IV + 1 байт данных
                    raise ValueError("Данные слишком короткие для OFB режима")
                iv = encrypted_data[:16]
                ciphertext_data = encrypted_data[16:]

            # OFB - потоковый режим, не требует выравнивания по блокам
            decrypted_blocks = []
            keystream_block = iv

            # Генерируем тот же keystream и применяем XOR
            for i in range(0, len(ciphertext_data), self.BLOCK_SIZE):
                block = ciphertext_data[i:i + self.BLOCK_SIZE]

                # Генерируем следующий блок keystream
                keystream_block = self.aes.encrypt_block(keystream_block)

                # XOR с шифртекстом (только для нужного количества байт)
                decrypted_block = bytes(a ^ b for a, b in zip(block, keystream_block[:len(block)]))
                decrypted_blocks.append(decrypted_block)

            # OFB не требует паддинга - возвращаем как есть
            return b''.join(decrypted_blocks)

        except Exception as e:
            raise Exception(f"Ошибка при дешифровании OFB: {e}")