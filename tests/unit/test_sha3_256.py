"""Unit-тесты для реализации SHA3-256."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.hash.sha3_256 import SHA3_256


class TestSHA3_256(unittest.TestCase):
    """Тесты для хеш-функции SHA3-256."""

    def test_empty_string(self):
        """Тест хеша пустой строки."""
        h = SHA3_256()
        h.update(b'')
        expected = 'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a'
        self.assertEqual(h.hexdigest(), expected)

    def test_abc(self):
        """Тест хеша 'abc'."""
        h = SHA3_256()
        h.update(b'abc')
        expected = '3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532'
        self.assertEqual(h.hexdigest(), expected)

    def test_digest_length(self):
        """Тест: digest имеет длину 32 байта."""
        h = SHA3_256()
        h.update(b'test')
        self.assertEqual(len(h.digest()), 32)

    def test_incremental_update(self):
        """Тест инкрементального обновления."""
        h1 = SHA3_256()
        h1.update(b'Hello, World!')

        h2 = SHA3_256()
        h2.update(b'Hello, ')
        h2.update(b'World!')

        self.assertEqual(h1.hexdigest(), h2.hexdigest())


if __name__ == '__main__':
    unittest.main()