"""Unit-тесты для реализации PBKDF2."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.kdf.pbkdf2 import pbkdf2_hmac_sha256, generate_salt


class TestPBKDF2(unittest.TestCase):
    """Тесты для PBKDF2-HMAC-SHA256."""

    def test_basic_derivation(self):
        """Тест базовой деривации ключа."""
        key = pbkdf2_hmac_sha256(b'password', b'salt', 1, 32)
        self.assertEqual(len(key), 32)

    def test_known_vector_1(self):
        """Тест с известным вектором — 1 итерация."""
        key = pbkdf2_hmac_sha256(b'password', b'salt', 1, 32)
        expected = '120fb6cffcf8b32c43e7225256c4f837a86548c92ccc35480805987cb70be17b'
        self.assertEqual(key.hex(), expected)

    def test_known_vector_2(self):
        """Тест с известным вектором — 2 итерации."""
        key = pbkdf2_hmac_sha256(b'password', b'salt', 2, 32)
        expected = 'ae4d0c95af6b46d32d0adff928f06dd02a303f8ef3c251dfd6e2d85a95474c43'
        self.assertEqual(key.hex(), expected)

    def test_known_vector_4096(self):
        """Тест с известным вектором — 4096 итераций."""
        key = pbkdf2_hmac_sha256(b'password', b'salt', 4096, 32)
        expected = 'c5e478d59288c841aa530db6845c4c8d962893a001ce4e11a4963873aa98134a'
        self.assertEqual(key.hex(), expected)

    def test_string_password(self):
        """Тест: строковый пароль работает."""
        key1 = pbkdf2_hmac_sha256('password', b'salt', 1, 32)
        key2 = pbkdf2_hmac_sha256(b'password', b'salt', 1, 32)
        self.assertEqual(key1, key2)

    def test_various_lengths(self):
        """Тест различных длин вывода."""
        for length in [1, 16, 32, 64, 100]:
            key = pbkdf2_hmac_sha256(b'password', b'salt', 1, length)
            self.assertEqual(len(key), length)

    def test_deterministic(self):
        """Тест: одинаковые входы дают одинаковый выход."""
        key1 = pbkdf2_hmac_sha256(b'password', b'salt', 100, 32)
        key2 = pbkdf2_hmac_sha256(b'password', b'salt', 100, 32)
        self.assertEqual(key1, key2)

    def test_different_salts_different_keys(self):
        """Тест: разные соли дают разные ключи."""
        key1 = pbkdf2_hmac_sha256(b'password', b'salt1', 100, 32)
        key2 = pbkdf2_hmac_sha256(b'password', b'salt2', 100, 32)
        self.assertNotEqual(key1, key2)

    def test_generate_salt_length(self):
        """Тест длины генерируемой соли."""
        salt = generate_salt(16)
        self.assertEqual(len(salt), 16)

    def test_generate_salt_uniqueness(self):
        """Тест: генерируемые соли уникальны."""
        salts = set()
        for _ in range(100):
            salt = generate_salt(16)
            salts.add(salt.hex())
        self.assertEqual(len(salts), 100)


if __name__ == '__main__':
    unittest.main()