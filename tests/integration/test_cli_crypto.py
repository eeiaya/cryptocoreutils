"""Интеграционные тесты для CLI команды crypto."""

import unittest
import subprocess
import sys
import os
import tempfile
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCLICrypto(unittest.TestCase):
    """Интеграционные тесты для шифрования/расшифрования через CLI."""

    def setUp(self):
        """Настройка временных файлов."""
        self.temp_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.temp_dir, 'input.txt')
        self.output_file = os.path.join(self.temp_dir, 'output.bin')
        self.decrypted_file = os.path.join(self.temp_dir, 'decrypted.txt')

        # Создаём тестовый файл
        with open(self.input_file, 'wb') as f:
            f.write(b'Hello, World! This is a test message for encryption.')

    def tearDown(self):
        """Очистка временных файлов."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def run_cli(self, *args):
        """Запуск CLI команды."""
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, 'main.py')] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_cbc_encrypt_decrypt(self):
        """Тест CBC шифрования и расшифрования."""
        key = '000102030405060708090a0b0c0d0e0f'

        # Шифрование
        result = self.run_cli(
            'crypto', '-alg', 'aes', '-mode', 'cbc', '-encrypt',
            '-key', key, '-input', self.input_file, '-output', self.output_file
        )
        self.assertEqual(result.returncode, 0, f"Encrypt failed: {result.stderr}")
        self.assertTrue(os.path.exists(self.output_file))

        # Расшифрование
        result = self.run_cli(
            'crypto', '-alg', 'aes', '-mode', 'cbc', '-decrypt',
            '-key', key, '-input', self.output_file, '-output', self.decrypted_file
        )
        self.assertEqual(result.returncode, 0, f"Decrypt failed: {result.stderr}")

        # Проверка
        with open(self.input_file, 'rb') as f:
            original = f.read()
        with open(self.decrypted_file, 'rb') as f:
            decrypted = f.read()
        self.assertEqual(original, decrypted)

    def test_gcm_encrypt_decrypt(self):
        """Тест GCM шифрования и расшифрования."""
        key = '000102030405060708090a0b0c0d0e0f'

        # Шифрование
        result = self.run_cli(
            'crypto', '-alg', 'aes', '-mode', 'gcm', '-encrypt',
            '-key', key, '-input', self.input_file, '-output', self.output_file
        )
        self.assertEqual(result.returncode, 0, f"Encrypt failed: {result.stderr}")

        # Расшифрование
        result = self.run_cli(
            'crypto', '-alg', 'aes', '-mode', 'gcm', '-decrypt',
            '-key', key, '-input', self.output_file, '-output', self.decrypted_file
        )
        self.assertEqual(result.returncode, 0, f"Decrypt failed: {result.stderr}")

        # Проверка
        with open(self.input_file, 'rb') as f:
            original = f.read()
        with open(self.decrypted_file, 'rb') as f:
            decrypted = f.read()
        self.assertEqual(original, decrypted)

    def test_missing_file_error(self):
        """Тест ошибки при отсутствующем файле."""
        result = self.run_cli(
            'crypto', '-alg', 'aes', '-mode', 'cbc', '-encrypt',
            '-key', '00' * 16, '-input', 'nonexistent.txt', '-output', 'out.bin'
        )
        self.assertNotEqual(result.returncode, 0)

    def test_invalid_key_error(self):
        """Тест ошибки при неверном формате ключа."""
        result = self.run_cli(
            'crypto', '-alg', 'aes', '-mode', 'cbc', '-encrypt',
            '-key', 'not_hex', '-input', self.input_file, '-output', self.output_file
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()