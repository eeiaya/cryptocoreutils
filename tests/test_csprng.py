"""Тесты для CSPRNG модуля"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cryptocoreutils.csprng import generate_random_key


def test_key_uniqueness():
    """Тест на уникальность сгенерированных ключей"""
    key_set = set()
    num_keys = 1000

    print("Тестирование уникальности ключей...")

    for i in range(num_keys):
        key = generate_random_key()

        # Проверка уникальности
        if key in key_set:
            raise AssertionError(f"Найден дубликат ключа: {key}")
        key_set.add(key)

    print(f"Успешно сгенерировано {len(key_set)} уникальных ключей")


if __name__ == "__main__":
    test_key_uniqueness()