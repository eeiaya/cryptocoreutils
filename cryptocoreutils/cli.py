
"""Парсер командной строки"""
import argparse
import sys
from .modes.ecb import ECBMode
from .file_io import read_file, write_file


def main():
    parser = argparse.ArgumentParser(
        description='CryptoCoreUtils - Шифрование файлов AES-128 ECB'
    )

    parser.add_argument('-algorithm', required=True, choices=['aes'], help='Алгоритм шифрования')
    parser.add_argument('-mode', required=True, choices=['ecb'], help='Режим работы')
    parser.add_argument('-encrypt', action='store_true', help='Режим шифрования')
    parser.add_argument('-decrypt', action='store_true', help='Режим дешифрования')
    parser.add_argument('-key', required=True, help='Ключ шифрования (32 hex символа)')
    parser.add_argument('-input', required=True, help='Входной файл')
    parser.add_argument('-output', required=True, help='Выходной файл')

    args = parser.parse_args()

    try:
        # Проверяем что выбран только один режим
        if not (args.encrypt or args.decrypt):
            print("Ошибка: необходимо указать либо -encrypt, либо -decrypt", file=sys.stderr)
            sys.exit(1)

        if args.encrypt and args.decrypt:
            print("Ошибка: нельзя указывать одновременно -encrypt и -decrypt", file=sys.stderr)
            sys.exit(1)

        # Создаем режим ECB
        ecb = ECBMode(args.key)

        # Читаем входной файл
        input_data = read_file(args.input)

        # Выполняем операцию
        if args.encrypt:
            output_data = ecb.encrypt(input_data)
            print(f"Файл {args.input} зашифрован -> {args.output}")
        else:
            output_data = ecb.decrypt(input_data)
            print(f"Файл {args.input} расшифрован -> {args.output}")

        # Записываем результат
        write_file(args.output, output_data)
        print("Операция завершена успешно!")

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)