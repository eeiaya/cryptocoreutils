"""Unit-тесты для CSPRNG."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.csprng import generate_random_bytes


class TestCSPRNG(unittest.TestCase):
    """Тесты для криптографически безопасного ГСЧ."""

    def test_length(self):
        """Тест: генерируется правильное количество байт."""
        for length in [1, 16, 32, 64, 128, 256]:
            data = generate_random_bytes(length)
            self.assertEqual(len(data), length)

    def test_uniqueness(self):
        """Тест: генерируемые значения уникальны."""
        values = set()
        for _ in range(100):
            data = generate_random_bytes(16)
            values.add(data.hex())
        self.assertEqual(len(values), 100)

    def test_returns_bytes(self):
        """Тест: возвращается тип bytes."""
        data = generate_random_bytes(16)
        self.assertIsInstance(data, bytes)

    def test_not_all_zeros(self):
        """Тест: результат не все нули (статистический)."""
        # Маловероятно что 32 случайных байта будут все нули
        data = generate_random_bytes(32)
        self.assertNotEqual(data, b'\x00' * 32)


if __name__ == '__main__':
    unittest.main()