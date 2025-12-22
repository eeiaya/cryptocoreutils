import unittest
import os
import tempfile
from cryptocoreutils.hash.sha256 import sha256_data, sha256_file
from cryptocoreutils.hash.sha3_256 import sha3_256_data, sha3_256_file


class TestHashFunctions(unittest.TestCase):

    def test_sha256_empty_string(self):
        """Тест SHA-256 для пустой строки"""
        result = sha256_data("")
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.assertEqual(result, expected)

    def test_sha256_abc(self):
        """Тест SHA-256 для строки 'abc'"""
        result = sha256_data("abc")
        expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        self.assertEqual(result, expected)

    def test_sha3_256_empty_string(self):
        """Тест SHA3-256 для пустой строки"""
        result = sha3_256_data("")
        expected = "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"
        self.assertEqual(result, expected)

    def test_sha3_256_abc(self):
        """Тест SHA3-256 для строки 'abc'"""
        result = sha3_256_data("abc")
        expected = "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"
        self.assertEqual(result, expected)

    def test_sha256_file(self):
        """Тест SHA-256 для файла"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_file = f.name

        try:
            result = sha256_file(temp_file)
            expected = sha256_data("test content")
            self.assertEqual(result, expected)
        finally:
            os.unlink(temp_file)

    def test_sha3_256_file(self):
        """Тест SHA3-256 для файла"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_file = f.name

        try:
            result = sha3_256_file(temp_file)
            expected = sha3_256_data("test content")
            self.assertEqual(result, expected)
        finally:
            os.unlink(temp_file)

    def test_avalanche_effect_sha256(self):
        """Тест эффекта лавины для SHA-256"""
        hash1 = sha256_data("Hello, world!")
        hash2 = sha256_data("Hello, world?")  # Изменен последний символ

        # Преобразуем в бинарный вид и считаем различающиеся биты
        bin1 = bin(int(hash1, 16))[2:].zfill(256)
        bin2 = bin(int(hash2, 16))[2:].zfill(256)

        diff_count = sum(bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

        # Эффект лавины: должно измениться ~128 битов (50%)
        self.assertTrue(100 < diff_count < 156,
                        f"Слабый эффект лавины: изменилось только {diff_count} битов")


if __name__ == '__main__':
    unittest.main()