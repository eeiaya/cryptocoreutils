"""
Encrypt-then-MAC (ETM) implementation.
Combines CTR encryption with HMAC for authenticated encryption.
"""

import os
from pathlib import Path
from ..crypto.aes import AES128  # Используем твой AES128
from ..mac.hmac import HMAC  # Используем твой HMAC
from ..exceptions import AuthenticationError, CryptoOperationError
from ..csprng import generate_random_bytes


class ETMMode:
    """
    Encrypt-then-MAC authenticated encryption mode.

    Security properties:
    1. Confidentiality: AES-128 in CTR mode
    2. Integrity/Authenticity: HMAC-SHA256 over ciphertext + AAD
    3. Catastrophic failure: No output on authentication failure

    Format: IV(16) || ciphertext || HMAC(32)
    """

    BLOCK_SIZE = 16  # AES block size
    IV_SIZE = 16     # IV size for CTR mode
    TAG_SIZE = 32    # HMAC-SHA256 output size (32 bytes = 256 bits)

    def __init__(self, key: bytes, iv: bytes = None):
        """
        Initialize ETM mode.

        Args:
            key: Master key (16 bytes for AES-128)
            iv: Initialization vector (16 bytes, auto-generated if None)

        Raises:
            ValueError: If key size is invalid
        """
        # Твой AES128 поддерживает только 16-байтные ключи
        if len(key) != 16:
            raise ValueError(f"Ключ должен быть 16 байт, получено: {len(key)}")

        self.master_key = key

        # Деривируем отдельные ключи для шифрования и MAC
        self.enc_key, self.mac_key = self._derive_keys(key)

        # Инициализируем твой AES128 для использования в CTR режиме
        self.aes = AES128(self.enc_key)

        # Генерируем IV если не предоставлен
        self.iv = iv if iv is not None else generate_random_bytes(self.IV_SIZE)

        if len(self.iv) != self.IV_SIZE:
            raise ValueError(f"IV должен быть {self.IV_SIZE} байт, получено {len(self.iv)}")

    def _derive_keys(self, master_key: bytes) -> tuple:
        """
        Derive separate keys for encryption and MAC from master key.

        Args:
            master_key: 16-byte master key

        Returns:
            Tuple of (encryption_key, mac_key)
        """
        # Деривация ключа шифрования
        hmac_enc = HMAC(master_key, hash_algo='sha256')
        hmac_enc.update(b"etm-encryption-key-derivation")
        enc_key = hmac_enc.digest()[:16]  # 128-bit encryption key

        # Деривация ключа MAC
        hmac_mac = HMAC(master_key, hash_algo='sha256')
        hmac_mac.update(b"etm-authentication-key-derivation")
        mac_key = hmac_mac.digest()  # 256-bit MAC key

        return enc_key, mac_key

    def _increment_counter(self, counter: bytes) -> bytes:
        """
        Increment 128-bit counter for CTR mode.

        Args:
            counter: 16-byte counter

        Returns:
            Incremented counter
        """
        counter_int = int.from_bytes(counter, 'big')
        counter_int = (counter_int + 1) & ((1 << 128) - 1)  # Mod 2^128
        return counter_int.to_bytes(16, 'big')

    def _ctr_process(self, data: bytes, iv: bytes) -> bytes:
        """
        CTR mode encryption/decryption.

        Args:
            data: Plaintext or ciphertext
            iv: Initial counter value

        Returns:
            Processed data
        """
        result = bytearray()
        counter = iv

        for i in range(0, len(data), self.BLOCK_SIZE):
            block = data[i:i + self.BLOCK_SIZE]

            # Шифруем счетчик для получения keystream
            keystream = self.aes.encrypt_block(counter)

            # XOR с данными
            for j, byte in enumerate(block):
                result.append(byte ^ keystream[j])

            # Инкрементируем счетчик
            counter = self._increment_counter(counter)

        return bytes(result)

    def _compute_mac(self, ciphertext: bytes, aad: bytes = b"") -> bytes:
        """
        Compute HMAC over ciphertext and AAD.

        Args:
            ciphertext: Encrypted data
            aad: Additional authenticated data

        Returns:
            32-byte HMAC tag
        """
        # Используем твой HMAC
        hmac = HMAC(self.mac_key, hash_algo='sha256')

        # Включаем AAD в вычисление MAC
        if aad:
            hmac.update(aad)

        # Включаем ciphertext
        hmac.update(ciphertext)

        # Для дополнительной безопасности включаем длины
        # (опционально, но рекомендуется для предотвращения атак)
        hmac.update(len(aad).to_bytes(8, 'big'))
        hmac.update(len(ciphertext).to_bytes(8, 'big'))

        return hmac.digest()

    @staticmethod
    def _constant_time_compare(a: bytes, b: bytes) -> bool:
        """
        Constant-time comparison to prevent timing attacks.

        Args:
            a: First byte string
            b: Second byte string

        Returns:
            bool: True if strings are equal, False otherwise
        """
        if len(a) != len(b):
            return False

        result = 0
        for x, y in zip(a, b):
            result |= x ^ y

        return result == 0

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> bytes:
        """
        Encrypt using Encrypt-then-MAC.

        Steps:
        1. Encrypt plaintext using CTR mode
        2. Compute HMAC over ciphertext + AAD
        3. Return: IV || ciphertext || HMAC

        Args:
            plaintext: Data to encrypt
            aad: Additional authenticated data

        Returns:
            bytes: IV(16) || ciphertext || HMAC(32)
        """
        # Убедимся что AAD - bytes
        if isinstance(aad, str):
            aad = aad.encode('utf-8')

        # 1. Шифруем в CTR режиме
        ciphertext = self._ctr_process(plaintext, self.iv)

        # 2. Вычисляем HMAC
        tag = self._compute_mac(ciphertext, aad)

        # 3. Возвращаем IV || ciphertext || tag
        return self.iv + ciphertext + tag

    def decrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        """
        Decrypt and verify MAC.

        Steps:
        1. Extract IV, ciphertext, and HMAC tag
        2. Verify HMAC over ciphertext + AAD
        3. If verification fails, raise AuthenticationError immediately
        4. Decrypt ciphertext

        Args:
            data: IV || ciphertext || HMAC
            aad: Additional authenticated data

        Returns:
            bytes: Decrypted plaintext

        Raises:
            AuthenticationError: If HMAC verification fails
            ValueError: If data is too short
        """
        # Убедимся что AAD - bytes
        if isinstance(aad, str):
            aad = aad.encode('utf-8')

        # 1. Проверяем минимальную длину
        min_size = self.IV_SIZE + self.TAG_SIZE
        if len(data) < min_size:
            raise ValueError(f"Данные слишком маленькие: {len(data)} байт, минимум {min_size}")

        # Извлекаем компоненты
        iv = data[:self.IV_SIZE]
        tag = data[-self.TAG_SIZE:]
        ciphertext = data[self.IV_SIZE:-self.TAG_SIZE]

        # 2. Проверяем HMAC (ПЕРЕД дешифрованием!)
        expected_tag = self._compute_mac(ciphertext, aad)

        if not self._constant_time_compare(tag, expected_tag):
            raise AuthenticationError("Authentication failed: AAD mismatch or ciphertext tampered")

        # 3. Дешифруем
        plaintext = self._ctr_process(ciphertext, iv)

        return plaintext

    def encrypt_file(self, input_path: str, output_path: str, aad: bytes = b""):
        """
        Encrypt a file using ETM.

        Args:
            input_path: Path to input file
            output_path: Path to output file
            aad: Additional authenticated data

        Raises:
            CryptoOperationError: If file I/O fails
        """
        try:
            with open(input_path, 'rb') as f:
                plaintext = f.read()

            encrypted = self.encrypt(plaintext, aad)

            with open(output_path, 'wb') as f:
                f.write(encrypted)

        except (IOError, OSError) as e:
            raise CryptoOperationError(f"File I/O error: {e}")

    def decrypt_file(self, input_path: str, output_path: str, aad: bytes = b""):
        """
        Decrypt a file with MAC verification.

        Args:
            input_path: Path to encrypted file
            output_path: Path to output file
            aad: Additional authenticated data

        Raises:
            AuthenticationError: If MAC verification fails
            CryptoOperationError: If file I/O fails
        """
        try:
            with open(input_path, 'rb') as f:
                data = f.read()

            # Пробуем дешифровать
            plaintext = self.decrypt(data, aad)

            # Записываем результат
            with open(output_path, 'wb') as f:
                f.write(plaintext)

        except AuthenticationError:
            # Катастрофический отказ: удаляем частично созданный файл
            import os
            if os.path.exists(output_path):
                os.remove(output_path)
            raise
        except (IOError, OSError) as e:
            raise CryptoOperationError(f"File I/O error: {e}")


# Factory function для удобства
def create_etm_mode(key: bytes, iv: bytes = None):
    """
    Factory function to create ETM mode.

    Args:
        key: Encryption key (16 bytes)
        iv: Initialization vector (optional)

    Returns:
        ETMMode instance
    """
    return ETMMode(key, iv)