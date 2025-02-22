"""
Модуль с механизмом повторных попыток.
"""

import time
import logging
from typing import TypeVar, Callable, Any
from functools import wraps

from .errors import SmsAeroConnectionError, SmsAeroTimeoutError

logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (SmsAeroConnectionError, SmsAeroTimeoutError),
) -> Callable:
    """
    Декоратор для повторных попыток выполнения функции.

    Args:
        max_attempts: Максимальное количество попыток
        delay: Начальная задержка между попытками в секундах
        backoff: Множитель для увеличения задержки
        exceptions: Исключения, при которых нужно повторять попытки

    Returns:
        Callable: Декорированная функция
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            "Попытка %d из %d не удалась: %s. Следующая попытка через %.1f сек",
                            attempt + 1,
                            max_attempts,
                            str(e),
                            current_delay,
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error("Все попытки исчерпаны (%d из %d): %s", attempt + 1, max_attempts, str(e))

            if last_exception:
                raise last_exception
            raise RuntimeError("Unexpected state in retry")

        return wrapper

    return decorator
