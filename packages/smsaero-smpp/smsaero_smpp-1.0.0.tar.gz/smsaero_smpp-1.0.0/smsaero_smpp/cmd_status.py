"""
Командная строка для проверки статуса SMS сообщения.
"""

import argparse
import logging
import sys

from .smpp import SmsAeroSmpp
from .logging import setup_logger


def create_parser() -> argparse.ArgumentParser:
    """
    Создает парсер аргументов командной строки.

    Returns:
        argparse.ArgumentParser: Настроенный парсер аргументов
    """
    parser = argparse.ArgumentParser(
        description="Проверка статуса SMS сообщения через SMPP протокол",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--login", required=True, help="Логин для подключения к SMPP серверу")
    parser.add_argument("--password", required=True, help="Пароль для подключения к SMPP серверу")
    parser.add_argument("--message-id", required=True, help="ID сообщения для проверки статуса")
    parser.add_argument(
        "--ip", help="IP адрес SMPP сервера (по умолчанию: %(default)s)", default=SmsAeroSmpp.DEFAULT_IP
    )
    parser.add_argument(
        "--port", type=int, help="Порт SMPP сервера (по умолчанию: %(default)s)", default=SmsAeroSmpp.DEFAULT_PORT
    )
    parser.add_argument(
        "--source", help="Имя отправителя (по умолчанию: %(default)s)", default=SmsAeroSmpp.DEFAULT_SOURCE
    )
    parser.add_argument("--debug", action="store_true", help="Включить режим отладки")
    return parser


def main() -> int:
    """
    Основная функция для проверки статуса SMS.

    Returns:
        int: Код возврата (0 - успех, 1 - ошибка)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Настройка логирования
    setup_logger(level=logging.DEBUG if args.debug else logging.INFO)

    try:
        client = SmsAeroSmpp(
            login=args.login,
            password=args.password,
            ip=args.ip,
            port=args.port,
            source=args.source,
        )

        result = client.sms_status(args.message_id)

        # Вывод результата в консоль
        print("Результат проверки статуса:")
        print(f"Message ID: {result['message_id']}")
        print(f"Статус: {result['status']}")
        if result["error_code"] is not None:
            print(f"Код ошибки: {result['error_code']}")
        print(f"Финальный статус: {'Да' if result['final'] else 'Нет'}")

        return 0

    except Exception as e:  # pylint: disable=broad-except
        print(f"Ошибка: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
