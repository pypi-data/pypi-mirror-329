"""
Модуль для отправки SMS сообщений через SMPP протокол.
"""

from .async_smpp import AsyncSmsAeroSmpp
from .errors import SmsAeroError, SmsAeroConnectionError, SmsAeroValidationError, SmsAeroTimeoutError
from .smpp import SmsAeroSmpp
from .types import SendResult, StatusResult, MessageInfo
from .validators import validate_phone, validate_ip, validate_port, validate_message
from .logging import setup_logger

# Настройка логирования по умолчанию
setup_logger()

__all__ = [
    # Основные классы
    "SmsAeroSmpp",
    "AsyncSmsAeroSmpp",
    # Исключения
    "SmsAeroError",
    "SmsAeroConnectionError",
    "SmsAeroValidationError",
    "SmsAeroTimeoutError",
    # Типы данных
    "SendResult",
    "StatusResult",
    "MessageInfo",
    # Валидаторы
    "validate_phone",
    "validate_ip",
    "validate_port",
    "validate_message",
    # Утилиты
    "setup_logger",
]
