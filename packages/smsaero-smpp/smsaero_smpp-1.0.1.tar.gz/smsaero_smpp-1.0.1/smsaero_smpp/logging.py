"""
Модуль с настройками логирования.
"""

import logging
from typing import Optional


def setup_logger(level: int = logging.ERROR, name: Optional[str] = None) -> logging.Logger:
    """
    Настройка логгера с заданными параметрами.

    Args:
        level: Уровень логирования
        name: Имя логгера

    Returns:
        logging.Logger: Настроенный логгер
    """
    # Настраиваем корневой логгер
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    if level == logging.DEBUG:
        # В режиме отладки показываем все логи
        root_logger.setLevel(level)

        # Настраиваем форматтер
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Добавляем обработчик для корневого логгера
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

        # В режиме отладки показываем все логи smpplib
        logging.getLogger("smpp").setLevel(level)
        logging.getLogger("smpplib").setLevel(level)
    else:
        # Без --debug отключаем все логи
        root_logger.setLevel(logging.CRITICAL + 1)  # Выше максимального уровня
        logging.getLogger("smpp").setLevel(logging.CRITICAL + 1)
        logging.getLogger("smpplib").setLevel(logging.CRITICAL + 1)

    # Настраиваем логгер для нашего приложения
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = True

    return logger
