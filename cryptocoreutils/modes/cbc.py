"""Реализация режима CBC"""
from . import BlockCipherMode
from ..crypto.padding import PKCS7Padding

class CBCMode(BlockCipherMode):
    """Реализация режима Cipher Block Chaining (CBC)"""

    def __init__(self, key_hex: str, iv_hex: str = None):
        super().__init__(key_hex, iv_hex)
        self.padding = PKCS7Padding
        self.iv_was_provided_externally = (iv_hex is not None)

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
            if not encrypted_data:
                raise ValueError("Данные для дешифрования не могут быть пустыми")

            # Если IV был передан в конструкторе, используем его и весь encrypted_data как шифртекст
            # Если IV не был передан, извлекаем первые 16 байт как IV
            if hasattr(self, 'iv') and self.iv is not None:
                # IV передан явно - используем весь encrypted_data как шифртекст
                iv = self.iv
                ciphertext_data = encrypted_data
                # Для данных от OpenSSL с padding, нужно убрать padding
                remove_padding = True
            else:
                # IV не передан - извлекаем из данных
                if len(encrypted_data) < 32:
                    raise ValueError("Данные слишком короткие для CBC режима")
                iv = encrypted_data[:16]
                ciphertext_data = encrypted_data[16:]
                # Для наших собственных данных также убираем padding
                remove_padding = True

            # Проверяем что данные кратны размеру блока
            if len(ciphertext_data) % self.BLOCK_SIZE != 0:
                raise ValueError("Размер зашифрованных данных должен быть кратен размеру блока")

            ciphertext_blocks = self._split_into_blocks(ciphertext_data)
            decrypted_blocks = []
            previous_block = iv

            for block in ciphertext_blocks:
                decrypted_block = self.aes.decrypt_block(block)
                plaintext_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
                decrypted_blocks.append(plaintext_block)
                previous_block = block

            decrypted_data = b''.join(decrypted_blocks)

            # Убираем padding только если это необходимо
            if remove_padding:
                # Проверяем, есть ли padding (последний байт указывает на длину padding)
                pad_len = decrypted_data[-1]
                if pad_len <= self.BLOCK_SIZE:
                    # Проверяем корректность padding
                    expected_padding = bytes([pad_len] * pad_len)
                    actual_padding = decrypted_data[-pad_len:]
                    if expected_padding == actual_padding:
                        unpadded_data = decrypted_data[:-pad_len]
                        return unpadded_data

            # Если padding некорректен или не нужно удалять, возвращаем как есть
            return decrypted_data

        except Exception as e:
            raise Exception(f"Ошибка при дешифровании CBC: {e}")