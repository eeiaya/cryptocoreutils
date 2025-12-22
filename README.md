
# CryptoCore

Утилита командной строки для блочного шифрования файлов с использованием AES-128 в различных режимах работы.

## Возможности

* Поддержка алгоритма AES-128
* Режимы работы: ECB, CBC, CFB, OFB, CTR, GCM, ETM
* Шифрование и дешифрование файлов
* Аутентифицированное шифрование (GCM, ETM)
* Поддержка ассоциированных данных (AAD)
* HMAC для проверки целостности данных
* SHA-256 и SHA3-256 хэш-функции
* Совместимость с OpenSSL
* Безопасная генерация ключей и IV

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

## Использование
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
crypto -alg aes -m ecb -enc -k 000102030405060708090a0b0c0d0e0f -i tests/document.txt -o tests/document.enc

# CBC режим (IV генерируется автоматически)
crypto -alg aes -m cbc -enc -k 000102030405060708090a0b0c0d0e0f -i tests/document.txt -o tests/document.enc

# CFB режим (потоковый)
crypto -alg aes -m cfb -enc -k 000102030405060708090a0b0c0d0e0f -i tests/document.txt -o tests/document.enc

# OFB режим (потоковый)  
crypto -alg aes -m ofb -enc -k 000102030405060708090a0b0c0d0e0f -i tests/document.txt -o tests/document.enc

# CTR режим (потоковый)
crypto -alg aes -m ctr -enc -k 000102030405060708090a0b0c0d0e0f -i tests/document.txt -o tests/document.enc

# GCM режим (аутентифицированное шифрование)
crypto -alg aes -m gcm -enc -k 00112233445566778899aabbccddeeff -i tests/document.txt -o tests/document.enc --aad 616263

# ETM режим (Encrypt-then-MAC)
crypto -alg aes -m etm -enc -k 00112233445566778899aabbccddeeff -i tests/document.txt -o tests/document.enc --aad 616263
```

### Базовые команды дешифрования

```
# ECB режим (без IV)
crypto -alg aes -m ecb -dec -k 000102030405060708090a0b0c0d0e0f -i tests/document.enc -o tests/document_decrypted.txt

# CBC режим (IV извлекается из файла)
crypto -alg aes -m cbc -dec -k 000102030405060708090a0b0c0d0e0f -i tests/document.enc -o tests/document_decrypted.txt

# CBC режим (IV передается явно)
crypto -alg aes -m cbc -dec -k 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 -i tests/document.enc -o tests/document_decrypted.txt

# Потоковые режимы (CFB, OFB, CTR) - аналогично CBC
crypto -alg aes -m cfb -dec -k 000102030405060708090a0b0c0d0e0f -i tests/document.enc -o tests/document_decrypted.txt

# GCM режим
crypto -alg aes -m gcm -dec -k 00112233445566778899aabbccddeeff --aad 616263 -i tests/document.enc -o tests/document_decrypted.txt

# ETM режим
crypto -alg aes -m etm -dec -k 00112233445566778899aabbccddeeff --aad 616263 -i tests/document.enc -o tests/document_decrypted.txt
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

## Автоматическая генерация ключей
### При шифровании без указания ключа утилита автоматически генерирует криптографически стойкий ключ:
```
# Выполняем шифрование без указания ключа в параметре
crypto -alg aes -m ctr -enc -i tests/plain.txt -o tests/cipher.bin
# Вывод в консоли: 
[INFO] Сгенерирован случайный ключ: 5fae09f459b9b496cf00c3c5f1f0b613
[INFO] Файл успешно зашифрован в режиме CFB                            
[INFO] Входной файл: tests\plain.txt -> Выходной файл: tests\cipher.bin

# Или с указанием ключа в параметре
crypto -alg aes -m ctr -enc -k 000102030405060708090a0b0c0d0e0f -i tests/plain.txt -o tests/cipher.bin
# Вывод в консоли: 
[INFO] Файл успешно зашифрован в режиме CTR
[INFO] Входной файл: tests\plain.txt -> Выходной файл: tests\cipher.bin

```
### При дешифровании параметр -key (-k) является обязательным.

## Команды хэширования и hmac 

```
# # Хэширование без указания выходного файла
crypto dgst -alg sha256 -i document.pdf
# Вывод: e3b0c44298fc1c149afbf4c899cfb92427ae41e4649b934ca495991b7852b855  document.pdf

# Хэширование с указанием выходного файла
crypto dgst -alg sha3-256 -i backup.tar -o backup.sha3

# HMAC без указания выходного файла
crypto dgst -alg sha256 --hmac -k 00112233445566778899aabbccddeeff -i tests/message.txt

# HMAC с указанием выходного файла
crypto dgst -alg sha256 --hmac -k 00112233445566778899aabbccddeeff -i tests/message.txt -o tests/hmac.txt

# HMAC с верификацией
crypto dgst -alg sha256 --hmac -k 00112233445566778899aabbccddeeff -i tests/message.txt -v tests/hmac.txt
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

## Формат вывода хэша и hmac
```
e3b0c44298fc1c149afbf4c899cfb92427ae41e4649b934ca495991b7852b855  document.pdf
```
## Аутентифицированное шифрование (GCM)
### Описание
GCM — стандартизированный режим аутентифицированного шифрования (NIST SP 800-38D), широко используемый в TLS, IPsec, SSH.

Характеристики:

* Nonce: 12 байт (96 бит)

* Tag: 16 байт (128 бит)

* Использует умножение в поле Галуа GF(2¹²⁸)

* Формат вывода: Nonce (12) || Ciphertext || Tag (16)

### Пример использования
```
# Шифрование с AAD
crypto -alg aes -m gcm -enc \
    -k 00112233445566778899aabbccddeeff \
    --aad 48656c6c6f576f726c64 \
    -i tests/plain.txt \
    -o tests/cipher.bin

# Шифрование без AAD
crypto -alg aes -m gcm -enc \
    -k 00112233445566778899aabbccddeeff \
    -i tests/plain.txt \
    -o tests/cipher.bin

# Расшифрование (nonce читается из файла автоматически)
crypto -alg aes -m gcm -dec \
    -k 00112233445566778899aabbccddeeff \
    --aad 48656c6c6f576f726c64 \
    -i tests/cipher.bin \
    -o tests/decrypted.txt

# Расшифрование с внешним nonce (через --nonce или --iv)
crypto -alg aes -m gcm -dec \
    -k 00112233445566778899aabbccddeeff \
    --nonce 000102030405060708090a0b \
    --aad 48656c6c6f576f726c64 \
    -i tests/ciphertext_without_nonce.bin \
    -o tests/decrypted.txt
```

## Аутентифицированное шифрование (ETM)
### Описание
ETM — составной режим аутентифицированного шифрования, комбинирующий CTR mode для шифрования и HMAC-SHA256 для аутентификации.

Характеристики:

* IV: 16 байт (128 бит)

* Tag: 32 байта (256 бит, HMAC-SHA256)

* Использует раздельные ключи для шифрования и MAC (key separation)

* Формат вывода: IV (16) || Ciphertext || HMAC Tag (32)

### Пример использования
```
# Шифрование с AAD
crypto -alg aes -m etm -enc \
    -k 00112233445566778899aabbccddeeff \
    --aad 616263 \
    -i tests/plain.txt \
    -o tests/cipher.bin

# Шифрование без AAD
crypto -a aes -m etm -enc \
    -k 00112233445566778899aabbccddeeff \
    -i tests/plain.txt \
    -o tests/cipher.bin

# Расшифрование
crypto -alg aes -m etm -dec \
    -k 00112233445566778899aabbccddeeff \
    --aad 616263 \
    -i tests/cipher.bin \
    -o tests/decrypted.txt
```

## AAD (Associated Authenticated Data)
### Описание

AAD — это дополнительные данные, которые:

* НЕ шифруются (остаются в открытом виде)

* Аутентифицируются (защищены от подмены)

* Используются для метаданных: заголовков, ID, timestamp и т.д.

## Формат AAD
AAD передаётся как hex-строка, например, 48656c6c6f (Hello в ASCII)

## Размер ключа, IV и Nonce

| Параметр           | Размер            | Режимы                       |
|--------------------|-------------------|------------------------------|
| Ключ               | 16 байт (32 hex)  | Все режимы                   |
| IV                 | 16 байт (32 hex)  | ECB, CBC, CFB, OFB, CTR, ETM |
| Nonce              | 12 байт (24 hex)  | GCM                          |

```
Правильный ключ: 000102030405060708090a0b0c0d0e0f (32 символа)
Неправильно: mykey123 (8 байт)

Правильный IV: AABBCCDDEEFF00112233445566778899 (32 символа)
Неправильно: ASFSAFSA909DAS9DA99129129DNNBN

Правильный Nonce: 000102030405060708090a0b (24 символа)
```
## Безопасность AEAD
### Свойства безопасности
| Свойство               | Описание         |
|------------------------|------------------|
| Защита от подмены      | Изменение любого бита ciphertext или tag приводит к ошибке аутентификации | 
| Защита AAD             | Изменение AAD также приводит к ошибке, хотя AAD не шифруется | 
| Катастрофический отказ | При ошибке аутентификации НЕ выводятся никакие данные |
| Уникальный nonce       | Каждое шифрование использует уникальный случайный nonce |

## Катастрофический отказ
При использовании GCM и ETM режимов:

* Неправильный AAD → аутентификация провалена → выходной файл не создается

* Измененный шифртекст → аутентификация провалена → выходной файл не создается

* Измененный тег аутентификации → аутентификация провалена → выходной файл не создается

## Рекомендации по использованию GCM/ETM
* Всегда используйте уникальный nonce/IV для каждого шифрования

* AAD должен быть одинаковым при шифровании и дешифровании

* Проверяйте ошибки аутентификации в своем коде

* Не используйте GCM с повторяющимися nonce

* Сохраняйте ключи в безопасном месте


## Генерация ключей (KDF)

Key Derivation Functions (KDF) — функции для получения криптографических ключей из паролей или других ключей. CryptoCore поддерживает:

- PBKDF2-HMAC-SHA256 — получение ключей из паролей
- Key Hierarchy — получение множества ключей из мастер-ключа

### Концепции

### Key Stretching (растяжение ключа)

Процесс преобразования пароля (с низкой энтропией) в криптографический ключ фиксированной длины. PBKDF2 использует многократное применение HMAC для увеличения вычислительной сложности атак перебором.

### Salting (соль)

Случайное значение, добавляемое к паролю перед хешированием. Предотвращает:
- Атаки с использованием радужных таблиц
- Определение одинаковых паролей по совпадению хешей

**Требования к соли:**
- Минимум 16 байт (128 бит)
- Криптографически случайная
- Уникальная для каждого пароля

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

## Совместимость с OpenSSL

### Шифрование OpenSSL, дешифрование утилитой

```bash
# Шифрование OpenSSL
openssl enc -aes-128-cbc \
       -K 000102030405060708090A0B0C0D0E0F \
       -iv AABBCCDDEEFF00112233445566778899 \
       -in plain.txt -out openssl_cipher.bin

# Дешифрование утилитой
crypto -algorithm aes --mode cbc --decrypt \
       -key 000102030405060708090a0b0c0d0e0f \
       -iv AABBCCDDEEFF00112233445566778899 \
       -input openssl_cipher.bin --output decrypted.txt
```

## Команды OpenSSL для разных режимов

* ECB: `openssl enc -aes-128-ecb`

* CBC: `openssl enc -aes-128-cbc`

* CFB: `openssl enc -aes-128-cfb`

* OFB: `openssl enc -aes-128-ofb`

* CTR: `openssl enc -aes-128-ctr`


## Тестирование CSPRNG с помощью NIST Statistical Test Suite
### Пошаговая инструкция запуска тестов:
1. **Переходим в корневую папку проекта:**
    ```bash
   cd /mnt/c/Users/user/PycharmProjects/CryptoCoreUtils
   ```
2. **Создаем тестовые данные (10мб):**
    ```bash
   python3 -c "
    from cryptocoreutils.csprng import generate_random_bytes
    data = generate_random_bytes(10000000)
    open('random_test_data.bin', 'wb').write(data)
    print('Сгенерирован файл random_test_data.bin размером 10 МБ')
    "
    ```
3. **Переходим в папку NIST STS:**
    ```bash
    cd sts-2.1.2/sts-2.1.2/
    ```
4. **Собираем тесты:**

    ```bash
    make
    ```
5. **Запускаем тесты:**
    ```bash
    ./assess 10000000
    ```
6. **Вводим параметры тестирования:**

* #### Enter Choice: 0 (Input File)

* #### User Prescribed Input File: ../../random_test_data.bin

* #### Enter Choice: 1 (All statistical tests)

* #### Select Test (0 to continue): 0 (Default parameters)

* #### How many bitstreams? 10 (Для точной оценки)

* #### Select input mode: 1 (Binary mode)

7. **Ждем выполнения тестов (5-7 минут)**

8. **Просматриваем результаты:**
    ```bash
    # (Linux/Mac/WSL)
    cat experiments/AlgorithmTesting/finalAnalysisReport.txt
    ```
9. **Ожимаемый вывод:**
    ```
    Все 15 статистических тестов NIST должны быть пройдены с показателем 10/10 и p-value ≥ 0.01
    
    ------------------------------------------------------------------------------
    RESULTS FOR THE UNIFORMITY OF P-VALUES AND THE PROPORTION OF PASSING SEQUENCES
    ------------------------------------------------------------------------------
    generator is <../../random_test_data.bin>
    ------------------------------------------------------------------------------
     C1  C2  C3  C4  C5  C6  C7  C8  C9 C10  P-VALUE  PROPORTION  STATISTICAL TEST
    ------------------------------------------------------------------------------
      0   1   1   3   3   0   1   1   0   0  0.213309     10/10      Frequency
      1   0   2   2   0   1   0   0   4   0  0.066882     10/10      BlockFrequency
      0   0   3   1   1   3   1   0   1   0  0.213309     10/10      CumulativeSums
      0   2   0   0   3   3   1   0   1   0  0.122325     10/10      CumulativeSums
      0   0   1   3   1   1   0   2   0   2  0.350485     10/10      Runs
      0   0   2   2   0   2   0   4   0   0  0.035174     10/10      LongestRun
      0   0   2   1   1   1   4   0   0   1  0.122325     10/10      Rank
      1   1   0   3   0   1   1   0   3   0  0.213309     10/10      FFT
      0   0   0   0   1   1   0   1   2   5  0.008879     10/10      NonOverlappingTemplate
      0   0   2   1   0   0   1   3   0   3  0.122325     10/10      NonOverlappingTemplate
      0   1   2   0   2   1   1   0   0   3  0.350485     10/10      NonOverlappingTemplate
      .....
    ```
   


## Тестирование хэш-функций
### Тестирование SHA-256 на тестовых векторах

```bash
   ## Хэшируем пустой файл
   crypto dgst -alg sha256 -i tests/empty.txt
   # Ожидаемый вывод: e3b0c44298fc1c149afbf4c899cfb92427ae41e4649b934ca495991b7852b855 tests/empty.txt
   
   ## Хэшируем файл со строкой "abc"
   crypto dgst -alg sha256 -i tests/test_one.txt
   # Ожидаемый вывод: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  tests/test_one.txt
   
```
### Тестирование SHA3-256 на тестовых векторах

```bash
   ## Хэшируем пустой файл
   crypto dgst -alg sha3-256 -i tests/empty.txt
   # Ожидаемый вывод: a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a tests/empty.txt
   
   ## Хэшируем файл со строкой "abc"
   crypto dgst -alg sha3-256 -i tests/test_one.txt
   # Ожидаемый вывод: 3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532  tests/test_one.txt
   
```

### Тестирование хэш-функций sha256 и sha3-256 на интероперабельность

```bash
  # Тестирование SHA-256 с sha256sum
crypto dgst -alg sha256 -i tests/empty.txt.txt -o tests/output_hash.txt
sha256sum tests/empty.txt.txt > tests/system_hash.txt
diff -s tests/output_hash.txt tests/system_hash.txt
# Ожидаемый вывод: Files tests/output_hash.txt and tests/system_hash.txt are identical

# Тестирование SHA3-256 с sha3sum
crypto dgst -alg sha3-256 -i tests/empty.txt.txt -o tests/output_hash.txt
sha3sum -a 256 tests/empty.txt.txt > tests/system_hash.txt
diff -s tests/output_hash.txt tests/system_hash.txt
# Ожидаемый вывод: Files tests/output_hash.txt and tests/system_hash.txt are identical
```

### Тестирование хэш-функций на файле ~1gb

```bash
   crypto dgst -alg sha256 -i tests/test1gb.txt
   # Ожидаемый вывод: d5739a8da2a57adb3b9a38495a389894227f5e083efb541b0b4473faccd55225  tests/test1gb.txt
```
## Тестирование HMAC
### Тесты с известными векторами RFC-4231
```
# Ключ - 20 байт
echo "Hi There" > tests/message.txt 
crypto dgst -alg sha256 --hmac -k 0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b -i tests/message.txt
# b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7  tests/message.txt

# Ключ - 131 байт
echo -n "Test Using Larger Than Block-Size Key - Hash Key First" > tests/message.txt
crypto dgst -alg sha256 --hmac -k aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -i tests/message.txt
# 60e431591ee0b67f0d8a26aacbf5b77f8e0bc6213728c5140546040f0ee37f54  tests/message.txt
```

### Тест верификации и обнаружения искажения
```
# Генерация HMAC
echo "original_content" > tests/message.txt
crypto dgst -alg sha256 --hmac -k 00112233445566778899aabbccddeeff -i tests/message.txt -o tests/original_hmac.txt

# Проверка (должна пройти)
crypto dgst -alg sha256 --hmac -k 00112233445566778899aabbccddeeff -i tests/message.txt -v tests/original_hmac.txt
# Вывод: [OK] Проверка HMAC успешна

# Изменение файла
echo "modified_content" > tests/message.txt
crypto dgst -alg sha256 --hmac -k 00112233445566778899aabbccddeeff -i tests/message.txt -v tests/original_hmac.txt
# Вывод: [ERROR] Проверка HMAC неверна
```
## Тестирование GCM
### TEST-1: NIST Test Vectors
```
# NIST Test Case 1: Empty plaintext, empty AAD
echo -n "" > tests/aead/nist_test1.txt

crypto -alg aes -m gcm -enc \
    -k 00000000000000000000000000000000 \
    --aad "" \
    -i tests/aead/nist_test1.txt \
    -o tests/aead/nist_test1_cipher.bin

# Размер должен быть 28 байт: 12 (nonce) + 0 (ciphertext) + 16 (tag)
wc -c < tests/aead/nist_test1_cipher.bin
# Ожидаемый вывод: 28

# Расшифровываем и проверяем
crypto -alg aes -m gcm -dec \
    -k 00000000000000000000000000000000 \
    --aad "" \
    -i tests/aead/nist_test1_cipher.bin \
    -o tests/aead/nist_test1_decrypted.txt

diff -s tests/aead/nist_test1.txt tests/aead/nist_test1_decrypted.txt
# Ожидаемый вывод: Files ... are identical
```

## TEST-2: Round-trip Test
```
# Создаём тестовый файл
echo -n "The quick brown fox jumps over the lazy dog" > tests/aead/roundtrip.txt

# Шифруем
crypto -alg aes -m gcm -enc \
    -k 0123456789abcdef0123456789abcdef \
    --aad 48656c6c6f576f726c64 \
    -i tests/aead/roundtrip.txt \
    -o tests/aead/roundtrip_cipher.bin

# Расшифровываем
crypto -alg aes -m gcm -dec \
    -k 0123456789abcdef0123456789abcdef \
    --aad 48656c6c6f576f726c64 \
    -i tests/aead/roundtrip_cipher.bin \
    -o tests/aead/roundtrip_decrypted.txt

# Проверяем
diff -s tests/aead/roundtrip.txt tests/aead/roundtrip_decrypted.txt
# Ожидаемый вывод: Files ... are identical
```

## TEST-3: AAD Tampering Detection
```
# Шифруем с правильным AAD
echo -n "Secret message" > tests/aead/aad_test.txt

crypto -alg aes -m gcm -enc \
    -k 00112233445566778899aabbccddeeff \
    --aad 636f72726563745f616164 \
    -i tests/aead/aad_test.txt \
    -o tests/aead/aad_test_cipher.bin

# Пытаемся расшифровать с НЕВЕРНЫМ AAD
crypto -alg aes -m gcm -dec \
    -k 00112233445566778899aabbccddeeff \
    --aad 77726f6e675f616164 \
    -i tests/aead/aad_test_cipher.bin \
    -o tests/aead/aad_test_fail.txt

# Ожидаемый вывод: [ERROR] Ошибка аутентификации

# Проверяем что файл НЕ создан
ls tests/aead/aad_test_fail.txt 2>&1
# Ожидаемый вывод: No such file or directory
```
### TEST-4: Ciphertext Tampering Detection
```
# Шифруем
echo -n "Message to tamper" > tests/aead/tamper_test.txt

crypto -alg aes -m gcm -enc \
    -k ffeeddccbbaa99887766554433221100 \
    --aad aabbccdd \
    -i tests/aead/tamper_test.txt \
    -o tests/aead/tamper_cipher.bin

# Копируем и модифицируем
cp tests/aead/tamper_cipher.bin tests/aead/tamper_modified.bin

python3 -c "data = bytearray(open('tests/aead/tamper_modified.bin', 'rb').read()); data[20] ^= 0x01; open('tests/aead/tamper_modified.bin', 'wb').write(data)"

# Пытаемся расшифровать
crypto -alg aes -m gcm -dec \
    -k ffeeddccbbaa99887766554433221100 \
    --aad aabbccdd \
    -i tests/aead/tamper_modified.bin \
    -o tests/aead/tamper_fail.txt

# Ожидаемый вывод: [ERROR] Ошибка аутентификации

# Файл НЕ создан
ls tests/aead/tamper_fail.txt 2>&1
# Ожидаемый вывод: No such file or directory
```
### TEST-5: Nonce Uniqueness
```
python3 -c "
import sys
sys.path.insert(0, '.')
from cryptocoreedu.modes.GCMMode import GCMMode
nonces = set()
key = bytes.fromhex('00112233445566778899aabbccddeeff')
for i in range(1000):
    gcm = GCMMode(key)
    nonces.add(gcm.nonce)
print(f'Unique nonces: {len(nonces)} out of 1000')
print('PASSED' if len(nonces) == 1000 else 'FAILED')
"
# Ожидаемый вывод: 
# Unique nonces: 1000 out of 1000
# PASSED
```
### TEST-6: Empty AAD
```
echo -n "Message with empty AAD" > tests/aead/empty_aad.txt

# Шифруем с пустым AAD
crypto -alg aes -m gcm -enc \
    -k 11111111111111111111111111111111 \
    --aad "" \
    -i tests/aead/empty_aad.txt \
    -o tests/aead/empty_aad_cipher.bin

# Расшифровываем с пустым AAD
crypto -alg aes -m gcm -dec \
    -k 11111111111111111111111111111111 \
    --aad "" \
    -i tests/aead/empty_aad_cipher.bin \
    -o tests/aead/empty_aad_decrypted.txt

diff -s tests/aead/empty_aad.txt tests/aead/empty_aad_decrypted.txt
# Ожидаемый вывод: Files ... are identical
```

### TEST-7: Large AAD
```
# Генерируем большой AAD (10KB в hex)
LARGE_AAD=$(python3 -c "import os; print(os.urandom(10240).hex())")

echo -n "Message with large AAD" > tests/aead/large_aad.txt

# Шифруем
crypto -alg aes -m gcm -enc \
    -k 33333333333333333333333333333333 \
    --aad "$LARGE_AAD" \
    -i tests/aead/large_aad.txt \
    -o tests/aead/large_aad_cipher.bin

# Расшифровываем
crypto -alg aes -m gcm -dec \
    -k 33333333333333333333333333333333 \
    --aad "$LARGE_AAD" \
    -i tests/aead/large_aad_cipher.bin \
    -o tests/aead/large_aad_decrypted.txt

diff -s tests/aead/large_aad.txt tests/aead/large_aad_decrypted.txt
# Ожидаемый вывод: Files ... are identical
```

## Тестирование ETM
### TEST-9.1: ETM Round-trip
```
echo -n "ETM test message" > tests/aead/etm_plain.txt

crypto -alg aes -m etm -enc \
    -k 00112233445566778899aabbccddeeff \
    --aad 616263 \
    -i tests/aead/etm_plain.txt \
    -o tests/aead/etm_cipher.bin

crypto -alg aes -m etm -dec \
    -k 00112233445566778899aabbccddeeff \
    --aad 616263 \
    -i tests/aead/etm_cipher.bin \
    -o tests/aead/etm_decrypted.txt

diff -s tests/aead/etm_plain.txt tests/aead/etm_decrypted.txt
# Ожидаемый вывод: Files ... are identical
```
### TEST-9.2: ETM AAD Tampering
```
crypto -alg aes -m etm -dec \
    -k 00112233445566778899aabbccddeeff \
    --aad 646566 \
    -i tests/aead/etm_cipher.bin \
    -o tests/aead/etm_aad_fail.txt

# Ожидаемый вывод: [ERROR] Ошибка аутентификации

ls tests/aead/etm_aad_fail.txt 2>&1
# Ожидаемый вывод: No such file or directory
```
### TEST-9.3: ETM Ciphertext Tampering
```
cp tests/aead/etm_cipher.bin tests/aead/etm_tampered.bin

python3 -c "
data = bytearray(open('tests/aead/etm_tampered.bin', 'rb').read())
data[20] ^= 0x01
open('tests/aead/etm_tampered.bin', 'wb').write(data)
"

crypto -alg aes -m etm -dec \
    -k 00112233445566778899aabbccddeeff \
    --aad 616263 \
    -i tests/aead/etm_tampered.bin \
    -o tests/aead/etm_tamper_fail.txt

# Ожидаемый вывод: [ERROR] Ошибка аутентификации
ls tests/aead/etm_tamper_fail.txt 2>&1
# Ожидаемый вывод: No such file or directory
```
### TEST-9.4: ETM Wrong Key
```
crypto -alg aes -m etm -dec \
    -k ffffffffffffffffffffffffffffffff \
    --aad 616263 \
    -i tests/aead/etm_cipher.bin \
    -o tests/aead/etm_wrong_key.txt

# Ожидаемый вывод: [ERROR] Ошибка аутентификации
ls tests/aead/etm_wrong_key.txt 2>&1
# Ожидаемый вывод: No such file or director
```
## Тестирование 
### TEST-1: Known-Answer Tests (PBKDF2-HMAC-SHA256)
```
python main.py derive --password "password" --salt 73616c74 --iterations 1 --length 20
# Ожидается: 120fb6cffcf8b32c43e7225256c4f837a86548c9 73616c74

# Тест 2: iterations=2, length=20
python main.py derive --password "password" --salt 73616c74 --iterations 2 --length 20
# Ожидается: ae4d0c95af6b46d32d0adff928f06dd02a303f8e 73616c74

# Тест 3: iterations=4096, length=20
python main.py derive --password "password" --salt 73616c74 --iterations 4096 --length 20
# Ожидается: c5e478d59288c841aa530db6845c4c8d962893a0 73616c74

# Тест 4: iterations=4096, length=32 (полный блок SHA256)
python main.py derive --password "password" --salt 73616c74 --iterations 4096 --length 32
# Ожидается: c5e478d59288c841aa530db6845c4c8d962893a001ce4e11a4963873aa98134a 73616c74

# Тест 5: длинный пароль и соль, length=25
python main.py derive --password "passwordPASSWORDpassword" --salt 73616c7453414c5473616c7453414c5473616c7453414c5473616c7453414c5473616c74 --iterations 4096 --length 25
# Ожидается: 348c89dbcbd32b2f32d814b8116e84cf2b17347ebc1800181c 73616c7453414c5473616c7453414c5473616c7453414c5473616c7453414c5473616c74
```
### TEST-2: Iteration Test (одинаковые параметры = одинаковый результат)
```
# Запустить 5 раз подряд - результат должен быть идентичным
python main.py derive --password "TestPassword123" --salt aabbccdd11223344 --iterations 1000 --length 32
python main.py derive --password "TestPassword123" --salt aabbccdd11223344 --iterations 1000 --length 32
python main.py derive --password "TestPassword123" --salt aabbccdd11223344 --iterations 1000 --length 32
python main.py derive --password "TestPassword123" --salt aabbccdd11223344 --iterations 1000 --length 32
python main.py derive --password "TestPassword123" --salt aabbccdd11223344 --iterations 1000 --length 32
# Все 5 результатов должны быть абсолютно одинаковыми
```
### TEST-3: Length Test (ключи различной длины 1-100 байт)
```
# Длина 1 байт
python main.py derive --password "password" --salt 73616c74 --iterations 100 --length 1
# Ожидается: 1 байт (2 hex символа)

# Длина 16 байт
python main.py derive --password "password" --salt 73616c74 --iterations 100 --length 16
# Ожидается: 16 байт (32 hex символа)

# Длина 31 байт (меньше блока SHA256)
python main.py derive --password "password" --salt 73616c74 --iterations 100 --length 31
# Ожидается: 31 байт (62 hex символа)

# Длина 32 байт (ровно 1 блок SHA256)
python main.py derive --password "password" --salt 73616c74 --iterations 100 --length 32
# Ожидается: 32 байт (64 hex символа)

# Длина 33 байт (больше 1 блока, нужен 2-й)
python main.py derive --password "password" --salt 73616c74 --iterations 100 --length 33
# Ожидается: 33 байт (66 hex символов)

# Длина 64 байт (ровно 2 блока)
python main.py derive --password "password" --salt 73616c74 --iterations 100 --length 64
# Ожидается: 64 байт (128 hex символов)

# Длина 100 байт
python main.py derive --password "password" --salt 73616c74 --iterations 100 --length 100
# Ожидается: 100 байт (200 hex символов)
```
### TEST-4: Interoperability Test с OpenSSL 
```
# Наша реализация
python main.py derive --password "test" --salt 1234567890abcdef --iterations 1000 --length 32
# 4cd8b5c46aee47f0d4a6a0dd7c205b1d30b54d2503c13fe7422e95ea312b7425
   
# OpenSSL (если установлен, версия 3.0+)
openssl kdf -keylen 32 -kdfopt digest:SHA256 -kdfopt pass:test -kdfopt hexsalt:1234567890abcdef -kdfopt iter:1000 PBKDF2
# Результаты должны совпадать. 4cd8b5c46aee47f0d4a6a0dd7c205b1d30b54d2503c13fe7422e95ea312b7425
```
### TEST-5: Key Hierarchy Test (derive_key детерминистичен)
```
# Запустить 5 раз с одинаковым мастер-ключом и контекстом
python main.py derive --master-key 0000000000000000000000000000000000000000000000000000000000000000 --context "encryption" --length 32
python main.py derive --master-key 0000000000000000000000000000000000000000000000000000000000000000 --context "encryption" --length 32
python main.py derive --master-key 0000000000000000000000000000000000000000000000000000000000000000 --context "encryption" --length 32
python main.py derive --master-key 0000000000000000000000000000000000000000000000000000000000000000 --context "encryption" --length 32
python main.py derive --master-key 0000000000000000000000000000000000000000000000000000000000000000 --context "encryption" --length 32
# Все 5 результатов должны быть идентичными
```
### TEST-6: Context Separation Test (разные контексты = разные ключи)
```
# Один и тот же мастер-ключ, разные контексты
python main.py derive --master-key aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa --context "encryption" --length 32
python main.py derive --master-key aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa --context "authentication" --length 32
python main.py derive --master-key aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa --context "signing" --length 32
python main.py derive --master-key aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa --context "key_wrapping" --length 32
python main.py derive --master-key aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa --context "iv_generation" --length 32
# Все 5 ключей должны быть РАЗНЫМИ!
```
### TEST-7: Salt Randomness Test (уникальность генерируемых солей)
```
# Запустить несколько раз без --salt и проверить что соли разные
python main.py derive --password "test" --length 16
python main.py derive --password "test" --length 16
python main.py derive --password "test" --length 16
python main.py derive --password "test" --length 16
python main.py derive --password "test" --length 16
# Каждый раз соль (вторая часть вывода) должна быть уникальной
```


## Требования

- Python 3.8 или выше
- pycryptodome 3.23.0 или выше
- numba
- numpy

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
│   ├── crypto/               
│   │   ├── __init__.py
│   │   ├── aes.py           
│   │   └── padding.py       
│   ├── hash/                 
│   │   ├── __init__.py
│   │   ├── sha256.py        
│   │   └── sha3_256.py 
│   ├── kdf/
│   │   ├── __init__.py
│   │   ├── hkdf.py   
│   │   └── pbkdf2.py 
│   ├── mac/                  
│   │   ├── __init__.py
│   │   └── hmac.py          
│   ├── modes/               
│   │   ├── __init__.py
│   │   ├── ecb.py          
│   │   ├── cbc.py          
│   │   ├── cfb.py          
│   │   ├── ofb.py          
│   │   ├── ctr.py 
│   │   ├── etm.py        
│   │   └── gcm.py          
│   ├── __init__.py         
│   ├── cli.py              
│   ├── csprng.py           
│   ├── exceptions.py       
│   └── file_io.py          
├── tests/                  
│   ├── __init__.py
│   ├── test_gcm.py        
│   ├── test_openssl.py    
│   ├── tests_hash.py      
│   ├── test_csprng.py     
│   ├── plain.txt        
│   ├── cipher.bin
│   ├── decrypted.txt
│   ├── modified.txt
│   └── test_etm.txt
├── .gitignore             
├── main.py               
├── README.md             
└── requirements.txt      
```

