"""Unit тесты для режимов шифрования."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.modes.ecb import ECBMode
from cryptocoreutils.modes.cbc import CBCMode
from cryptocoreutils.modes.ctr import CTRMode
from cryptocoreutils.modes.cfb import CFBMode
from cryptocoreutils.modes.ofb import OFBMode


class TestECBMode(unittest.TestCase):
    """Тесты для ECB режима."""

    def setUp(self):
        self.key = '000102030405060708090a0b0c0d0e0f'
        self.cipher = ECBMode(self.key)

    def test_encrypt_decrypt_roundtrip(self):
        """Тест ECB encrypt/decrypt roundtrip."""
        plaintext = b'Hello, World! This is a test message.'
        ciphertext = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(ciphertext)
        self.assertEqual(decrypted, plaintext)

    def test_same_blocks_same_ciphertext(self):
        """Тест: ECB даёт одинаковый шифртекст для одинаковых блоков."""
        plaintext = b'AAAAAAAAAAAAAAAA' * 2  # Два одинаковых блока
        ciphertext = self.cipher.encrypt(plaintext)
        # В ECB одинаковые блоки дают одинаковый шифртекст
        self.assertEqual(ciphertext[:16], ciphertext[16:32])


class TestCBCMode(unittest.TestCase):
    """Тесты для CBC режима."""

    def setUp(self):
        self.key = '000102030405060708090a0b0c0d0e0f'
        self.iv = '101112131415161718191a1b1c1d1e1f'

    def test_encrypt_decrypt_roundtrip(self):
        """Тест CBC encrypt/decrypt roundtrip."""
        cipher = CBCMode(self.key, self.iv)
        plaintext = b'Hello, World! This is a test message.'
        ciphertext = cipher.encrypt(plaintext)

        cipher2 = CBCMode(self.key)  # Извлечёт IV из шифртекста
        decrypted = cipher2.decrypt(ciphertext)
        self.assertEqual(decrypted, plaintext)

    def test_iv_included_in_ciphertext(self):
        """Тест: IV добавлен в начало шифртекста."""
        cipher = CBCMode(self.key, self.iv)
        plaintext = b'Test message....'  # 16 байт
        ciphertext = cipher.encrypt(plaintext)

        # Первые 16 байт должны быть IV
        self.assertEqual(ciphertext[:16].hex(), self.iv)

    def test_random_iv_generation(self):
        """Тест: случайный IV генерируется если не указан."""
        cipher1 = CBCMode(self.key)
        cipher2 = CBCMode(self.key)

        ct1 = cipher1.encrypt(b'same message..!!')
        ct2 = cipher2.encrypt(b'same message..!!')

        # Разные IV должны дать разные шифртексты
        self.assertNotEqual(ct1, ct2)


class TestCTRMode(unittest.TestCase):
    """Тесты для CTR режима."""

    def setUp(self):
        self.key = '000102030405060708090a0b0c0d0e0f'

    def test_encrypt_decrypt_roundtrip(self):
        """Тест CTR encrypt/decrypt roundtrip."""
        cipher = CTRMode(self.key)
        plaintext = b'Hello, World! This is a test message.'
        ciphertext = cipher.encrypt(plaintext)

        cipher2 = CTRMode(self.key)
        decrypted = cipher2.decrypt(ciphertext)
        self.assertEqual(decrypted, plaintext)

    def test_no_padding_needed(self):
        """Тест: CTR не требует padding."""
        cipher = CTRMode(self.key)
        # Сообщение нечётной длины
        plaintext = b'12345'
        ciphertext = cipher.encrypt(plaintext)

        cipher2 = CTRMode(self.key)
        decrypted = cipher2.decrypt(ciphertext)
        self.assertEqual(decrypted, plaintext)


class TestCFBMode(unittest.TestCase):
    """Тесты для CFB режима."""

    def test_encrypt_decrypt_roundtrip(self):
        """Тест CFB encrypt/decrypt roundtrip."""
        key = '000102030405060708090a0b0c0d0e0f'
        cipher = CFBMode(key)
        plaintext = b'Hello, World!'
        ciphertext = cipher.encrypt(plaintext)

        cipher2 = CFBMode(key)
        decrypted = cipher2.decrypt(ciphertext)
        self.assertEqual(decrypted, plaintext)


class TestOFBMode(unittest.TestCase):
    """Тесты для OFB режима."""

    def test_encrypt_decrypt_roundtrip(self):
        """Тест OFB encrypt/decrypt roundtrip."""
        key = '000102030405060708090a0b0c0d0e0f'
        cipher = OFBMode(key)
        plaintext = b'Hello, World!'
        ciphertext = cipher.encrypt(plaintext)

        cipher2 = OFBMode(key)
        decrypted = cipher2.decrypt(ciphertext)
        self.assertEqual(decrypted, plaintext)


if __name__ == '__main__':
    unittest.main()