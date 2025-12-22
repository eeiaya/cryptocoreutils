"""
PBKDF2-HMAC-SHA256 test vectors.
Vectors verified against Python hashlib.pbkdf2_hmac
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.kdf.pbkdf2 import pbkdf2_hmac_sha256


class TestPBKDF2Vectors(unittest.TestCase):
    """PBKDF2-HMAC-SHA256 Known Answer Tests."""

    def test_vector_1_iteration(self):
        """
        PBKDF2-HMAC-SHA256 with 1 iteration.
        Password: "password"
        Salt: "salt"
        Iterations: 1
        dkLen: 32
        """
        result = pbkdf2_hmac_sha256(b'password', b'salt', 1, 32)
        expected = bytes.fromhex('120fb6cffcf8b32c43e7225256c4f837a86548c92ccc35480805987cb70be17b')

        self.assertEqual(result, expected)
        print("✓ PBKDF2 1-iteration test passed")

    def test_vector_2_iterations(self):
        """
        PBKDF2-HMAC-SHA256 with 2 iterations.
        """
        result = pbkdf2_hmac_sha256(b'password', b'salt', 2, 32)
        expected = bytes.fromhex('ae4d0c95af6b46d32d0adff928f06dd02a303f8ef3c251dfd6e2d85a95474c43')

        self.assertEqual(result, expected)
        print("✓ PBKDF2 2-iteration test passed")

    def test_vector_4096_iterations(self):
        """
        PBKDF2-HMAC-SHA256 with 4096 iterations.
        """
        result = pbkdf2_hmac_sha256(b'password', b'salt', 4096, 32)
        expected = bytes.fromhex('c5e478d59288c841aa530db6845c4c8d962893a001ce4e11a4963873aa98134a')

        self.assertEqual(result, expected)
        print("✓ PBKDF2 4096-iteration test passed")

    def test_vector_long_password_salt(self):
        """
        PBKDF2-HMAC-SHA256 with long password and salt.
        """
        result = pbkdf2_hmac_sha256(
            b'passwordPASSWORDpassword',
            b'saltSALTsaltSALTsaltSALTsaltSALTsalt',
            4096,
            40
        )
        expected = bytes.fromhex('348c89dbcbd32b2f32d814b8116e84cf2b17347ebc1800181c4e2a1fb8dd53e1c635518c7dac47e9')

        self.assertEqual(result, expected)
        print("✓ PBKDF2 long password/salt test passed")

    def test_short_output(self):
        """Test PBKDF2 with shorter output (16 bytes)."""
        result = pbkdf2_hmac_sha256(b'password', b'salt', 1, 16)
        expected = bytes.fromhex('120fb6cffcf8b32c43e7225256c4f837')

        self.assertEqual(result, expected)
        print("✓ PBKDF2 short output test passed")

    def test_long_output_dynamic(self):
        """
        Test PBKDF2 with longer output (64 bytes - 2 blocks).
        Compares against Python's hashlib implementation.
        """
        import hashlib

        password = b'password'
        salt = b'salt'
        iterations = 1
        dklen = 64

        # Получаем эталонное значение из hashlib
        expected = hashlib.pbkdf2_hmac('sha256', password, salt, iterations, dklen)

        # Проверяем нашу реализацию
        result = pbkdf2_hmac_sha256(password, salt, iterations, dklen)

        self.assertEqual(result, expected,
                         f"Expected: {expected.hex()}\nGot: {result.hex()}")
        print("✓ PBKDF2 long output (64 bytes) test passed")

    def test_string_password(self):
        """Test that string password produces same result as bytes."""
        result_str = pbkdf2_hmac_sha256('password', b'salt', 1, 32)
        result_bytes = pbkdf2_hmac_sha256(b'password', b'salt', 1, 32)

        self.assertEqual(result_str, result_bytes)
        print("✓ PBKDF2 string password test passed")

    def test_various_lengths(self):
        """Test PBKDF2 produces correct length output."""
        for length in [1, 16, 32, 48, 64, 100]:
            result = pbkdf2_hmac_sha256(b'password', b'salt', 1, length)
            self.assertEqual(len(result), length, f"Wrong length for dklen={length}")
        print("✓ PBKDF2 various lengths test passed")

    def test_deterministic(self):
        """Test that same inputs produce same output."""
        result1 = pbkdf2_hmac_sha256(b'password', b'salt', 100, 32)
        result2 = pbkdf2_hmac_sha256(b'password', b'salt', 100, 32)
        self.assertEqual(result1, result2)
        print("✓ PBKDF2 deterministic test passed")

    def test_different_salts_different_output(self):
        """Test that different salts produce different keys."""
        result1 = pbkdf2_hmac_sha256(b'password', b'salt1', 1, 32)
        result2 = pbkdf2_hmac_sha256(b'password', b'salt2', 1, 32)
        self.assertNotEqual(result1, result2)
        print("✓ PBKDF2 different salts test passed")


if __name__ == '__main__':
    unittest.main(verbosity=2)