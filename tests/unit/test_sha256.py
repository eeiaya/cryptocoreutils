"""Unit-тесты для реализации SHA-256."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.hash.sha256 import SHA256


class TestSHA256(unittest.TestCase):
    """Тесты для хеш-функции SHA-256."""

    def test_empty_string(self):
        """Тест хеша пустой строки."""
        h = SHA256()
        h.update(b'')
        expected = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        self.assertEqual(h.hexdigest(), expected)

    def test_abc(self):
        """Тест хеша 'abc'."""
        h = SHA256()
        h.update(b'abc')
        expected = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
        self.assertEqual(h.hexdigest(), expected)

    def test_long_message(self):
        """Тест хеша длинного сообщения."""
        h = SHA256()
        h.update(b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq')
        expected = '248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1'
        self.assertEqual(h.hexdigest(), expected)

    def test_incremental_update(self):
        """Тест: инкрементальные обновления дают тот же результат."""
        # Одно обновление
        h1 = SHA256()
        h1.update(b'Hello, World!')

        # Несколько обновлений
        h2 = SHA256()
        h2.update(b'Hello, ')
        h2.update(b'World!')

        self.assertEqual(h1.hexdigest(), h2.hexdigest())

    def test_digest_length(self):
        """Тест: digest имеет длину 32 байта."""
        h = SHA256()
        h.update(b'test')
        self.assertEqual(len(h.digest()), 32)

    def test_hexdigest_length(self):
        """Тест: hexdigest имеет длину 64 символа."""
        h = SHA256()
        h.update(b'test')
        self.assertEqual(len(h.hexdigest()), 64)


if __name__ == '__main__':
    unittest.main()