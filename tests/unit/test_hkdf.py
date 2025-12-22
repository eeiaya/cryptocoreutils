"""Unit-тесты для key hierarchy (HKDF-like)."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.kdf.hkdf import derive_key


class TestHKDF(unittest.TestCase):
    """Тесты для функции derive_key."""

    def test_basic_derivation(self):
        """Тест базовой деривации."""
        master = b'0' * 32
        key = derive_key(master, 'encryption', 32)
        self.assertEqual(len(key), 32)

    def test_deterministic(self):
        """Тест детерминированности."""
        master = b'0' * 32
        key1 = derive_key(master, 'encryption', 32)
        key2 = derive_key(master, 'encryption', 32)
        self.assertEqual(key1, key2)

    def test_context_separation(self):
        """Тест: разные контексты дают разные ключи."""
        master = b'0' * 32
        key1 = derive_key(master, 'encryption', 32)
        key2 = derive_key(master, 'authentication', 32)
        key3 = derive_key(master, 'signing', 32)

        self.assertNotEqual(key1, key2)
        self.assertNotEqual(key2, key3)
        self.assertNotEqual(key1, key3)

    def test_various_lengths(self):
        """Тест различных длин."""
        master = b'0' * 32
        for length in [1, 16, 32, 64, 128]:
            key = derive_key(master, 'test', length)
            self.assertEqual(len(key), length)

    def test_string_context(self):
        """Тест: строковый контекст работает."""
        master = b'0' * 32
        key = derive_key(master, 'test_context', 32)
        self.assertEqual(len(key), 32)


if __name__ == '__main__':
    unittest.main()