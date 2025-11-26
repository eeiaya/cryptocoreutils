"""Реализация режима CFB"""
from . import BlockCipherMode


class CFBMode(BlockCipherMode):
    """Реализация режима Cipher Feedback (CFB)"""

    def __init__(self, key_hex: str, iv_hex: str = None):
        super().__init__(key_hex, iv_hex)
        self.iv_was_provided_externally = (iv_hex is not None)

    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных в режиме CFB"""
        try:
            if not data:
                raise ValueError("Данные для шифрования не могут быть пустыми")

            encrypted_blocks = []
            feedback = self.iv  # Начинаем с IV

            # Обрабатываем данные побайтово (потоковый режим)
            for i in range(0, len(data), self.BLOCK_SIZE):
                block = data[i:i + self.BLOCK_SIZE]

                # Шифруем feedback регистр
                encrypted_feedback = self.aes.encrypt_block(feedback)

                # XOR с открытым текстом
                encrypted_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
                encrypted_blocks.append(encrypted_block)

                # Обновляем feedback (в CFB режиме feedback = ciphertext)
                feedback = encrypted_block

            # Возвращаем IV + зашифрованные данные
            return self.iv + b''.join(encrypted_blocks)

        except Exception as e:
            raise Exception(f"Ошибка при шифровании CFB: {e}")

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Дешифрование данных в режиме CFB"""
        try:
            if not encrypted_data:
                raise ValueError("Данные для дешифрования не могут быть пустыми")

            # Унифицированная логика извлечения IV как в CBC
            if self.iv_was_provided_externally:
                iv = self.iv
                # ВАЖНО: если IV передан явно, то весь encrypted_data - это шифртекст без IV
                ciphertext_data = encrypted_data
            else:
                # IV не передан - извлекаем из данных
                if len(encrypted_data) < 17:  # Минимум 16 байт IV + 1 байт данных
                    raise ValueError("Данные слишком короткие для CFB режима")
                iv = encrypted_data[:16]
                ciphertext_data = encrypted_data[16:]

            # CFB - потоковый режим, не требует выравнивания по блокам
            decrypted_blocks = []
            feedback = iv

            for i in range(0, len(ciphertext_data), self.BLOCK_SIZE):
                block = ciphertext_data[i:i + self.BLOCK_SIZE]

                # Шифруем feedback регистр
                encrypted_feedback = self.aes.encrypt_block(feedback)

                # XOR с шифртекстом для получения открытого текста
                decrypted_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
                decrypted_blocks.append(decrypted_block)

                # Обновляем feedback (в CFB режиме feedback = ciphertext)
                feedback = block

            # CFB не требует паддинга - возвращаем как есть
            return b''.join(decrypted_blocks)

        except Exception as e:
            raise Exception(f"Ошибка при дешифровании CFB: {e}")
