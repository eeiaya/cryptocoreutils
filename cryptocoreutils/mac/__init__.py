"""
Модуль для вычисления Message Authentication Codes (MAC)
"""

from .hmac import (
    HMAC,
    hmac_data,
    hmac_file,
    verify_hmac,
    parse_hmac_file
)

__all__ = [
    'HMAC',
    'hmac_data',
    'hmac_file',
    'verify_hmac',
    'parse_hmac_file'
]