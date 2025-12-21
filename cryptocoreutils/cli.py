import argparse
import sys
import os
from .modes.ecb import ECBMode
from .modes.cbc import CBCMode
from .modes.cfb import CFBMode
from .modes.ofb import OFBMode
from .modes.ctr import CTRMode
from .modes.gcm import GCMMode
from .mac.hmac import hmac_file, verify_hmac, parse_hmac_file
from .modes.etm import ETMMode


def main():
    parser = argparse.ArgumentParser(description='CryptoCore - Cryptographic Utilities')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Crypto command
    crypto_parser = subparsers.add_parser('crypto', help='Encryption/decryption operations')
    crypto_parser.add_argument('-algorithm', '-alg', choices=['aes'], required=True,
                               help='Cryptographic algorithm')
    crypto_parser.add_argument('-mode', '-m',
                               choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr', 'gcm', 'etm'],
                               required=True, help='Block cipher mode')
    crypto_parser.add_argument('-encrypt', '-enc', action='store_true', help='Encrypt mode')
    crypto_parser.add_argument('-decrypt', '-dec', action='store_true', help='Decrypt mode')
    crypto_parser.add_argument('-key', '-k', help='Encryption key in hex')
    crypto_parser.add_argument('-input', '-i', required=True, help='Input file path')
    crypto_parser.add_argument('-output', '-o', required=True, help='Output file path')
    crypto_parser.add_argument('-iv', help='Initialization vector in hex')
    crypto_parser.add_argument('-aad', '--aad', help='Associated Authenticated Data in hex')

    # Hash/digest command
    hash_parser = subparsers.add_parser('dgst', help='Compute message digests (hash) and HMAC')
    hash_parser.add_argument('-algorithm', '-alg', choices=['sha256', 'sha3-256'],
                             required=True, help='Hash algorithm')
    hash_parser.add_argument('-input', '-i', required=True, help='Input file path')
    hash_parser.add_argument('-output', '-o', help='Output file path (optional)')

    hmac_group = hash_parser.add_argument_group('HMAC options')
    hmac_group.add_argument('--hmac', action='store_true',
                            help='Enable HMAC mode (requires --key)')
    hmac_group.add_argument('--key', '-k', help='Key for HMAC in hex format')
    hmac_group.add_argument('--verify', metavar='FILE',
                            help='Verify HMAC against file with expected value')
    hmac_group.add_argument('--cmac', action='store_true',
                            help='Use AES-CMAC instead of HMAC')

    # Derive command (Sprint 7)
    derive_parser = subparsers.add_parser('derive', help='Key derivation operations')
    derive_parser.add_argument('--password', '-p', help='Password string')
    derive_parser.add_argument('--password-file', metavar='FILE',
                               help='Read password from file')
    derive_parser.add_argument('--salt', '-s', help='Salt in hex format')
    derive_parser.add_argument('--iterations', '-n', type=int, default=100000,
                               help='Number of iterations (default: 100000)')
    derive_parser.add_argument('--length', '-l', type=int, default=32,
                               help='Key length in bytes (default: 32)')
    derive_parser.add_argument('--algorithm', '-alg', choices=['pbkdf2'], default='pbkdf2',
                               help='KDF algorithm (default: pbkdf2)')
    derive_parser.add_argument('--output', '-o', help='Output file path (optional)')
    derive_parser.add_argument('--context', '-c', help='Context string for key hierarchy')
    derive_parser.add_argument('--master-key', '-mk', help='Master key in hex for key hierarchy')

    args = parser.parse_args()

    if args.command == 'crypto':
        handle_crypto_command(args)
    elif args.command == 'dgst':
        handle_hash_command(args)
    elif args.command == 'derive':
        handle_derive_command(args)
    else:
        parser.print_help()


def handle_crypto_command(args):
    """Обработка команды шифрования/дешифрования."""
    try:
        if args.algorithm != 'aes':
            print(f"Ошибка: Неподдерживаемый алгоритм: {args.algorithm}")
            sys.exit(1)

        # Проверка входного файла
        if not os.path.exists(args.input):
            print(f"Ошибка: Файл {args.input} не найден")
            sys.exit(1)

        # Обработка AAD для GCM/ETM
        aad = b""
        if args.aad:
            try:
                aad = bytes.fromhex(args.aad)
            except ValueError:
                print("Ошибка: AAD должен быть в шестнадцатеричном формате")
                sys.exit(1)

        # Обработка ключа - режимы ожидают HEX СТРОКУ
        if not args.key:
            from .csprng import generate_random_bytes
            key_bytes = generate_random_bytes(16)
            key_hex = key_bytes.hex()
            print(f"[INFO] Сгенерирован случайный ключ: {key_hex}")
        else:
            # Проверяем что ключ валидный hex
            try:
                bytes.fromhex(args.key)  # Проверка валидности
                key_hex = args.key
            except ValueError:
                print("Ошибка: Ключ должен быть в шестнадцатеричном формате")
                sys.exit(1)

        # Обработка IV - режимы ожидают HEX СТРОКУ или None
        iv_hex = None
        if args.iv:
            try:
                bytes.fromhex(args.iv)  # Проверка валидности
                iv_hex = args.iv
            except ValueError:
                print("Ошибка: IV должен быть в шестнадцатеричном формате")
                sys.exit(1)

        # Создание cipher объекта - передаём HEX СТРОКИ
        if args.mode == 'ecb':
            cipher = ECBMode(key_hex)
        elif args.mode == 'cbc':
            cipher = CBCMode(key_hex, iv_hex)
        elif args.mode == 'cfb':
            cipher = CFBMode(key_hex, iv_hex)
        elif args.mode == 'ofb':
            cipher = OFBMode(key_hex, iv_hex)
        elif args.mode == 'ctr':
            cipher = CTRMode(key_hex, iv_hex)
        elif args.mode == 'gcm':
            cipher = GCMMode(key_hex, iv_hex)
        elif args.mode == 'etm':
            cipher = ETMMode(key_hex, iv_hex)
        else:
            print(f"Ошибка: Неподдерживаемый режим: {args.mode}")
            sys.exit(1)

        # Читаем входной файл
        with open(args.input, 'rb') as f:
            data = f.read()

        # Выполняем шифрование или дешифрование
        if args.encrypt:
            if args.mode == 'gcm':
                result = cipher.encrypt(data, aad)
            elif args.mode == 'etm':
                result = cipher.encrypt(data, aad)
            else:
                result = cipher.encrypt(data)
            print(f"Файл {args.input} зашифрован -> {args.output} (режим {args.mode.upper()})")

        elif args.decrypt:
            try:
                if args.mode == 'gcm':
                    result = cipher.decrypt(data, aad)
                elif args.mode == 'etm':
                    result = cipher.decrypt(data, aad)
                else:
                    result = cipher.decrypt(data)
                print(f"Файл {args.input} расшифрован -> {args.output} (режим {args.mode.upper()})")

            except Exception as e:
                error_msg = str(e)
                if "Authentication" in error_msg or "аутентификации" in error_msg:
                    print(f"[ERROR] {e}")
                    print("Файл не создан из-за провала аутентификации")
                    if os.path.exists(args.output):
                        os.remove(args.output)
                    sys.exit(1)
                else:
                    raise

        else:
            print("Ошибка: Укажите -encrypt или -decrypt")
            sys.exit(1)

        # Записываем результат
        with open(args.output, 'wb') as f:
            f.write(result)

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка формата: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


def handle_hash_command(args):
    """Обработка команды хеширования и HMAC."""
    try:
        if not os.path.exists(args.input):
            print(f"Ошибка: Файл {args.input} не найден")
            sys.exit(1)

        if args.hmac:
            if not args.key:
                print("Ошибка: В режиме HMAC требуется указать --key")
                sys.exit(1)

            try:
                key_bytes = bytes.fromhex(args.key)
            except ValueError:
                print("Ошибка: Ключ должен быть в шестнадцатеричном формате")
                sys.exit(1)

            computed_hmac = hmac_file(key_bytes, args.input, args.algorithm)
            output_line = f"{computed_hmac} {args.input}\n"

            if args.verify:
                try:
                    expected_hmac, _ = parse_hmac_file(args.verify)

                    if verify_hmac(expected_hmac, computed_hmac):
                        print("[OK] HMAC verification successful")
                        sys.exit(0)
                    else:
                        print("[ERROR] HMAC verification failed")
                        sys.exit(1)

                except FileNotFoundError:
                    print(f"Ошибка: Файл не найден: {args.verify}")
                    sys.exit(1)
                except ValueError as e:
                    print(f"Ошибка: {e}")
                    sys.exit(1)

            else:
                if args.output:
                    with open(args.output, 'w') as f:
                        f.write(output_line)
                    print(f"HMAC записан в файл: {args.output}")
                else:
                    print(output_line.strip())

        else:
            from .hash.sha256 import sha256_file
            from .hash.sha3_256 import sha3_256_file

            if args.algorithm == 'sha256':
                hash_value = sha256_file(args.input)
            elif args.algorithm == 'sha3-256':
                hash_value = sha3_256_file(args.input)
            else:
                print(f"Ошибка: Неподдерживаемый алгоритм: {args.algorithm}")
                sys.exit(1)

            output_line = f"{hash_value} {args.input}\n"

            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output_line)
                print(f"Хеш записан в файл: {args.output}")
            else:
                print(output_line.strip())

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


def handle_derive_command(args):
    """Обработка команды деривации ключей."""
    try:
        from .kdf.pbkdf2 import pbkdf2_hmac_sha256, generate_salt
        from .kdf.hkdf import derive_key

        # Проверка длины
        if args.length < 1:
            print("Ошибка: Длина ключа должна быть положительной")
            sys.exit(1)

        # ===== KEY HIERARCHY MODE =====
        if args.master_key:
            if not args.context:
                print("Ошибка: Для key hierarchy требуется указать --context")
                sys.exit(1)

            try:
                master_key_bytes = bytes.fromhex(args.master_key)
            except ValueError:
                print("Ошибка: Мастер-ключ должен быть в шестнадцатеричном формате")
                sys.exit(1)

            derived_key = derive_key(master_key_bytes, args.context, args.length)

            # Вывод для key hierarchy
            if args.output:
                with open(args.output, 'wb') as f:
                    f.write(derived_key)
                print(f"[INFO] Ключ записан в: {args.output}", file=sys.stderr)
                print(f"[INFO] Контекст: {args.context}", file=sys.stderr)
                print(f"[INFO] Длина ключа: {args.length} байт", file=sys.stderr)
            else:
                # Для key hierarchy выводим только ключ (нет соли)
                print(derived_key.hex())

            # Очистка
            derived_key = None
            return

        # ===== PBKDF2 MODE =====
        # Получение пароля (обязательно для PBKDF2)
        password = None
        if args.password_file:
            try:
                with open(args.password_file, 'r', encoding='utf-8') as f:
                    password = f.read().strip()
            except Exception as e:
                print(f"Ошибка чтения файла пароля: {e}")
                sys.exit(1)
        elif args.password:
            password = args.password
        else:
            print("Ошибка: Требуется указать --password, --password-file или --master-key")
            sys.exit(1)

        # Проверка итераций
        if args.iterations < 1:
            print("Ошибка: Количество итераций должно быть положительным")
            sys.exit(1)

        # Получение или генерация соли
        salt = None
        salt_generated = False
        if args.salt:
            try:
                salt = bytes.fromhex(args.salt)
            except ValueError:
                print("Ошибка: Соль должна быть в шестнадцатеричном формате")
                sys.exit(1)
        else:
            salt = generate_salt(16)
            salt_generated = True
            print(f"[INFO] Сгенерирована соль: {salt.hex()}", file=sys.stderr)

        # Выполнение PBKDF2
        derived_key = pbkdf2_hmac_sha256(
            password=password,
            salt=salt,
            iterations=args.iterations,
            dklen=args.length
        )

        # Вывод результата
        if args.output:
            # Записываем ключ в файл как сырые байты
            with open(args.output, 'wb') as f:
                f.write(derived_key)
            print(f"[INFO] Ключ записан в: {args.output}", file=sys.stderr)
            print(f"[INFO] Соль: {salt.hex()}", file=sys.stderr)
            print(f"[INFO] Итерации: {args.iterations}", file=sys.stderr)
            print(f"[INFO] Длина: {args.length} байт", file=sys.stderr)
        else:
            # Вывод в stdout: KEY_HEX SALT_HEX (согласно CLI-3)
            print(f"{derived_key.hex()} {salt.hex()}")

        # Очистка пароля из памяти
        password = None
        derived_key = None

    except ImportError as e:
        print(f"Ошибка импорта KDF модулей: {e}")
        print("Убедитесь что реализованы модули kdf/pbkdf2.py и kdf/hkdf.py")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при выполнении derive: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()