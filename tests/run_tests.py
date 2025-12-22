#!/usr/bin/env python3
"""
CryptoCore Test Runner

Запускает все unit-тесты, интеграционные тесты и known-answer тесты.

Использование:
    python tests/run_tests.py           # Запуск всех тестов
    python tests/run_tests.py --unit    # Только unit-тесты
    python tests/run_tests.py --kat     # Только KAT тесты
    python tests/run_tests.py -v        # Подробный вывод
"""

import unittest
import sys
import os
import argparse
import time

# Добавляем корень проекта в путь
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def create_test_suite(test_type: str = 'all') -> unittest.TestSuite:
    """Создаёт набор тестов в зависимости от типа."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    tests_dir = os.path.dirname(os.path.abspath(__file__))

    if test_type in ('all', 'unit'):
        unit_dir = os.path.join(tests_dir, 'unit')
        if os.path.exists(unit_dir):
            discovered = loader.discover(unit_dir, pattern='test_*.py')
            suite.addTests(discovered)
            print(f"[+] Найдено unit-тестов: {discovered.countTestCases()}")

    if test_type in ('all', 'integration'):
        integration_dir = os.path.join(tests_dir, 'integration')
        if os.path.exists(integration_dir):
            discovered = loader.discover(integration_dir, pattern='test_*.py')
            suite.addTests(discovered)
            print(f"[+] Найдено интеграционных тестов: {discovered.countTestCases()}")

    if test_type in ('all', 'kat', 'vectors'):
        vectors_dir = os.path.join(tests_dir, 'vectors')
        if os.path.exists(vectors_dir):
            discovered = loader.discover(vectors_dir, pattern='test_*.py')
            suite.addTests(discovered)
            print(f"[+] Найдено KAT тестов: {discovered.countTestCases()}")

    return suite


def run_tests(verbosity: int = 2, test_type: str = 'all') -> bool:
    """Запускает тесты и возвращает статус успешности."""
    print("=" * 70)
    print("CryptoCore Test Suite")
    print("=" * 70)
    print(f"Тип тестов: {test_type}")
    print(f"Python: {sys.version}")
    print(f"Рабочая директория: {PROJECT_ROOT}")
    print("=" * 70)
    print()

    suite = create_test_suite(test_type)

    if suite.countTestCases() == 0:
        print("\n[!] Тесты не найдены!")
        print("\nУбедитесь, что тестовые файлы существуют в:")
        print("  - tests/unit/")
        print("  - tests/integration/")
        print("  - tests/vectors/")
        return False

    print(f"\nЗапуск {suite.countTestCases()} тестов...\n")
    print("-" * 70)

    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    elapsed_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("ИТОГИ")
    print("=" * 70)
    print(f"Выполнено тестов: {result.testsRun}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Пропущено: {len(result.skipped)}")
    print(f"Время: {elapsed_time:.2f} секунд")
    print("=" * 70)

    if result.wasSuccessful():
        print("\n ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print("\n НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ!")

        if result.failures:
            print("\nПроваленные тесты:")
            for test, _ in result.failures:
               print(f"  - {test}")
                #print("Нет")

        if result.errors:
            print("\nТесты с ошибками:")
            for test, _ in result.errors:
                print(f"  - {test}")

    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(description='CryptoCore Test Runner')
    parser.add_argument('--unit', action='store_true', help='Только unit-тесты')
    parser.add_argument('--integration', action='store_true', help='Только интеграционные тесты')
    parser.add_argument('--kat', '--vectors', action='store_true', help='Только KAT тесты')
    parser.add_argument('-v', '--verbose', action='store_true', help='Подробный вывод')
    parser.add_argument('-q', '--quiet', action='store_true', help='Минимальный вывод')

    args = parser.parse_args()

    # Определяем тип тестов
    if args.unit:
        test_type = 'unit'
    elif args.integration:
        test_type = 'integration'
    elif args.kat:
        test_type = 'kat'
    else:
        test_type = 'all'

    # Определяем уровень подробности
    if args.quiet:
        verbosity = 0
    elif args.verbose:
        verbosity = 2
    else:
        verbosity = 1

    success = run_tests(verbosity=verbosity, test_type=test_type)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()