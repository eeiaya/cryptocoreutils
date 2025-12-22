"""Unit-тесты для реализации HMAC."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.mac.hmac import HMAC, hmac_data, verify_hmac


class TestHMAC(unittest.TestCase):
    """Тесты для HMAC."""

    def test_rfc4231_vector1(self):
        """Тест RFC 4231 вектор 1."""
        key = bytes.fromhex('0b' * 20)
        data = b'Hi There'
        expected = 'b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7'

        hmac = HMAC(key, 'sha256')
        hmac.update(data)
        self.assertEqual(hmac.hexdigest(), expected)

    def test_rfc4231_vector2(self):
        """Тест RFC 4231 вектор 2 (key = 'Jefe')."""
        key = b'Jefe'
        data = b'what do ya want for nothing?'
        expected = '5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843'

        hmac = HMAC(key, 'sha256')
        hmac.update(data)
        self.assertEqual(hmac.hexdigest(), expected)

    def test_rfc4231_vector3(self):
        """Тест RFC 4231 вектор 3."""
        key = bytes.fromhex('aa' * 20)
        data = bytes.fromhex('dd' * 50)
        expected = '773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565fe'

        hmac = HMAC(key, 'sha256')
        hmac.update(data)
        self.assertEqual(hmac.hexdigest(), expected)

    def test_long_key(self):
        """Тест HMAC с ключом длиннее размера блока."""
        key = b'A' * 100  # > 64 байт — будет хеширован
        data = b'test data'

        hmac = HMAC(key, 'sha256')
        hmac.update(data)
        result = hmac.hexdigest()

        self.assertEqual(len(result), 64)

    def test_verify_hmac_correct(self):
        """Тест проверки HMAC с правильным значением."""
        self.assertTrue(verify_hmac('abc123', 'abc123'))
        self.assertTrue(verify_hmac('ABC123', 'abc123'))  # Регистронезависимо

    def test_verify_hmac_incorrect(self):
        """Тест проверки HMAC с неправильным значением."""
        self.assertFalse(verify_hmac('abc123', 'abc124'))
        self.assertFalse(verify_hmac('abc123', 'abc12'))

    def test_different_keys_different_hmac(self):
        """Тест: разные ключи дают разные HMAC."""
        data = b'same message'

        hmac1 = HMAC(b'key1', 'sha256')
        hmac1.update(data)

        hmac2 = HMAC(b'key2', 'sha256')
        hmac2.update(data)

        self.assertNotEqual(hmac1.hexdigest(), hmac2.hexdigest())


if __name__ == '__main__':
    unittest.main()