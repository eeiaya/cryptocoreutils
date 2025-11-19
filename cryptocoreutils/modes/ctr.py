"""Реализация режима CTR"""
from . import BlockCipherMode


class CTRMode(BlockCipherMode):
    """Реализация режима Counter (CTR)"""

    def __init__(self, key_hex: str, iv_hex: str = None):
        super().__init__(key_hex, iv_hex)

    def _increment_counter(self, counter: bytes) -> bytes:
        """Инкрементирует счетчик (big-endian)"""
        counter_int = int.from_bytes(counter, byteorder='big')
        counter_int = (counter_int + 1) & ((1 << 128) - 1)  # Ограничение 128 бит
        return counter_int.to_bytes(16, byteorder='big')

    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных в режиме CTR"""
        try:
            if not data:
                raise ValueError("Данные для шифрования не могут быть пустыми")

            encrypted_blocks = []
            counter = self.iv  # Начинаем с IV/nonce

            # Генерируем keystream и применяем XOR
            for i in range(0, len(data), self.BLOCK_SIZE):
                block = data[i:i + self.BLOCK_SIZE]

                # Шифруем текущее значение счетчика
                keystream_block = self.aes.encrypt_block(counter)

                # XOR с открытым текстом
                encrypted_block = bytes(a ^ b for a, b in zip(block, keystream_block))
                encrypted_blocks.append(encrypted_block)

                # Инкрементируем счетчик
                counter = self._increment_counter(counter)

            # Возвращаем IV/nonce + зашифрованные данные
            return self.iv + b''.join(encrypted_blocks)

        except Exception as e:
            raise Exception(f"Ошибка при шифровании CTR: {e}")

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Дешифрование данных в режиме CTR"""
        try:
            if not encrypted_data:
                raise ValueError("Данные для дешифрования не могут быть пустыми")

            # Если IV был передан в конструкторе, используем его и весь encrypted_data как шифртекст
            # Если IV не был передан, извлекаем первые 16 байт как IV
            if hasattr(self, 'iv') and self.iv is not None:
                # IV передан явно - используем весь encrypted_data как шифртекст
                iv = self.iv
                ciphertext_data = encrypted_data
            else:
                # IV не передан - извлекаем из данных
                if len(encrypted_data) < 32:
                    raise ValueError("Данные слишком короткие для CTR режима")
                iv = encrypted_data[:16]
                ciphertext_data = encrypted_data[16:]

            # CTR - потоковый режим, не требует выравнивания по блокам
            decrypted_blocks = []
            counter = iv

            # Генерируем тот же keystream и применяем XOR
            for i in range(0, len(ciphertext_data), self.BLOCK_SIZE):
                block = ciphertext_data[i:i + self.BLOCK_SIZE]

                # Шифруем текущее значение счетчика
                keystream_block = self.aes.encrypt_block(counter)

                # XOR с шифртекстом (тот же процесс что и шифрование)
                decrypted_block = bytes(a ^ b for a, b in zip(block, keystream_block))
                decrypted_blocks.append(decrypted_block)

                # Инкрементируем счетчик
                counter = self._increment_counter(counter)

            # CTR не требует паддинга - возвращаем как есть
            return b''.join(decrypted_blocks)

        except Exception as e:
            raise Exception(f"Ошибка при дешифровании CTR: {e}")