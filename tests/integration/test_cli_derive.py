"""Интеграционные тесты CLI для команды derive."""

import unittest
import subprocess
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCLIDerive(unittest.TestCase):
    """Интеграционные тесты для деривации ключей CLI."""

    def run_cli(self, *args):
        """Запуск CLI команды."""
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, 'main.py')] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_basic_derive(self):
        """Тест базовой деривации ключа."""
        result = self.run_cli(
            'derive', '--password', 'test', '--salt', '00' * 16,
            '--iterations', '1', '--length', '32'
        )
        self.assertEqual(result.returncode, 0, f"Failed: {result.stderr}")

        # Вывод должен быть KEY_HEX SALT_HEX
        output = result.stdout.strip()
        parts = output.split()
        self.assertEqual(len(parts), 2)
        self.assertEqual(len(parts[0]), 64)  # 32 байта = 64 hex символа

    def test_known_vector(self):
        """Тест против известного PBKDF2 вектора."""
        result = self.run_cli(
            'derive', '--password', 'password', '--salt', '73616c74',
            '--iterations', '1', '--length', '32'
        )
        self.assertEqual(result.returncode, 0)

        output = result.stdout.strip().split()[0]
        expected = '120fb6cffcf8b32c43e7225256c4f837a86548c92ccc35480805987cb70be17b'
        self.assertEqual(output, expected)

    def test_key_hierarchy(self):
        """Тест деривации иерархии ключей."""
        master_key = '00' * 32

        result1 = self.run_cli(
            'derive', '--master-key', master_key, '--context', 'encryption'
        )
        result2 = self.run_cli(
            'derive', '--master-key', master_key, '--context', 'authentication'
        )

        self.assertEqual(result1.returncode, 0)
        self.assertEqual(result2.returncode, 0)

        # Разные контексты должны дать разные ключи
        self.assertNotEqual(result1.stdout.strip(), result2.stdout.strip())

    def test_missing_password_error(self):
        """Тест ошибки при отсутствии пароля."""
        result = self.run_cli('derive', '--salt', '00' * 16)
        self.assertNotEqual(result.returncode, 0)

    def test_deterministic(self):
        """Тест: одинаковые входы дают одинаковый выход."""
        args = ['derive', '--password', 'test', '--salt', '00' * 16,
                '--iterations', '100', '--length', '32']

        result1 = self.run_cli(*args)
        result2 = self.run_cli(*args)

        self.assertEqual(result1.stdout, result2.stdout)


if __name__ == '__main__':
    unittest.main()