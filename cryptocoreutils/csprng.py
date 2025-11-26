"""Криптографически стойкий генератор псевдослучайных чисел"""
import os


def generate_random_bytes(num_bytes: int) -> bytes:
    """
    Генерирует криптографически стойкую случайную байтовую строку.

    Args:
        num_bytes: Количество байт для генерации

    Returns:
        bytes: Случайные байты

    Raises:
        OSError: Если системный генератор недоступен
    """
    if num_bytes <= 0:
        raise ValueError("Количество байт должно быть положительным")

    try:
        return os.urandom(num_bytes)
    except Exception as e:
        raise OSError(f"Ошибка генерации случайных байт: {e}")


def generate_random_key() -> str:
    """Генерирует случайный 128-битный ключ AES"""
    key_bytes = generate_random_bytes(16)
    return key_bytes.hex()


def generate_random_iv() -> bytes:
    """Генерирует случайный IV"""
    return generate_random_bytes(16)



