"""
NIST AES-128 test vectors.
Sources:
- FIPS 197 Appendix B
- NIST SP 800-38A
"""

import unittest
import sys
import os

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Попробуем разные варианты импорта
try:
    from cryptocoreutils.crypto.aes import AES128 as AES
    # Проверяем что это класс, а не модуль
    if not callable(AES):
        raise ImportError("AES is not callable")
except (ImportError, TypeError):
    try:
        from cryptocoreutils.crypto.aes import AESCipher as AES
    except ImportError:
        try:
            from cryptocoreutils.crypto import aes
            # Ищем класс в модуле
            if hasattr(aes, 'AES'):
                AES = aes.AES
            elif hasattr(aes, 'AESCipher'):
                AES = aes.AESCipher
            else:
                # Выводим что есть в модуле для диагностики
                print(f"Available in aes module: {dir(aes)}")
                raise ImportError("Cannot find AES class")
        except ImportError as e:
            print(f"Failed to import AES: {e}")
            raise


class TestAESNISTVectors(unittest.TestCase):
    """NIST AES-128 Known Answer Tests."""

    def test_fips197_appendix_b(self):
        """
        FIPS 197 Appendix B - AES-128 test vector.

        Key:        2b7e151628aed2a6abf7158809cf4f3c
        Plaintext:  3243f6a8885a308d313198a2e0370734
        Ciphertext: 3925841d02dc09fbdc118597196a0b32
        """
        key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
        plaintext = bytes.fromhex('3243f6a8885a308d313198a2e0370734')
        expected_ciphertext = bytes.fromhex('3925841d02dc09fbdc118597196a0b32')

        aes = AES(key)
        ciphertext = aes.encrypt_block(plaintext)

        self.assertEqual(ciphertext, expected_ciphertext,
                         "FIPS 197 Appendix B encryption failed")

        # Test decryption
        decrypted = aes.decrypt_block(ciphertext)
        self.assertEqual(decrypted, plaintext,
                         "FIPS 197 Appendix B decryption failed")

        print("✓ FIPS 197 Appendix B test passed")

    def test_nist_sp800_38a_ecb_vector1(self):
        """NIST SP 800-38A ECB-AES128 Vector 1."""
        key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
        plaintext = bytes.fromhex('6bc1bee22e409f96e93d7e117393172a')
        expected = bytes.fromhex('3ad77bb40d7a3660a89ecaf32466ef97')

        aes = AES(key)
        ciphertext = aes.encrypt_block(plaintext)

        self.assertEqual(ciphertext, expected,
                         "NIST SP 800-38A ECB Vector 1 failed")
        print("✓ NIST SP 800-38A ECB Vector 1 passed")

    def test_nist_sp800_38a_ecb_vector2(self):
        """NIST SP 800-38A ECB-AES128 Vector 2."""
        key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
        plaintext = bytes.fromhex('ae2d8a571e03ac9c9eb76fac45af8e51')
        expected = bytes.fromhex('f5d3d58503b9699de785895a96fdbaaf')

        aes = AES(key)
        ciphertext = aes.encrypt_block(plaintext)

        self.assertEqual(ciphertext, expected,
                         "NIST SP 800-38A ECB Vector 2 failed")
        print("✓ NIST SP 800-38A ECB Vector 2 passed")

    def test_nist_sp800_38a_ecb_vector3(self):
        """NIST SP 800-38A ECB-AES128 Vector 3."""
        key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
        plaintext = bytes.fromhex('30c81c46a35ce411e5fbc1191a0a52ef')
        expected = bytes.fromhex('43b1cd7f598ece23881b00e3ed030688')

        aes = AES(key)
        ciphertext = aes.encrypt_block(plaintext)

        self.assertEqual(ciphertext, expected,
                         "NIST SP 800-38A ECB Vector 3 failed")
        print("✓ NIST SP 800-38A ECB Vector 3 passed")

    def test_nist_sp800_38a_ecb_vector4(self):
        """NIST SP 800-38A ECB-AES128 Vector 4."""
        key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
        plaintext = bytes.fromhex('f69f2445df4f9b17ad2b417be66c3710')
        expected = bytes.fromhex('7b0c785e27e8ad3f8223207104725dd4')

        aes = AES(key)
        ciphertext = aes.encrypt_block(plaintext)

        self.assertEqual(ciphertext, expected,
                         "NIST SP 800-38A ECB Vector 4 failed")
        print("✓ NIST SP 800-38A ECB Vector 4 passed")

    def test_all_nist_ecb_vectors(self):
        """Run all NIST SP 800-38A ECB vectors in batch."""
        key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')

        vectors = [
            ('6bc1bee22e409f96e93d7e117393172a', '3ad77bb40d7a3660a89ecaf32466ef97'),
            ('ae2d8a571e03ac9c9eb76fac45af8e51', 'f5d3d58503b9699de785895a96fdbaaf'),
            ('30c81c46a35ce411e5fbc1191a0a52ef', '43b1cd7f598ece23881b00e3ed030688'),
            ('f69f2445df4f9b17ad2b417be66c3710', '7b0c785e27e8ad3f8223207104725dd4'),
        ]

        aes = AES(key)

        for i, (pt_hex, ct_hex) in enumerate(vectors, 1):
            plaintext = bytes.fromhex(pt_hex)
            expected_ct = bytes.fromhex(ct_hex)

            ciphertext = aes.encrypt_block(plaintext)
            self.assertEqual(ciphertext, expected_ct, f"ECB Vector {i} encryption failed")

            decrypted = aes.decrypt_block(ciphertext)
            self.assertEqual(decrypted, plaintext, f"ECB Vector {i} decryption failed")

        print(f"✓ All {len(vectors)} NIST ECB vectors passed")


if __name__ == '__main__':
    unittest.main(verbosity=2)