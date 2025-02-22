"""
Основной модуль для работы с SMPP протоколом.
"""

import logging
import typing

import smpplib.client
import smpplib.consts
import smpplib.gsm

from .constants import (
    STATUS_MAPPING,
    FINAL_STATUSES,
    PDU_SUBMIT_SM_RESP,
    PDU_DELIVER_SM,
    PDU_QUERY_SM_RESP,
    PDU_GENERIC_NACK,
)
from .errors import SmsAeroConnectionError
from .types import MessageInfo
from .validators import validate_phone, validate_ip, validate_port, validate_message
from .retry import retry

logger = logging.getLogger(__name__)


class SmsAeroSmpp:
    """Класс для отправки SMS через SMPP протокол."""

    DEFAULT_IP = "82.202.194.38"
    DEFAULT_PORT = 2775
    DEFAULT_SOURCE = "SMS Aero"
    DEFAULT_RETRY_MAX_ATTEMPTS = 1
    DEFAULT_RETRY_DELAY = 1.0
    DEFAULT_RETRY_BACKOFF = 2.0

    def __init__(
        self,
        login: str,
        password: str,
        ip: str = DEFAULT_IP,
        port: int = DEFAULT_PORT,
        source: str = DEFAULT_SOURCE,
        timeout: float = 30.0,
        retry_max_attempts: int = DEFAULT_RETRY_MAX_ATTEMPTS,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        retry_backoff: float = DEFAULT_RETRY_BACKOFF,
    ):
        """
        Инициализация клиента SMPP.

        Args:
            login: Логин для SMPP сервера
            password: Пароль для SMPP сервера
            ip: IP адрес SMPP сервера
            port: Порт SMPP сервера
            source: Номер отправителя
            timeout: Тайм-аут для операций с SMPP сервером
            retry_max_attempts: Максимальное количество попыток
            retry_delay: Начальная задержка между попытками в секундах
            retry_backoff: Множитель для увеличения задержки

        Raises:
            ValueError: При некорректных значениях параметров
        """
        if not login or not password:
            raise ValueError("Логин и пароль не могут быть пустыми")

        self.login = login
        self.password = password
        self.ip = validate_ip(ip)
        self.port = validate_port(port)
        self.source = source
        self.timeout = timeout
        self.retry_max_attempts = retry_max_attempts
        self.retry_delay = retry_delay
        self.retry_backoff = retry_backoff
        self.client: typing.Optional[smpplib.client.Client] = None
        self._test_mode_enabled = False
        self._send_sms_impl = None
        self._sms_status_impl = None

    def _ensure_connection(self) -> smpplib.client.Client:
        """
        Проверяет и устанавливает соединение с SMPP сервером.

        Returns:
            smpplib.client.Client: Подключенный SMPP клиент

        Raises:
            SmsAeroConnectionError: При проблемах с подключением
        """
        try:
            if self.client is None:
                self.client = smpplib.client.Client(self.ip, self.port, timeout=self.timeout)
                self.client.connect()
                self.client.bind_transceiver(system_id=self.login, password=self.password)
            return self.client
        except (
            smpplib.exceptions.ConnectionError,
            smpplib.exceptions.PDUError,
            ConnectionRefusedError,
            OSError,
            TimeoutError,
        ) as e:
            self.client = None
            raise SmsAeroConnectionError() from e

    def _disconnect(self) -> None:
        """Безопасное отключение от SMPP сервера."""
        if self.client is not None:
            try:
                self.client.unbind()
                self.client.disconnect()
            except Exception as e:  # pylint: disable=broad-except
                logger.warning("Ошибка при отключении от SMPP сервера: %s", str(e))
            finally:
                self.client = None

    def _get_retry_decorator(self):
        """Создает декоратор retry с текущими настройками."""
        if self.retry_max_attempts <= 1:
            return lambda func: func
        return retry(max_attempts=self.retry_max_attempts, delay=self.retry_delay, backoff=self.retry_backoff)

    @property
    def send_sms(self):
        """Метод отправки SMS с текущими настройками retry."""
        if self._test_mode_enabled:
            return self._send_sms_impl
        return self._get_retry_decorator()(self._send_sms)

    @property
    def sms_status(self):
        """Метод проверки статуса с текущими настройками retry."""
        if self._test_mode_enabled:
            return self._sms_status_impl
        return self._get_retry_decorator()(self._sms_status)

    def _send_sms(self, phone: str, message: str) -> typing.Dict:
        """Внутренний метод отправки SMS без retry."""
        logger.info("Попытка отправки SMS на %s", phone)
        messages = []

        try:
            validated_phone = validate_phone(phone)
            validated_message = validate_message(message)
            parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(validated_message)

            client = self._ensure_connection()

            for part in parts:
                pdu = client.send_message(
                    source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    source_addr=self.source,
                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    destination_addr=validated_phone,
                    short_message=part,
                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                )

                while True:
                    resp_pdu = client.read_pdu()
                    if resp_pdu.command == PDU_SUBMIT_SM_RESP:
                        messages.append(
                            MessageInfo(
                                sequence=pdu.sequence,
                                message_id=resp_pdu.message_id.decode() if resp_pdu.message_id else None,
                            )
                        )
                        break
                    if resp_pdu.command == PDU_DELIVER_SM:
                        continue

                    messages.append(MessageInfo(sequence=pdu.sequence, message_id=None))
                    break

            logger.info("SMS успешно отправлено на: %s", phone)
            return {"status": "success", "messages": messages, "parts_count": len(parts)}

        except SmsAeroConnectionError:
            logger.error("Ошибка подключения к SMPP серверу")
            raise
        except ValueError as e:
            logger.error("Ошибка валидации: %s", str(e))
            raise
        except Exception as e:
            logger.error("Неожиданная ошибка при отправке SMS: %s", str(e))
            raise
        finally:
            self._disconnect()

    def _sms_status(self, message_id: str) -> typing.Dict:
        """Внутренний метод проверки статуса без retry."""
        if not message_id:
            raise ValueError("message_id не может быть пустым")

        logger.info("Запрос статуса для сообщения: %s", message_id)

        try:
            client = self._ensure_connection()

            client.query_message(
                message_id=message_id,
                source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                source_addr=self.source,
                dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                destination_addr="",
            )

            resp_pdu = client.read_pdu()

            if resp_pdu.command == PDU_GENERIC_NACK:
                logger.warning("Получен generic_nack, код ошибки: %s", getattr(resp_pdu, "command_status", "Unknown"))
                return {"message_id": message_id, "status": "unknown", "error_code": None, "final": False}

            if resp_pdu.command not in (PDU_QUERY_SM_RESP, PDU_DELIVER_SM):
                logger.warning("Получен неожиданный тип ответа: %s", resp_pdu.command)
                return {"message_id": message_id, "status": "unknown", "error_code": None, "final": False}

            message_state = None
            if hasattr(resp_pdu, "message_state"):
                if isinstance(resp_pdu.message_state, bytes):
                    message_state = resp_pdu.message_state.decode()
                elif isinstance(resp_pdu.message_state, int):
                    message_state = str(resp_pdu.message_state)
                else:
                    message_state = "UNKNOWN"
            elif hasattr(resp_pdu, "short_message"):
                try:
                    if isinstance(resp_pdu.short_message, bytes):
                        message_state = resp_pdu.short_message.decode()
                    elif isinstance(resp_pdu.short_message, int):
                        message_state = str(resp_pdu.short_message)
                    else:
                        message_state = str(resp_pdu.short_message)
                except (AttributeError, UnicodeDecodeError):
                    message_state = "UNKNOWN"

            logger.debug("Получен статус сообщения (raw): %s", message_state)
            message_state = str(message_state) if message_state is not None else "UNKNOWN"
            status = STATUS_MAPPING.get(message_state, "unknown")
            logger.debug("Преобразованный статус: %s", status)

            is_final = status in FINAL_STATUSES

            result = {
                "message_id": message_id,
                "status": status,
                "error_code": typing.cast(typing.Optional[int], getattr(resp_pdu, "command_status", None)),
                "final": bool(is_final),
            }

            logger.info("Получен статус для сообщения %s: %s", message_id, status)
            return result

        except SmsAeroConnectionError:
            logger.error("Ошибка подключения к SMPP серверу")
            raise
        except Exception as e:
            logger.error("Ошибка при получении статуса сообщения: %s", str(e))
            raise
        finally:
            self._disconnect()

    def check_connection(self) -> bool:
        """
        Проверяет доступность SMPP сервера.

        Returns:
            bool: True если сервер доступен, False в противном случае
        """
        try:
            client = self._ensure_connection()
            return bool(client)
        except Exception:  # pylint: disable=broad-except
            return False
        finally:
            self._disconnect()

    def _test_mode(self):
        """Специальный метод для тестирования, отключающий retry механизм."""
        self._test_mode_enabled = True
        self._send_sms_impl = self._send_sms
        self._sms_status_impl = self._sms_status
        return self
