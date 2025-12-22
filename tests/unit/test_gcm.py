"""Unit-тесты для режима GCM."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.modes.gcm import GCMMode


class TestGCMMode(unittest.TestCase):
    """Тесты для аутентифицированного шифрования GCM."""

    def setUp(self):
        #self.key = '000102030405060708090a0b0c0d0e0f'
        self.key = bytes.fromhex('000102030405060708090a0b0c0d0e0f')

    def test_encrypt_decrypt_roundtrip(self):
        """Тест GCM encrypt/decrypt roundtrip."""
        cipher = GCMMode(self.key)
        plaintext = b'Hello, World!'
        ciphertext = cipher.encrypt(plaintext)

        cipher2 = GCMMode(self.key)
        decrypted = cipher2.decrypt(ciphertext)
        self.assertEqual(decrypted, plaintext)

    def test_encrypt_decrypt_with_aad(self):
        """Тест GCM с Additional Authenticated Data."""
        cipher = GCMMode(self.key)
        plaintext = b'Secret message'
        aad = b'header data'
        ciphertext = cipher.encrypt(plaintext, aad)

        cipher2 = GCMMode(self.key)
        decrypted = cipher2.decrypt(ciphertext, aad)
        self.assertEqual(decrypted, plaintext)

    def test_wrong_aad_fails(self):
        """Тест: неверный AAD вызывает ошибку аутентификации."""
        cipher = GCMMode(self.key)
        plaintext = b'Secret message'
        aad = b'correct aad'
        ciphertext = cipher.encrypt(plaintext, aad)

        cipher2 = GCMMode(self.key)
        with self.assertRaises(Exception):
            cipher2.decrypt(ciphertext, b'wrong aad')

    def test_tampered_ciphertext_fails(self):
        """Тест: изменённый шифртекст вызывает ошибку аутентификации."""
        cipher = GCMMode(self.key)
        plaintext = b'Secret message'
        ciphertext = bytearray(cipher.encrypt(plaintext))

        # Изменяем шифртекст
        if len(ciphertext) > 20:
            ciphertext[20] ^= 0xFF

        cipher2 = GCMMode(self.key)
        with self.assertRaises(Exception):
            cipher2.decrypt(bytes(ciphertext))

    def test_wrong_key_fails(self):
        """Тест: неверный ключ вызывает ошибку аутентификации."""
        cipher = GCMMode(self.key)
        plaintext = b'Secret message'
        ciphertext = cipher.encrypt(plaintext)

        #wrong_key = '0f0e0d0c0b0a09080706050403020100'
        wrong_key = bytes.fromhex('0f0e0d0c0b0a09080706050403020100')
        cipher2 = GCMMode(wrong_key)
        with self.assertRaises(Exception):
            cipher2.decrypt(ciphertext)

    def test_empty_plaintext(self):
        """Тест GCM с пустым plaintext (только AAD)."""
        cipher = GCMMode(self.key)
        plaintext = b''
        aad = b'metadata only'
        ciphertext = cipher.encrypt(plaintext, aad)

        cipher2 = GCMMode(self.key)
        decrypted = cipher2.decrypt(ciphertext, aad)
        self.assertEqual(decrypted, plaintext)


if __name__ == '__main__':
    unittest.main()