## Установка

### Установка из исходного кода

```bash
git clone <https://github.com/eeiaya/cryptocoreutils.git>
cd CryptoCoreUtils
pip install -e .
```

### Прямой запуск без установки

```bash
python -m cryptocoreutils --help
```
### Поддерживаемые режимы
* ECB (Electronic Codebook) - базовый режим, требует паддинг

* CBC (Cipher Block Chaining) - блочный режим с цепочкой, требует паддинг

* CFB (Cipher Feedback) - потоковый режим, без паддинга

* OFB (Output Feedback) - потоковый режим, без паддинга

* CTR (Counter) - потоковый режим, без паддинга

* GCM (Galois/Counter Mode) - аутентифицированное шифрование по стандарту NIST SP 800-38D

* ETM (Encrypt-then-MAC) - составной режим CTR + HMAC-SHA256

### Базовые команды шифрования
Вектор инициализации (IV) генерируется автоматически с помощью криптографически стойкого генератора псевдослучайных чисел

```
# ECB режим (без IV)
python main.py crypto -alg aes -m ecb -enc -k 000102030405060708090a0b0c0d0e0f -i tests/document.txt -o tests/document.enc

# CBC режим (IV генерируется автоматически)
python main.py crypto -alg aes -m cbc -enc -k 000102030405060708090a0b0c0d0e0f -i tests/document.txt -o tests/document.enc

# CFB режим (потоковый)
python main.py crypto -alg aes -m cfb -enc -k 000102030405060708090a0b0c0d0e0f -i tests/document.txt -o tests/document.enc

# OFB режим (потоковый)  
python main.py crypto -alg aes -m ofb -enc -k 000102030405060708090a0b0c0d0e0f -i tests/document.txt -o tests/document.enc

# CTR режим (потоковый)
python main.py crypto -alg aes -m ctr -enc -k 000102030405060708090a0b0c0d0e0f -i tests/document.txt -o tests/document.enc

# GCM режим (аутентифицированное шифрование)
python main.py crypto -alg aes -m gcm -enc -k 00112233445566778899aabbccddeeff -i tests/document.txt -o tests/document.enc --aad 616263

# ETM режим (Encrypt-then-MAC)
python main.py crypto -alg aes -m etm -enc -k 00112233445566778899aabbccddeeff -i tests/document.txt -o tests/document.enc --aad 616263
```

### Базовые команды дешифрования

```
# ECB режим (без IV)
python main.py crypto -alg aes -m ecb -dec -k 000102030405060708090a0b0c0d0e0f -i tests/document.enc -o tests/document_decrypted.txt

# CBC режим (IV извлекается из файла)
python main.py crypto -alg aes -m cbc -dec -k 000102030405060708090a0b0c0d0e0f -i tests/document.enc -o tests/document_decrypted.txt

# CBC режим (IV передается явно)
python main.py crypto -alg aes -m cbc -dec -k 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 -i tests/document.enc -o tests/document_decrypted.txt

# Потоковые режимы (CFB, OFB, CTR) - аналогично CBC
python main.py crypto -alg aes -m cfb -dec -k 000102030405060708090a0b0c0d0e0f -i tests/document.enc -o tests/document_decrypted.txt

# GCM режим
python main.py crypto -alg aes -m gcm -dec -k 00112233445566778899aabbccddeeff --aad 616263 -i tests/document.enc -o tests/document_decrypted.txt

# ETM режим
python main.py crypto -alg aes -m etm -dec -k 00112233445566778899aabbccddeeff --aad 616263 -i tests/document.enc -o tests/document_decrypted.txt
```
### GCM Mode
```
# Шифрование с AAD
python main.py crypto -alg aes -m gcm -enc \
    -k 00112233445566778899aabbccddeeff \
    --aad 48656c6c6f576f726c64 \
    -i tests/plain.txt \
    -o tests/cipher.bin

# Шифрование без AAD
python main.py crypto -alg aes -m gcm -enc \
    -k 00112233445566778899aabbccddeeff \
    -i tests/plain.txt \
    -o tests/cipher.bin

# Расшифрование (nonce читается из файла автоматически)
python main.py crypto -alg aes -m gcm -dec \
    -k 00112233445566778899aabbccddeeff \
    --aad 48656c6c6f576f726c64 \
    -i tests/cipher.bin \
    -o tests/decrypted.txt

# Расшифрование с внешним nonce (через --nonce или --iv)
python main.py crypto -alg aes -m gcm -dec\
    -k 00112233445566778899aabbccddeeff\
    --nonce 000102030405060708090a0b \
    --aad 48656c6c6f576f726c64 \
    -i tests/ciphertext_without_nonce.bin \
    -o tests/decrypted.txt
```
### ETM Mode
```
# Шифрование с AAD
python main.py crypto -alg aes -m etm -enc \
    -k 00112233445566778899aabbccddeeff \
    --aad 616263 \
    -i tests/plain.txt \
    -o tests/cipher.bin

# Шифрование без AAD
python main.py crypto -a aes -m etm -enc \
    -k 00112233445566778899aabbccddeeff \
    -i tests/plain.txt \
    -o tests/cipher.bin

# Расшифрование
python main.py crypto -alg aes -m etm -dec \
    -k 00112233445566778899aabbccddeeff \
    --aad 616263 \
    -i tests/cipher.bin \
    -o tests/decrypted.txt
```
## Параметры командной строки

- `--algorithm` (`-alg`): Алгоритм шифрования (только `aes`)
- `--mode` (`-m`): Режим работы (`ecb`, `cbc`, `cfb`, `ofb`, `ctr`)
- `--encrypt` (`-enc`): Режим шифрования
- `--decrypt` (`-dec`): Режим дешифрования
- `--key` (`-k`): Ключ шифрования (32 hex символа)
- `--input` (`-i`): Входной файл
- `--output` (`-o`): Выходной файл
- `--iv`: Вектор инициализации (только для дешифрования)
- `--add`: Ассоциированные данные
- `--nonce` (`-n`): Nonce для GCM (12 байт в hex; алиас для --iv)

## Команды хэширования и hmac 

```
# # Хэширование без указания выходного файла
python main.py dgst -alg sha256 -i document.pdf
# Вывод: e3b0c44298fc1c149afbf4c899cfb92427ae41e4649b934ca495991b7852b855  document.pdf

# Хэширование с указанием выходного файла
python main.py dgst -alg sha3-256 -i backup.tar -o backup.sha3

# HMAC без указания выходного файла
python main.py dgst -alg sha256 --hmac -k 00112233445566778899aabbccddeeff -i tests/message.txt

# HMAC с указанием выходного файла
python main.py dgst -alg sha256 --hmac -k 00112233445566778899aabbccddeeff -i tests/message.txt -o tests/hmac.txt

# HMAC с верификацией
python main.py dgst -alg sha256 --hmac -k 00112233445566778899aabbccddeeff -i tests/message.txt -v tests/hmac.txt
# Вывод: [OK] HMAC verification successful
```

## Параметры хэш-функций
- `-algorithm (-alg)`: Алгоритм хэширования (`sha256`, `sha3-256`)
- `-input (-i)`: Входной файл
- `-output (-o)`: Выходной файл (опционально)

## Параметры HMAC
* `-algorithm` (`-alg`): Алгоритм хэширования (sha256, sha3-256)

* `-hmac`: Флаг для вычисления HMAC

* `-key` (`-k`): Ключ для вычисления HMAC (обязателен для флага --hmac; может быть любой длины от 1 байта)

* `-input` (`-i`): Входной файл

* `-output` (`-o`): Выходной файл (опционально)

* `-verify` (`-v`): Файл с ожидаемым HMAC для проверки

### Команда derive

```bash
# Базовое использование
python main.py derive --password "MyPassword" --salt <HEX> --iterations 100000 --length 32

# С автогенерацией соли
python main.py derive --password "MyPassword"

# Сохранение в файл
python main.py derive --password "MyPassword" --output key.bin

# Key Hierarchy (иерархия ключей)
python main.py derive --master-key <HEX> --context "encryption" --length 32
```
## Основные команды запуска тестов
```
# Запуск ВСЕХ тестов (unit + integration + vectors)
python tests/run_tests.py

# С подробным выводом
python tests/run_tests.py -v
python tests/run_tests.py --verbose

# С минимальным выводом
python tests/run_tests.py -q
python tests/run_tests.py --quiet
```
### Запуск тестов по категориям
```
# Только unit тесты
python tests/run_tests.py --unit

# Только integration тесты
python tests/run_tests.py --integration

# Только тестовые векторы (KAT - Known Answer Tests)
python tests/run_tests.py --vectors
python tests/run_tests.py --kat
```
### Запуск отдельных файлов тестов
### Unit тесты
```
# Тесты AES
python -m unittest tests.unit.test_aes -v
python tests/unit/test_aes.py

# Тесты SHA-256
python -m unittest tests.unit.test_sha256 -v
python tests/unit/test_sha256.py

# Тесты SHA3-256
python -m unittest tests.unit.test_sha3_256 -v
python tests/unit/test_sha3_256.py

# Тесты HMAC
python -m unittest tests.unit.test_hmac -v
python tests/unit/test_hmac.py

# Тесты PBKDF2
python -m unittest tests.unit.test_pbkdf2 -v
python tests/unit/test_pbkdf2.py

# Тесты HKDF
python -m unittest tests.unit.test_hkdf -v
python tests/unit/test_hkdf.py

# Тесты CSPRNG
python -m unittest tests.unit.test_csprng -v
python tests/unit/test_csprng.py

# Тесты режимов шифрования (все в одном файле)
python -m unittest tests.unit.test_modes -v
python tests/unit/test_modes.py
```
### Integration тесты
```
# Тесты CLI crypto команды
python -m unittest tests.integration.test_cli_crypto -v
python tests/integration/test_cli_crypto.py

# Тесты CLI hash команды
python -m unittest tests.integration.test_cli_hash -v
python tests/integration/test_cli_hash.py

# Тесты CLI derive команды
python -m unittest tests.integration.test_cli_derive -v
python tests/integration/test_cli_derive.py

# Тесты CLI hmac команды
python -m unittest tests.integration.test_cli_hmac -v
python tests/integration/test_cli_hmac.py
```
### Тестовые векторы
```
# AES векторы NIST
python -m unittest tests.vectors.test_aes_vectors -v
python tests/vectors/test_aes_vectors.py

# SHA векторы NIST
python -m unittest tests.vectors.test_sha_vectors -v
python tests/vectors/test_sha_vectors.py

# HMAC векторы RFC 4231
python -m unittest tests.vectors.test_hmac_vectors -v
python tests/vectors/test_hmac_vectors.py

# PBKDF2 векторы
python -m unittest tests.vectors.test_pbkdf2_vectors -v
python tests/vectors/test_pbkdf2_vectors.py
```
