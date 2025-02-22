"""
Модуль с кастомными исключениями для SMPP клиента.
"""


class SmsAeroError(Exception):
    """Базовое исключение для всех ошибок SmsAero."""


class SmsAeroConnectionError(SmsAeroError):
    """Исключение при ошибке подключения к SMPP серверу."""

    URL = "https://smsaero.ru/cabinet/settings/apikey/"

    def __init__(self, message="Ошибка подключения к SMPP серверу"):
        self.message = f"{message}. Убедитесь, что ваш IP адрес добавлен в белый список в личном кабинете: {self.URL}"
        super().__init__(self.message)


class SmsAeroValidationError(SmsAeroError):
    """Исключение при ошибке валидации."""


class SmsAeroTimeoutError(SmsAeroError):
    """Исключение при превышении времени ожидания."""
