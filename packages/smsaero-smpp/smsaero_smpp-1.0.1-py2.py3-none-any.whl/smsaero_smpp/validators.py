"""
Модуль с функциями валидации для SMPP клиента.
"""

import ipaddress

import phonenumbers


def validate_phone(phone: str) -> str:
    """
    Проверяет корректность номера телефона.

    Args:
        phone: Номер телефона для проверки

    Returns:
        str: Нормализованный номер телефона

    Raises:
        ValueError: Если номер телефона некорректен
    """
    try:
        phone_obj = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(phone_obj):
            raise ValueError("Некорректный номер телефона")
        return phonenumbers.format_number(phone_obj, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException as exc:
        raise ValueError("Не удалось распознать номер телефона") from exc


def validate_ip(ip: str) -> str:
    """
    Проверяет корректность IP адреса.

    Args:
        ip: IP адрес для проверки

    Returns:
        str: Проверенный IP адрес

    Raises:
        ValueError: Если IP адрес некорректен
    """
    try:
        ipaddress.ip_address(ip)
        return ip
    except ValueError as exc:
        raise ValueError("Некорректный IP адрес") from exc


def validate_port(port: int) -> int:
    """
    Проверяет корректность номера порта.

    Args:
        port: Номер порта для проверки

    Returns:
        int: Проверенный номер порта

    Raises:
        ValueError: Если номер порта некорректен
    """
    if not 1 <= port <= 65535:
        raise ValueError("Номер порта должен быть в диапазоне от 1 до 65535")
    return port


def validate_message(message: str) -> str:
    """
    Проверяет корректность текста сообщения.

    Args:
        message: Текст сообщения

    Returns:
        str: Проверенный текст сообщения

    Raises:
        ValueError: Если сообщение слишком длинное или пустое
    """
    if not message:
        raise ValueError("Текст сообщения не может быть пустым")
    if len(message) > 960:
        raise ValueError("Текст сообщения не может быть длиннее 960 символов")
    return message
