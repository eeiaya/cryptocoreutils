import argparse
import sys
import os
from .modes.ecb import ECBMode
from .modes.cbc import CBCMode
from .modes.cfb import CFBMode
from .modes.ofb import OFBMode
from .modes.ctr import CTRMode


def main():
    parser = argparse.ArgumentParser(description='CryptoCore - Cryptographic Utilities')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Encryption/Decryption command
    crypto_parser = subparsers.add_parser('crypto', help='Encryption/decryption operations')
    crypto_parser.add_argument('-algorithm', '-alg', choices=['aes'], required=True, help='Cryptographic algorithm')
    crypto_parser.add_argument('-mode', '-m', choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'], required=True,
                               help='Block cipher mode')
    crypto_parser.add_argument('-encrypt', '-enc', action='store_true', help='Encrypt mode')
    crypto_parser.add_argument('-decrypt', '-dec', action='store_true', help='Decrypt mode')
    crypto_parser.add_argument('-key', '-k', required=True, help='Encryption key in hex')
    crypto_parser.add_argument('-input', '-i', required=True, help='Input file path')
    crypto_parser.add_argument('-output', '-o', required=True, help='Output file path')
    crypto_parser.add_argument('-iv', help='Initialization vector in hex')

    # Hash command (NEW for M4)
    hash_parser = subparsers.add_parser('dgst', help='Compute message digests (hash)')
    hash_parser.add_argument('-algorithm', '-alg', choices=['sha256', 'sha3-256'], required=True, help='Hash algorithm')
    hash_parser.add_argument('-input', '-i', required=True, help='Input file path')
    hash_parser.add_argument('-output', '-o', help='Output file path (optional)')

    args = parser.parse_args()

    if args.command == 'crypto':
        handle_crypto_command(args)
    elif args.command == 'dgst':
        handle_hash_command(args)
    else:
        parser.print_help()


def handle_crypto_command(args):
    """Обработка команд шифрования/дешифрования"""
    try:
        if args.algorithm == 'aes':
            if args.mode == 'ecb':
                cipher = ECBMode(args.key)
            elif args.mode == 'cbc':
                cipher = CBCMode(args.key, args.iv)
            elif args.mode == 'cfb':
                cipher = CFBMode(args.key, args.iv)
            elif args.mode == 'ofb':
                cipher = OFBMode(args.key, args.iv)
            elif args.mode == 'ctr':
                cipher = CTRMode(args.key, args.iv)
            else:
                print(f"Ошибка: Неподдерживаемый режим: {args.mode}")
                return

            with open(args.input, 'rb') as f:
                data = f.read()

            if args.encrypt:
                result = cipher.encrypt(data)
                print(f"Файл {args.input} зашифрован -> {args.output} (режим {args.mode.upper()})")
            elif args.decrypt:
                result = cipher.decrypt(data)
                print(f"Файл {args.input} расшифрован -> {args.output} (режим {args.mode.upper()})")
            else:
                print("Ошибка: Укажите --encrypt или --decrypt")
                return

            with open(args.output, 'wb') as f:
                f.write(result)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


def handle_hash_command(args):
    """Обработка команд хеширования (NEW for M4)"""
    try:
        # Динамический импорт чтобы избежать циклических зависимостей

        from cryptocoreutils.hash.sha256 import sha256_file, sha256_data
        from cryptocoreutils.hash.sha3_256 import sha3_256_file, sha3_256_data

        # Проверяем существование файла
        if not os.path.exists(args.input):
            print(f"Ошибка: Файл {args.input} не найден")
            sys.exit(1)

        # Вычисляем хеш в зависимости от алгоритма
        if args.algorithm == 'sha256':
            hash_value = sha256_file(args.input)
        elif args.algorithm == 'sha3-256':
            hash_value = sha3_256_file(args.input)
        else:
            print(f"Ошибка: Неподдерживаемый алгоритм хеширования: {args.algorithm}")
            sys.exit(1)

        # Форматируем вывод
        output_line = f"{hash_value} {args.input}\n"

        # Выводим результат
        if args.output:
            # Записываем в файл
            with open(args.output, 'w') as f:
                f.write(output_line)
            print(f"Хеш записан в файл: {args.output}")
        else:
            # Выводим в stdout
            print(output_line.strip())

    except Exception as e:
        print(f"Ошибка при вычислении хеша: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()