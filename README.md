
# CryptoCore

Утилита командной строки для блочного шифрования файлов с использованием AES-128 в различных режимах работы.

## Возможности

* Поддержка алгоритма AES-128
* Режимы работы: ECB, CBC, CFB, OFB, CTR
* Шифрование и дешифрование файлов
* Совместимость с OpenSSL
* Безопасная генерация IV

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

### Базовые команды

Шифрование файла в режиме CBC:

```shell
cryptocoreutils --algorithm aes --mode cbc --encrypt \
       --key 000102030405060708090a0b0c0d0e0f \
       --input document.txt \
       --output document.enc
```

Дешифрование файла в режиме CBC:

```shell
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

## Команды хэширования
```shell
# хэширование без указания выходного файла 
python main.py dgst -alg sha256 -i document.pdf
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 document.pdf

# хэширование с указанием выходного файла
python main.py dgst -alg sha3-256 -i backup.tar -o backup.sha3
```
## Параметры хэш-функций
- `--algorithm (-alg)`: Алгоритм хэширования (`sha256`, `sha3-256`)
- `--input (-i)`: Входной файл
- `--output (-o)`: Выходной файл (опционально)

**Формат вывода хэша**:
#### e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 document.pdf

## HMAC (Hash-based Message Authentication Code)
HMAC обеспечивает проверку целостности и подлинности данных с использованием секретного ключа. Реализовано согласно RFC 2104.
### Генерация HMAC
```bash
# HMAC-SHA256
cryptocore dgst --algorithm sha256 --hmac --key <ключ_в_hex> --input <файл>

# HMAC-SHA3-256
cryptocore dgst --algorithm sha3-256 --hmac --key <ключ_в_hex> --input <файл>

# С сохранением в файл
cryptocore dgst --algorithm sha256 --hmac --key <ключ> --input <файл> --output hmac.txt
```
### Проверка HMAC
```bash
#cryptocore dgst --algorithm sha256 --hmac --key <ключ> --input <файл> --verify hmac.txt

# При успехе: [OK] HMAC verification successful
# При ошибке: [ERROR] HMAC verification failed
```
### Параметры HMAC 
* --hmac: включить режим HMAC
* --key, -k: секретный ключ в шестнадцатеричном формате
* --verify: файл с ожидаемым HMAC для проверки

### Пример использования
```bash
# 1. Генерация HMAC
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input document.pdf --output doc.hmac

# 2. Проверка HMAC (должна пройти)
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input document.pdf --verify doc.hmac

# 3. Изменяем файл
echo "изменения" >> document.pdf

# 4. Проверка HMAC (должна провалиться)  
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input document.pdf --verify doc.hmac
```
### Особенности реализации 
* Поддержка ключей произвольной длины

* Автоматическая обработка ключей (хеширование длинных ключей, дополнение коротких)

* Сравнение HMAC с защитой от атак по времени

  * Поддержка SHA-256 и SHA3-256
### Размер ключа и IV
Ключ должен быть ровно **16 байт** (32 hex-символа):
```
Правильно: 000102030405060708090a0b0c0d0e0f
Неправильно: mykey123 (8 байт)
```
IV должен быть ровно **16 байт** (32 hex-символа):
```
Правильно: AABBCCDDEEFF00112233445566778899
Неправильно: ASFSAFSA909DAS9DA99129129DNNBN
```

## Совместимость с OpenSSL

### Шифрование утилитой, дешифрование OpenSSL

```bash
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

```bash
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
   
### Тестирование хэш-функций

#### Тестирование хэш-функций sha256 и sha3-256 на тестовых векторах

```bash
   # Тестирование sha256 (Linux/MacOS/WSL)
   ## Хэшируем пустой файл
   crypto dgst -alg sha256 -i tests/empty.txt
   # Ожидаемый вывод: e3b0c44298fc1c149afbf4c899cfb92427ae41e4649b934ca495991b7852b855 tests/empty.txt
   
   ## Хэшируем файл со строкой "abc"
   crypto dgst -alg sha256 -i tests/test_one.txt
   # Ожидаемый вывод: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  tests/test_one.txt
   
   ## Хэшируем файл со строкой "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
   crypto dgst -alg sha256 -i tests/test_two.txt
   # Ожидаемый вывод: 248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1  tests/test_two.txt

```

```bash
   # Тестирование sha3-256 (Linux/MacOS/WSL)
   ## Хэшируем пустой файл
   crypto dgst -alg sha3-256 -i tests/empty.txt
   # Ожидаемый вывод: a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a tests/empty.txt
   
   ## Хэшируем файл со строкой "abc"
   crypto dgst -alg sha3-256 -i tests/test_one.txt
   # Ожидаемый вывод: 3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532  tests/test_one.txt
   
   ## Хэшируем файл со строкой "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
   crypto dgst -alg sha3-256 -i tests/test_two.txt
   # Ожидаемый вывод: 41c0dba2a9d6240849100376a8235e2c82e1b9998a999e21db32dd97496d3376  tests/test_two.txt

```

#### Тестирование хэш-функций sha256 и sha3-256 на интероперабельность

```bash
   # Тестирование sha256 (Linux/MacOS/WSL)
   # хэшируем пустой файл нашей реализацией
   crypto dgst -alg sha256 -i tests/empty.txt -o tests/output_hash.txt
   # хэшируем пустой файл с помощью sha256sum
   sha256sum tests/empty.txt > tests/system_hash.txt
   # проверяем идентичность
   diff -s tests/output_hash.txt tests/system_hash.txt
   #Ожидаемый вывод: Files tests/output_hash.txt and tests/system_hash.txt are identical
```

```bash
   # Тестирование sha3-256 (Linux/MacOS/WSL)
   # хэшируем пустой файл нашей реализацией
   crypto dgst -alg sha3-256 -i tests/empty.txt -o tests/output_hash.txt
   # хэшируем пустой файл с помощью sha3sum
   sha3sum -a 256 tests/empty.txt > tests/system_hash.txt
   # проверяем идентичность
   diff -s tests/output_hash.txt tests/system_hash.txt
   #Ожидаемый вывод: Files tests/output_hash.txt and tests/system_hash.txt are identical
```

#### Тестирование хэш-функций на файле ~1gb

```bash
   crypto dgst -alg sha256 -i tests/test1gb.txt
   # Ожидаемый вывод: d5739a8da2a57adb3b9a38495a389894227f5e083efb541b0b4473faccd55225  tests/test1gb.txt
   # Примерное время выполнение около 50-55 секунд
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

