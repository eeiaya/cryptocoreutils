
"""Работа с файлами"""

def read_file(file_path: str) -> bytes:
    """Чтение файла"""
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла {file_path}: {e}")

def write_file(file_path: str, data: bytes) -> None:
    """Запись файла"""
    try:
        with open(file_path, 'wb') as f:
            f.write(data)
    except Exception as e:
        raise Exception(f"Ошибка при записи файла {file_path}: {e}")