```markdown
# CryptoCore

Утилита командной строки для блочного шифрования файлов с использованием AES-128 в различных режимах работы.

## Возможности

- Поддержка алгоритма AES-128
- Режимы работы: ECB, CBC, CFB, OFB, CTR
- Шифрование и дешифрование файлов
- Совместимость с OpenSSL
- Безопасная генерация IV

## Установка

### Установка из исходного кода

```
git clone <https://github.com/eeiaya/cryptocoreutils.git>
cd CryptoCoreUtils
pip install -e .
```

### Прямой запуск без установки

```
python -m cryptocoreutils --help
```

## Использование

### Базовые команды

Шифрование файла в режиме CBC:

```
cryptocoreutils --algorithm aes --mode cbc --encrypt \
       --key 000102030405060708090a0b0c0d0e0f \
       --input document.txt \
       --output document.enc
```

Дешифрование файла в режиме CBC:

```
cryptocoreutils --algorithm aes --mode cbc --decrypt \
       --key 000102030405060708090a0b0c0d0e0f \
       --iv AABBCCDDEEFF00112233445566778899 \
       --input document.enc \
       --output document_decrypted.txt
```

### Параметры командной строки

- `--algorithm` (`-alg`): Алгоритм шифрования (только `aes`)
- `--mode` (`-m`): Режим работы (`ecb`, `cbc`, `cfb`, `ofb`, `ctr`)
- `--encrypt` (`-enc`): Режим шифрования
- `--decrypt` (`-dec`): Режим дешифрования
- `--key` (`-k`): Ключ шифрования (32 hex символа)
- `--input` (`-i`): Входной файл
- `--output` (`-o`): Выходной файл
- `--iv`: Вектор инициализации (только для дешифрования)

## Особенности режимов работы

### ECB (Electronic Codebook)
- Не требует IV
- Использует padding (PKCS#7)
- Каждый блок шифруется независимо

### CBC (Cipher Block Chaining)
- Требует IV при дешифровании
- Использует padding (PKCS#7)
- Каждый блок зависит от предыдущего

### CFB (Cipher Feedback)
- Требует IV при дешифровании
- Не использует padding
- Потоковый режим

### OFB (Output Feedback)
- Требует IV при дешифровании
- Не использует padding
- Потоковый режим

### CTR (Counter)
- Требует IV при дешифровании
- Не использует padding
- Потоковый режим

## Совместимость с OpenSSL

### Шифрование утилитой, дешифрование OpenSSL

```
# Шифрование
cryptocoreutils --algorithm aes --mode cbc --encrypt \
       --key 000102030405060708090a0b0c0d0e0f \
       --input plain.txt --output cipher.bin

# Извлечение IV и шифртекста
dd if=cipher.bin of=iv.bin bs=16 count=1
dd if=cipher.bin of=ciphertext_only.bin bs=16 skip=1

# Дешифрование OpenSSL
openssl enc -aes-128-cbc -d \
       -K 000102030405060708090A0B0C0D0E0F \
       -iv $(xxd -p iv.bin | tr -d '\n') \
       -in ciphertext_only.bin -out decrypted.txt
```

### Шифрование OpenSSL, дешифрование утилитой

```
# Шифрование OpenSSL
openssl enc -aes-128-cbc \
       -K 000102030405060708090A0B0C0D0E0F \
       -iv AABBCCDDEEFF00112233445566778899 \
       -in plain.txt -out openssl_cipher.bin

# Дешифрование утилитой
cryptocoreutils --algorithm aes --mode cbc --decrypt \
       --key 000102030405060708090a0b0c0d0e0f \
       --iv AABBCCDDEEFF00112233445566778899 \
       --input openssl_cipher.bin --output decrypted.txt
```

## Требования

- Python 3.8 или выше
- pycryptodome 3.23.0 или выше

## Формат ключа

Ключ должен быть ровно 16 байт (32 hex символа):

```
Правильно: 000102030405060708090a0b0c0d0e0f
Неправильно: 001122 (3 байта)
```

## Проверка целостности

Для проверки корректности шифрования/дешифрования:

```
# Linux/Mac
cmp original.txt decrypted.txt

# Windows
fc /b original.txt decrypted.txt
```

## Примечания

- Проект разработан в образовательных целях
- Режим ECB не рекомендуется для защиты реальных данных
- Всегда используйте надежные случайные ключи
- Сохраняйте ключи в безопасном месте

## Структура проекта

```
CryptoCoreUtils/
├── cryptocoreutils/
│   ├── modes/
│   │   ├── ecb.py
│   │   ├── cbc.py
│   │   ├── cfb.py
│   │   ├── ofb.py
│   │   └── ctr.py
│   ├── crypto/
│   │   ├── aes.py
│   │   └── padding.py
│   ├── file_io.py
│   ├── cli.py
│   └── main.py
├── tests/
│   ├── test_ecb.py
│   └── test_openssl.py
├── README.md
└── requirements.txt
```
```

