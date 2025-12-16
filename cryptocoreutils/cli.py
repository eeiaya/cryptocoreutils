import argparse
import sys
import os
from .modes.ecb import ECBMode
from .modes.cbc import CBCMode
from .modes.cfb import CFBMode
from .modes.ofb import OFBMode
from .modes.ctr import CTRMode
from .mac.hmac import hmac_file, verify_hmac, parse_hmac_file


def main():
    parser = argparse.ArgumentParser(description='CryptoCore - Cryptographic Utilities')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

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
                            help='Use AES-CMAC instead of HMAC (bonus)')

    args = parser.parse_args()

    if args.command == 'crypto':
        handle_crypto_command(args)
    elif args.command == 'dgst':
        handle_hash_command(args)
    else:
        parser.print_help()


def handle_crypto_command(args):
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


if __name__ == '__main__':
    main()