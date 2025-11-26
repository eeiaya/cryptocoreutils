"""Парсер командной строки"""
import argparse
import sys
import os
from .modes.ecb import ECBMode
from .modes.cbc import CBCMode
from .modes.cfb import CFBMode
from .modes.ofb import OFBMode
from .modes.ctr import CTRMode
from .file_io import read_file, write_file, validate_file_exists, validate_file_not_empty
from .csprng import generate_random_key


def validate_args(args) -> None:
    """Валидация аргументов командной строки"""
    if not (args.encrypt or args.decrypt):
        raise ValueError("Необходимо указать либо --encrypt, либо --decrypt")

    if args.encrypt and args.decrypt:
        raise ValueError("Нельзя указывать одновременно --encrypt и --decrypt")

    if args.input == args.output:
        raise ValueError("Входной и выходной файлы не могут быть одинаковыми")

    validate_file_exists(args.input)
    validate_file_not_empty(args.input)

    # Валидация ключа
    if args.decrypt and not args.key:
        raise ValueError("Для дешифрования ключ обязателен")

    # Валидация IV
    if args.encrypt and args.iv:
        print("  Предупреждение: IV игнорируется при шифровании")

    if args.decrypt and args.mode != 'ecb' and not args.iv:
        print("  Информация: IV будет прочитан из файла")

    # Проверка слабых ключей
    if args.key:
        _check_weak_key(args.key)


def _check_weak_key(key_hex: str) -> None:
    """Проверяет ключ на слабость"""
    key_hex = key_hex.lstrip('@')

    # Проверка ключа из нулей
    if all(c == '0' for c in key_hex):
        print("  ⚠️  Предупреждение: Используется ключ из нулей - небезопасно!")

    # Проверка последовательных байт
    try:
        key_bytes = bytes.fromhex(key_hex)
        # Проверка на последовательные значения
        is_sequential = all(
            key_bytes[i] + 1 == key_bytes[i + 1]
            for i in range(len(key_bytes) - 1)
        )
        if is_sequential:
            print("  ⚠️  Предупреждение: Используется последовательный ключ - небезопасно!")
    except:
        pass


def main():
    parser = argparse.ArgumentParser(
        description='CryptoCoreUtils - Шифрование файлов AES-128'
    )

    parser.add_argument('-algorithm', '-alg', required=True, choices=['aes'], help='Алгоритм шифрования')
    parser.add_argument('-mode', '-m', required=True, choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'], help='Режим работы')
    parser.add_argument('-encrypt', '-enc', action='store_true', help='Режим шифрования')
    parser.add_argument('-decrypt', '-dec', action='store_true', help='Режим дешифрования')
    parser.add_argument('-key', '-k', help='Ключ шифрования (32 hex символа)')  # ← Сделано НЕОБЯЗАТЕЛЬНЫМ
    parser.add_argument('-input', '-i', required=True, help='Входной файл')
    parser.add_argument('-output', '-o', required=True, help='Выходной файл')
    parser.add_argument('-iv', help='Вектор инициализации (только для дешифрования)')

    args = parser.parse_args()

    try:
        validate_args(args)

        # Генерация ключа если не предоставлен при шифровании
        if args.encrypt and not args.key:
            args.key = generate_random_key()
            print(f"[INFO] Сгенерирован случайный ключ: {args.key}")

        # Создаем соответствующий режим
        mode_classes = {
            'ecb': ECBMode,
            'cbc': CBCMode,
            'cfb': CFBMode,
            'ofb': OFBMode,
            'ctr': CTRMode
        }

        mode_class = mode_classes[args.mode]

        # Для режимов с IV передаем IV, для ECB - нет
        if args.mode == 'ecb':
            crypto_mode = mode_class(args.key)
        else:
            crypto_mode = mode_class(args.key, args.iv if args.decrypt else None)

        input_data = read_file(args.input)

        # Выполняем операцию
        if args.encrypt:
            output_data = crypto_mode.encrypt(input_data)
            print(f"Файл {args.input} зашифрован -> {args.output} (режим {args.mode.upper()})")
        else:
            output_data = crypto_mode.decrypt(input_data)
            print(f"Файл {args.input} расшифрован -> {args.output} (режим {args.mode.upper()})")

        write_file(args.output, output_data)
        print("Операция завершена успешно!")

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)