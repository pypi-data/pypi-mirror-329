"""
Модуль предоставляет интерфейс командной строки для отправки SMS сообщений через SMPP.

Пример использования:
    python -m smsaero_smpp.command_line --login LOGIN --password PASSWORD --phone +79991234567 --message "Hello"
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
        description="Отправка SMS сообщений через SMPP протокол",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--login", required=True, help="Логин для подключения к SMPP серверу")
    parser.add_argument("--password", required=True, help="Пароль для подключения к SMPP серверу")
    parser.add_argument("--phone", required=True, help="Номер телефона получателя")
    parser.add_argument("--message", required=True, help="Текст сообщения")
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
    Основная функция для отправки SMS.

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

        result = client.send_sms(args.phone, args.message)

        # Вывод результата в консоль
        print("Результат отправки:")
        print(f"Статус: {result['status']}")
        print(f"Количество частей: {result['parts_count']}")
        for msg in result["messages"]:
            print(f"Sequence: {msg['sequence']}")
            print(f"Message ID: {msg['message_id']}")

        return 0

    except Exception as e:  # pylint: disable=broad-except
        print(f"Ошибка: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
