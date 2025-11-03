"""Работа с файлами"""
import os


def validate_file_exists(file_path: str) -> None:
    """Проверяет что файл существует"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")


def validate_file_not_empty(file_path: str) -> None:
    """Проверяет что файл не пустой"""
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"Файл пустой: {file_path}")


def validate_output_path(file_path: str) -> None:
    """Проверяет что можно создать выходной файл"""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if os.path.exists(file_path):
        print(f"Предупреждение: файл {file_path} будет перезаписан")


def read_file(file_path: str) -> bytes:
    """Чтение файла с валидацией"""
    validate_file_exists(file_path)
    validate_file_not_empty(file_path)

    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла {file_path}: {e}")


def write_file(file_path: str, data: bytes) -> None:
    """Запись файла с валидацией"""
    validate_output_path(file_path)

    try:
        with open(file_path, 'wb') as f:
            f.write(data)
    except Exception as e:
        raise Exception(f"Ошибка при записи файла {file_path}: {e}")


def read_file_with_iv(file_path: str) -> tuple[bytes, bytes]:
    """Чтение файла с извлечением IV из первых 16 байт"""
    data = read_file(file_path)
    if len(data) < 16:
        raise ValueError(f"Файл {file_path} слишком короткий для содержания IV")
    return data[:16], data[16:]


def write_file_with_iv(file_path: str, iv: bytes, data: bytes) -> None:
    """Запись файла с добавлением IV в начало"""
    write_file(file_path, iv + data)