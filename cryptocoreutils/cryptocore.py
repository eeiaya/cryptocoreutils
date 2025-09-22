
import sys
import argparse
from Crypto.Cipher import AES


def main():
    try:

        parser = argparse.ArgumentParser()
        parser.add_argument('-algorithm', required=True)
        parser.add_argument('-mode', required=True)
        parser.add_argument('-encrypt', action='store_true')
        parser.add_argument('-decrypt', action='store_true')
        parser.add_argument('-key', required=True)
        parser.add_argument('-input', required=True)
        parser.add_argument('-output', required=True)

        args = parser.parse_args()


        if not (args.encrypt or args.decrypt):
            print("Ошибка: выбери либо -encrypt, либо -decrypt")
            sys.exit(1)

        if args.encrypt and args.decrypt:
            print("Ошибка: нельзя выбирать и -encrypt и -decrypt одновременно")
            sys.exit(1)


        key_hex = args.key


        if len(key_hex) != 32:
            print(f"Ошибка: ключ должен быть 16 байт (32 hex символа), а у тебя {len(key_hex)}")
            sys.exit(1)

        key = bytes.fromhex(key_hex)


        try:
            with open(args.input, 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Ошибка: файл {args.input} не найден!")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            sys.exit(1)


        if args.encrypt:

            padding_len = 16 - (len(data) % 16)
            if padding_len == 0:
                padding_len = 16
            data += bytes([padding_len] * padding_len)


            cipher = AES.new(key, AES.MODE_ECB)
            result = cipher.encrypt(data)
            print(f"Файл зашифрован! Размер: {len(result)} байт")

        else:
            cipher = AES.new(key, AES.MODE_ECB)
            result = cipher.decrypt(data)


            padding_len = result[-1]
            result = result[:-padding_len]
            print(f"Файл расшифрован! Размер: {len(result)} байт")


        try:
            with open(args.output, 'wb') as f:
                f.write(result)
            print(f"Результат сохранен в: {args.output}")

        except Exception as e:
            print(f"Ошибка при записи файла: {e}")
            sys.exit(1)

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()