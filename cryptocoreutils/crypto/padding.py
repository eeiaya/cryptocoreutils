"""Реализация PKCS7 padding"""


class PKCS7Padding:
    BLOCK_SIZE = 16

    @staticmethod
    def constant_time_compare(a: bytes, b: bytes) -> bool:
        """Сравнение с постоянным временем для безопасности"""
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0

    @classmethod
    def pad(cls, data: bytes) -> bytes:
        """Паддинг по PKCS#7"""
        if len(data) % cls.BLOCK_SIZE == 0:
            pad_len = cls.BLOCK_SIZE
        else:
            pad_len = cls.BLOCK_SIZE - (len(data) % cls.BLOCK_SIZE)
        return data + bytes([pad_len] * pad_len)

    @classmethod
    def unpad(cls, data: bytes) -> bytes:
        """Удаление паддинга по PKCS#7"""
        if not data:
            return data
        pad_len = data[-1]

        # Проверка корректности дополнения
        if pad_len > cls.BLOCK_SIZE or pad_len == 0:
            raise ValueError("Ошибка: Некорректное дополнение")

        expected_padding = bytes([pad_len] * pad_len)
        actual_padding = data[-pad_len:]

        if not cls.constant_time_compare(expected_padding, actual_padding):
            raise ValueError("Ошибка: Некорректное дополнение")

        return data[:-pad_len]