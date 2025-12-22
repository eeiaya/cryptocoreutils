"""Интеграционные тесты CLI для команды dgst."""

import unittest
import subprocess
import sys
import os
import tempfile
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCLIHash(unittest.TestCase):
    """Интеграционные тесты для хеширования CLI."""

    def setUp(self):
        """Подготовка временных файлов."""
        self.temp_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.temp_dir, 'input.txt')

        with open(self.input_file, 'wb') as f:
            f.write(b'Hello, World!')

    def tearDown(self):
        """Очистка временных файлов."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def run_cli(self, *args):
        """Запуск CLI команды."""
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, 'main.py')] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_sha256_hash(self):
        """Тест SHA-256 хеширования."""
        result = self.run_cli(
            'dgst', '-alg', 'sha256', '-input', self.input_file
        )
        self.assertEqual(result.returncode, 0)
        # Проверяем что вывод содержит hex хеш
        output = result.stdout.strip()
        self.assertEqual(len(output.split()[0]), 64)

    def test_sha3_256_hash(self):
        """Тест SHA3-256 хеширования."""
        result = self.run_cli(
            'dgst', '-alg', 'sha3-256', '-input', self.input_file
        )
        self.assertEqual(result.returncode, 0)
        output = result.stdout.strip()
        self.assertEqual(len(output.split()[0]), 64)

    def test_hmac_generation(self):
        """Тест генерации HMAC."""
        key = '000102030405060708090a0b0c0d0e0f'
        result = self.run_cli(
            'dgst', '-alg', 'sha256', '--hmac', '--key', key,
            '-input', self.input_file
        )
        self.assertEqual(result.returncode, 0)
        output = result.stdout.strip()
        self.assertEqual(len(output.split()[0]), 64)

    def test_missing_file_error(self):
        """Тест ошибки для несуществующего файла."""
        result = self.run_cli(
            'dgst', '-alg', 'sha256', '-input', 'nonexistent.txt'
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()