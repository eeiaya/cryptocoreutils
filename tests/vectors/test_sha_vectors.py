"""
NIST SHA-256 и SHA3-256 test vectors.
Sources:
- NIST FIPS 180-4 (SHA-256)
- NIST FIPS 202 (SHA3-256)
"""

import unittest
import sys
import os

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.hash.sha256 import SHA256
from cryptocoreutils.hash.sha3_256 import SHA3_256


class TestSHA256NISTVectors(unittest.TestCase):
    """NIST SHA-256 Known Answer Tests from FIPS 180-4."""

    def test_empty_string(self):
        """
        SHA-256 of empty string.
        Input: "" (empty)
        Expected: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        """
        h = SHA256()
        h.update(b'')
        expected = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

        self.assertEqual(h.hexdigest(), expected,
                         "SHA-256 empty string vector failed")
        print("✓ SHA-256 empty string test passed")

    def test_abc(self):
        """
        SHA-256 of "abc".
        Input: "abc"
        Expected: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
        """
        h = SHA256()
        h.update(b'abc')
        expected = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'

        self.assertEqual(h.hexdigest(), expected,
                         "SHA-256 'abc' vector failed")
        print("✓ SHA-256 'abc' test passed")

    def test_448_bits(self):
        """
        SHA-256 of 448-bit message (56 bytes).
        Input: "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
        Expected: 248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1
        """
        h = SHA256()
        h.update(b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq')
        expected = '248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1'

        self.assertEqual(h.hexdigest(), expected,
                         "SHA-256 448-bit message vector failed")
        print("✓ SHA-256 448-bit message test passed")

    def test_896_bits(self):
        """
        SHA-256 of 896-bit message (112 bytes).
        Input: "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmn
                hijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu"
        Expected: cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1
        """
        h = SHA256()
        msg = (b'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmn'
               b'hijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu')
        h.update(msg)
        expected = 'cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1'

        self.assertEqual(h.hexdigest(), expected,
                         "SHA-256 896-bit message vector failed")
        print("✓ SHA-256 896-bit message test passed")

    def test_million_a(self):
        """
        SHA-256 of one million 'a' characters.
        Input: "a" repeated 1,000,000 times
        Expected: cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0
        """
        h = SHA256()
        # Обновляем частями чтобы не забить память
        chunk = b'a' * 1000
        for _ in range(1000):
            h.update(chunk)
        expected = 'cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0'

        self.assertEqual(h.hexdigest(), expected,
                         "SHA-256 million 'a' vector failed")
        print("✓ SHA-256 million 'a' test passed")

    def test_incremental_update(self):
        """Test that incremental updates produce same result as single update."""
        # Одно обновление
        h1 = SHA256()
        h1.update(b'Hello, World!')

        # Несколько обновлений
        h2 = SHA256()
        h2.update(b'Hello, ')
        h2.update(b'World!')

        self.assertEqual(h1.hexdigest(), h2.hexdigest(),
                         "SHA-256 incremental update failed")
        print("✓ SHA-256 incremental update test passed")

    def test_digest_length(self):
        """Test that digest is 32 bytes."""
        h = SHA256()
        h.update(b'test')
        self.assertEqual(len(h.digest()), 32,
                         "SHA-256 digest length should be 32 bytes")
        print("✓ SHA-256 digest length test passed")

    def test_hexdigest_length(self):
        """Test that hexdigest is 64 characters."""
        h = SHA256()
        h.update(b'test')
        self.assertEqual(len(h.hexdigest()), 64,
                         "SHA-256 hexdigest length should be 64 chars")
        print("✓ SHA-256 hexdigest length test passed")


class TestSHA3_256NISTVectors(unittest.TestCase):
    """NIST SHA3-256 Known Answer Tests from FIPS 202."""

    def test_empty_string(self):
        """
        SHA3-256 of empty string.
        Input: "" (empty)
        Expected: a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
        """
        h = SHA3_256()
        h.update(b'')
        expected = 'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a'

        self.assertEqual(h.hexdigest(), expected,
                         "SHA3-256 empty string vector failed")
        print("✓ SHA3-256 empty string test passed")

    def test_abc(self):
        """
        SHA3-256 of "abc".
        Input: "abc"
        Expected: 3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532
        """
        h = SHA3_256()
        h.update(b'abc')
        expected = '3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532'

        self.assertEqual(h.hexdigest(), expected,
                         "SHA3-256 'abc' vector failed")
        print("✓ SHA3-256 'abc' test passed")

    def test_448_bits(self):
        """
        SHA3-256 of 448-bit message.
        Input: "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
        Expected: 41c0dba2a9d6240849100376a8235e2c82e1b9998a999e21db32dd97496d3376
        """
        h = SHA3_256()
        h.update(b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq')
        expected = '41c0dba2a9d6240849100376a8235e2c82e1b9998a999e21db32dd97496d3376'

        self.assertEqual(h.hexdigest(), expected,
                         "SHA3-256 448-bit message vector failed")
        print("✓ SHA3-256 448-bit message test passed")

    def test_200_bytes_0xa3(self):
        """
        SHA3-256 of 200 bytes (0xa3 repeated).
        Input: 0xa3 repeated 200 times
        Expected: 79f38adec5c20307a98ef76e8324afbfd46cfd81b22e3973c65fa1bd9de31787
        """
        h = SHA3_256()
        h.update(bytes([0xa3] * 200))
        expected = '79f38adec5c20307a98ef76e8324afbfd46cfd81b22e3973c65fa1bd9de31787'

        self.assertEqual(h.hexdigest(), expected,
                         "SHA3-256 200-byte 0xa3 vector failed")
        print("✓ SHA3-256 200-byte test passed")

    def test_digest_length(self):
        """Test that digest is 32 bytes."""
        h = SHA3_256()
        h.update(b'test')
        self.assertEqual(len(h.digest()), 32,
                         "SHA3-256 digest length should be 32 bytes")
        print("✓ SHA3-256 digest length test passed")

    def test_hexdigest_length(self):
        """Test that hexdigest is 64 characters."""
        h = SHA3_256()
        h.update(b'test')
        self.assertEqual(len(h.hexdigest()), 64,
                         "SHA3-256 hexdigest length should be 64 chars")
        print("✓ SHA3-256 hexdigest length test passed")

    def test_incremental_update(self):
        """Test that incremental updates produce same result as single update."""
        # Одно обновление
        h1 = SHA3_256()
        h1.update(b'Hello, World!')

        # Несколько обновлений
        h2 = SHA3_256()
        h2.update(b'Hello, ')
        h2.update(b'World!')

        self.assertEqual(h1.hexdigest(), h2.hexdigest(),
                         "SHA3-256 incremental update failed")
        print("✓ SHA3-256 incremental update test passed")


class TestSHAComparison(unittest.TestCase):
    """Тесты сравнения SHA-256 и SHA3-256."""

    def test_different_algorithms_different_output(self):
        """SHA-256 и SHA3-256 должны давать разный результат."""
        data = b'test message'

        sha256 = SHA256()
        sha256.update(data)

        sha3 = SHA3_256()
        sha3.update(data)

        self.assertNotEqual(sha256.hexdigest(), sha3.hexdigest(),
                            "SHA-256 and SHA3-256 should produce different hashes")
        print("✓ SHA-256 and SHA3-256 produce different outputs")

    def test_both_deterministic(self):
        """Оба алгоритма должны быть детерминированными."""
        data = b'deterministic test'

        # SHA-256
        h1 = SHA256()
        h1.update(data)
        h2 = SHA256()
        h2.update(data)
        self.assertEqual(h1.hexdigest(), h2.hexdigest())

        # SHA3-256
        h3 = SHA3_256()
        h3.update(data)
        h4 = SHA3_256()
        h4.update(data)
        self.assertEqual(h3.hexdigest(), h4.hexdigest())

        print("✓ Both algorithms are deterministic")


def run_all_sha_tests():
    """Запуск всех SHA тестов с подробным выводом."""
    print("=" * 70)
    print("SHA-256 and SHA3-256 Test Vectors")
    print("=" * 70)
    print()

    # Создаём тестовый набор
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestSHA256NISTVectors))
    suite.addTests(loader.loadTestsFromTestCase(TestSHA3_256NISTVectors))
    suite.addTests(loader.loadTestsFromTestCase(TestSHAComparison))

    # Запускаем
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✅ All SHA test vectors passed!")
    else:
        print("❌ Some tests failed!")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == '__main__':
    # Можно запустить как:
    # python tests/vectors/test_sha_vectors.py
    # или
    # python -m pytest tests/vectors/test_sha_vectors.py -v

    run_all_sha_tests()