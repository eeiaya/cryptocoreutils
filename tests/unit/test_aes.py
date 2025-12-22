"""Unit-тесты для реализации AES."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.crypto.aes import AES128 as AES
#from cryptocoreutils.crypto.aes import AES

class TestAES(unittest.TestCase):
    """Тесты для блочного шифра AES."""

    def setUp(self):
        """Настройка тестовых данных."""
        self.key = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
        self.aes = AES(self.key)

    def test_encrypt_decrypt_roundtrip(self):
        """Тест: шифрование и расшифрование возвращает оригинал."""
        plaintext = b'0123456789abcdef'  # 16 байт
        ciphertext = self.aes.encrypt_block(plaintext)
        decrypted = self.aes.decrypt_block(ciphertext)
        self.assertEqual(decrypted, plaintext)

    def test_encrypt_block_length(self):
        """Тест: зашифрованный блок имеет длину 16 байт."""
        plaintext = b'0123456789abcdef'
        ciphertext = self.aes.encrypt_block(plaintext)
        self.assertEqual(len(ciphertext), 16)

    def test_different_keys_different_output(self):
        """Тест: разные ключи дают разный шифртекст."""
        plaintext = b'0123456789abcdef'

        key1 = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
        key2 = bytes.fromhex('0f0e0d0c0b0a09080706050403020100')

        aes1 = AES(key1)
        aes2 = AES(key2)

        ct1 = aes1.encrypt_block(plaintext)
        ct2 = aes2.encrypt_block(plaintext)

        self.assertNotEqual(ct1, ct2)

    def test_deterministic(self):
        """Тест: шифрование детерминировано."""
        plaintext = b'Test block......'
        ct1 = self.aes.encrypt_block(plaintext)
        ct2 = self.aes.encrypt_block(plaintext)
        self.assertEqual(ct1, ct2)

    def test_nist_test_vector(self):
        """Тест против NIST AES вектора."""
        # NIST FIPS 197 Appendix B
        key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
        plaintext = bytes.fromhex('3243f6a8885a308d313198a2e0370734')
        expected = bytes.fromhex('3925841d02dc09fbdc118597196a0b32')

        aes = AES(key)
        ciphertext = aes.encrypt_block(plaintext)
        self.assertEqual(ciphertext, expected)


if __name__ == '__main__':
    unittest.main()