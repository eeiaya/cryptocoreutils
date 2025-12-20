class CryptoOperationError(Exception):
    """Базовое исключение для операций шифрования"""
    pass

class AuthenticationError(CryptoOperationError):
    """Исключение при провале аутентификации"""
    pass

class InvalidKeyError(CryptoOperationError):
    """Исключение при неверном ключе"""
    pass

class InvalidModeError(CryptoOperationError):
    """Исключение при неверном режиме"""
    pass