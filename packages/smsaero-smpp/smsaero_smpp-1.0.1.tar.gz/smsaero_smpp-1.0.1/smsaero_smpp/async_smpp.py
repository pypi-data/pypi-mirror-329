"""
Асинхронная версия SMPP клиента.
"""

import asyncio
import typing
from typing import Optional

from .smpp import SmsAeroSmpp


class AsyncSmsAeroSmpp:
    """Асинхронный класс для отправки SMS через SMPP протокол."""

    def __init__(
        self,
        login: str,
        password: str,
        ip: str = SmsAeroSmpp.DEFAULT_IP,
        port: int = SmsAeroSmpp.DEFAULT_PORT,
        source: str = SmsAeroSmpp.DEFAULT_SOURCE,
        timeout: float = 30.0,
        retry_max_attempts: int = SmsAeroSmpp.DEFAULT_RETRY_MAX_ATTEMPTS,
        retry_delay: float = SmsAeroSmpp.DEFAULT_RETRY_DELAY,
        retry_backoff: float = SmsAeroSmpp.DEFAULT_RETRY_BACKOFF,
    ) -> None:
        self._smpp = SmsAeroSmpp(
            login=login,
            password=password,
            ip=ip,
            port=port,
            source=source,
            timeout=timeout,
            retry_max_attempts=retry_max_attempts,
            retry_delay=retry_delay,
            retry_backoff=retry_backoff,
        )
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    async def send_sms(self, phone: str, message: str) -> typing.Dict:
        """Асинхронная отправка SMS."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._smpp.send_sms, phone, message)

    async def sms_status(self, message_id: str) -> typing.Dict:
        """Асинхронная проверка статуса SMS."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._smpp.sms_status, message_id)
