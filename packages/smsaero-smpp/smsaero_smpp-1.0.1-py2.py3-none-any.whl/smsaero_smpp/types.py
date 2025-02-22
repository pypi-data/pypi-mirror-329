"""
Модуль с типами данных для SMPP клиента.
"""

from typing import TypedDict, List, Optional


class MessageInfo(TypedDict):
    """
    Информация о сообщении после отправки.

    Attributes:
        sequence: Порядковый номер части сообщения
        message_id: Уникальный идентификатор сообщения, присвоенный SMPP сервером
    """

    sequence: int
    message_id: Optional[str]


class SendResult(TypedDict):
    """
    Результат отправки SMS сообщения.

    Attributes:
        status: Статус отправки ('success' или 'error')
        messages: Список информации о частях сообщения
        parts_count: Количество частей, на которые было разбито сообщение
    """

    status: str
    messages: List[MessageInfo]
    parts_count: int


class StatusResult(TypedDict):
    """
    Результат проверки статуса SMS сообщения.

    Attributes:
        message_id: Уникальный идентификатор сообщения
        status: Текущий статус сообщения ('delivered', 'expired', 'undeliverable' и т.д.)
        error_code: Код ошибки (если есть)
        final: Флаг, указывающий является ли статус финальным
    """

    message_id: str
    status: str
    error_code: Optional[int]
    final: bool
