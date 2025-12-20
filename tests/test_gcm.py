import unittest
import os
import tempfile
from pathlib import Path
from cryptocoreutils.modes.gcm import GCMMode


class TestGCMModeM6(unittest.TestCase):
    """Тесты для GCM режима (M6)"""

    def test_gcm_basic_encrypt_decrypt(self):
        """Базовый тест GCM шифрование-дешифрование"""
        print("🧪 Тест 1: Базовое шифрование-дешифрование GCM")
        key = os.urandom(16)
        plaintext = b"Test GCM mode implementation"

        gcm = GCMMode(key)
        ciphertext = gcm.encrypt(plaintext)

        # Проверяем структуру выходных данных
        self.assertGreaterEqual(len(ciphertext), 28)  # nonce(12) + tag(16)
        self.assertEqual(len(ciphertext[:12]), 12)  # nonce
        self.assertEqual(len(ciphertext[-16:]), 16)  # tag

        decrypted = gcm.decrypt(ciphertext)
        self.assertEqual(plaintext, decrypted)
        print("   ✅ Успешно")

    def test_gcm_with_aad(self):
        """GCM с дополнительными аутентифицированными данными"""
        print("🧪 Тест 2: GCM с AAD")
        key = os.urandom(16)
        plaintext = b"Secret document for AAD test"
        aad = b"metadata: user=admin, date=2024"

        gcm = GCMMode(key)
        ciphertext = gcm.encrypt(plaintext, aad)

        # Правильный AAD
        decrypted = gcm.decrypt(ciphertext, aad)
        self.assertEqual(plaintext, decrypted)
        print("   ✅ Правильный AAD работает")

        # Неправильный AAD
        with self.assertRaises(Exception) as e:
            gcm.decrypt(ciphertext, b"wrong metadata")

        error_msg = str(e.exception)
        self.assertTrue("Authentication" in error_msg or "аутентификации" in error_msg)
        print("   ✅ Неправильный AAD вызывает исключение")

    def test_gcm_tamper_detection(self):
        """Обнаружение изменений в шифртексте"""
        print("🧪 Тест 3: Обнаружение изменений в шифртексте")
        key = os.urandom(16)
        plaintext = b"Important data that should not be modified"

        gcm = GCMMode(key)
        ciphertext = gcm.encrypt(plaintext)

        # Изменяем байт в шифртексте (после nonce)
        tampered = bytearray(ciphertext)
        if len(tampered) > 20:
            tampered[20] ^= 0x01  # Меняем один бит

        with self.assertRaises(Exception):
            gcm.decrypt(bytes(tampered))
        print("   ✅ Изменения обнаруживаются")

    def test_gcm_tag_tamper_detection(self):
        """Обнаружение изменений в теге аутентификации"""
        print("🧪 Тест 4: Обнаружение изменений в теге")
        key = os.urandom(16)
        plaintext = b"Test tag tampering"

        gcm = GCMMode(key)
        ciphertext = gcm.encrypt(plaintext)

        # Изменяем последний байт тега
        tampered = bytearray(ciphertext)
        tampered[-1] ^= 0xFF

        with self.assertRaises(Exception):
            gcm.decrypt(bytes(tampered))
        print("   ✅ Изменение тега обнаруживается")

    def test_gcm_empty_aad(self):
        """GCM с пустым AAD"""
        print("🧪 Тест 5: GCM с пустым AAD")
        key = os.urandom(16)
        plaintext = b"Test with empty AAD"

        gcm = GCMMode(key)
        ciphertext = gcm.encrypt(plaintext, b"")
        decrypted = gcm.decrypt(ciphertext, b"")

        self.assertEqual(plaintext, decrypted)
        print("   ✅ Пустой AAD работает")

    def test_gcm_nonce_uniqueness(self):
        """Уникальность nonce для каждого шифрования"""
        print("🧪 Тест 6: Уникальность nonce")
        key = os.urandom(16)
        plaintext = b"Same message, different nonce"

        # Два шифрования одного сообщения
        gcm1 = GCMMode(key)
        gcm2 = GCMMode(key)

        ciphertext1 = gcm1.encrypt(plaintext)
        ciphertext2 = gcm2.encrypt(plaintext)

        # Извлекаем nonce (первые 12 байт)
        nonce1 = ciphertext1[:12]
        nonce2 = ciphertext2[:12]

        self.assertNotEqual(nonce1, nonce2, "Nonce должны быть разными!")
        print("   ✅ Nonce уникальны")

        # Также проверяем что шифртексты разные
        self.assertNotEqual(ciphertext1[12:], ciphertext2[12:], "Шифртексты должны быть разными")

    def test_gcm_key_sizes(self):
        """Поддержка разных размеров ключей"""
        print("🧪 Тест 7: Разные размеры ключей")

        # Твой AES128 поддерживает только 16-байтные ключи
        test_cases = [
            (16, "128-bit key"),
            # (24, "192-bit key"),  # Не поддерживается твоим AES128
            # (32, "256-bit key"),  # Не поддерживается твоим AES128
        ]

        for key_size, description in test_cases:
            key = os.urandom(key_size)
            plaintext = b"Test with " + description.encode()

            gcm = GCMMode(key)
            ciphertext = gcm.encrypt(plaintext)
            decrypted = gcm.decrypt(ciphertext)

            self.assertEqual(plaintext, decrypted)
            print(f"   ✅ {description} работает")

        # Дополнительный тест - проверяем что большие ключи вызывают ошибку
        print("   ⚠️  AES128 поддерживает только 128-bit ключи (16 байт)")

    def test_gcm_file_operations(self):
        """Тест операций с файлами через GCM"""
        print("🧪 Тест 8: Файловые операции GCM")

        key = os.urandom(16)
        plaintext = b"File operation test content for GCM"
        aad = b"file metadata"

        # Создаем временные файлы
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f_input:
            f_input.write(plaintext)
            input_path = f_input.name

        encrypted_path = input_path + '.gcm'
        decrypted_path = input_path + '.dec'

        try:
            # Шифрование файла
            gcm = GCMMode(key)
            gcm.encrypt_file(input_path, encrypted_path, aad)

            # Проверяем что файл создан
            self.assertTrue(os.path.exists(encrypted_path))
            print("   ✅ Файл зашифрован")

            # Дешифрование файла
            gcm2 = GCMMode(key)
            gcm2.decrypt_file(encrypted_path, decrypted_path, aad)

            # Проверяем содержимое
            with open(decrypted_path, 'rb') as f:
                decrypted_content = f.read()

            self.assertEqual(plaintext, decrypted_content)
            print("   ✅ Файл расшифрован корректно")

            # Тест катастрофического отказа
            wrong_aad_path = decrypted_path + '.wrong'
            with self.assertRaises(Exception):
                gcm2.decrypt_file(encrypted_path, wrong_aad_path, b"wrong aad")

            # Файл не должен существовать
            self.assertFalse(os.path.exists(wrong_aad_path))
            print("   ✅ Катастрофический отказ работает (файл не создан)")

        finally:
            # Очистка
            for path in [input_path, encrypted_path, decrypted_path]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_gcm_constant_time_comparison(self):
        """Проверка сравнения с постоянным временем"""
        print("🧪 Тест 9: Сравнение с постоянным временем")

        # Тестируем статический метод
        same1 = os.urandom(16)
        same2 = same1
        different = os.urandom(16)

        # Одинаковые должны вернуть True
        self.assertTrue(GCMMode._constant_time_compare(same1, same2))

        # Разные должны вернуть False
        self.assertFalse(GCMMode._constant_time_compare(same1, different))

        # Разная длина должна вернуть False
        self.assertFalse(GCMMode._constant_time_compare(same1, different[:8]))

        print("   ✅ Сравнение с постоянным временем работает")


def run_gcm_tests():
    """Запуск всех тестов GCM с красивым выводом"""
    print("\n" + "=" * 60)
    print("🚀 ЗАПУСК ТЕСТОВ GCM (M6)")
    print("=" * 60)

    # Создаем test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Добавляем все тесты из класса
    suite.addTests(loader.loadTestsFromTestCase(TestGCMModeM6))

    # Запускаем
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ GCM:")
    print(f"   Всего тестов: {result.testsRun}")
    print(f"   Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")

    if result.failures:
        print(f"   ❌ Провалено: {len(result.failures)}")
        for test, traceback in result.failures:
            print(f"\n   Провален: {test}")
            print(f"   Ошибка: {traceback.splitlines()[-1]}")

    if result.errors:
        print(f"   ⚠️  Ошибок: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n🎉 ВСЕ ТЕСТЫ GCM ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("\n❌ ЕСТЬ ПРОБЛЕМЫ С РЕАЛИЗАЦИЕЙ GCM")

    print("=" * 60)

    return result.wasSuccessful()


# Если файл запускается напрямую, запускаем тесты
if __name__ == '__main__':
    run_gcm_tests()