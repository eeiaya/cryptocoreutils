
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

