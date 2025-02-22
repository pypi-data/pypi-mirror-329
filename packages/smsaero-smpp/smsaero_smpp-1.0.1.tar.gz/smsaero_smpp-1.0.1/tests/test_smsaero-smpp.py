"""
Модуль тестирования для библиотеки smsaero_smpp.
"""

import unittest
from unittest.mock import Mock, patch
import smpplib.exceptions
from smsaero_smpp import (
    SmsAeroSmpp,
    validate_phone,
    validate_ip,
    validate_port,
    validate_message,
    SmsAeroConnectionError,
)


class TestSmsAeroSmpp(unittest.TestCase):
    """Тесты для основного класса SmsAeroSmpp."""

    def setUp(self):
        """Инициализация тестового клиента."""
        self.client = SmsAeroSmpp(login="test_login", password="test_password")._test_mode()

    def test_init_with_default_values(self):
        """Тест инициализации с значениями по умолчанию."""
        self.assertEqual(self.client.ip, SmsAeroSmpp.DEFAULT_IP)
        self.assertEqual(self.client.port, SmsAeroSmpp.DEFAULT_PORT)
        self.assertEqual(self.client.source, SmsAeroSmpp.DEFAULT_SOURCE)

    def test_init_with_custom_values(self):
        """Тест инициализации с пользовательскими значениями."""
        client = SmsAeroSmpp(login="test_login", password="test_password", ip="127.0.0.1", port=1234, source="Custom")
        self.assertEqual(client.ip, "127.0.0.1")
        self.assertEqual(client.port, 1234)
        self.assertEqual(client.source, "Custom")

    def test_init_with_invalid_credentials(self):
        """Тест инициализации с некорректными учетными данными."""
        with self.assertRaises(ValueError):
            SmsAeroSmpp(login="", password="test")
        with self.assertRaises(ValueError):
            SmsAeroSmpp(login="test", password="")

    @patch("smpplib.client.Client")
    def test_send_sms_success(self, mock_client):
        """Тест успешной отправки SMS."""
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        # Настраиваем мок для PDU ответа
        mock_resp_pdu = Mock()
        mock_resp_pdu.command = "submit_sm_resp"
        mock_resp_pdu.message_id = b"test_message_id"
        mock_instance.read_pdu.return_value = mock_resp_pdu

        # Настраиваем sequence для PDU отправки
        mock_send_pdu = Mock()
        mock_send_pdu.sequence = 1
        mock_instance.send_message.return_value = mock_send_pdu

        result = self.client.send_sms("+79991234567", "Test message")

        expected_result = {
            "status": "success",
            "messages": [{"sequence": 1, "message_id": "test_message_id"}],
            "parts_count": 1,
        }

        self.assertEqual(result, expected_result)
        mock_instance.connect.assert_called_once()
        mock_instance.bind_transceiver.assert_called_once()
        mock_instance.send_message.assert_called()
        mock_instance.unbind.assert_called_once()
        mock_instance.disconnect.assert_called_once()

    @patch("smpplib.client.Client")
    def test_connection_error(self, mock_client):
        """Тест обработки ошибки подключения."""
        mock_instance = Mock()
        mock_instance.connect.side_effect = smpplib.exceptions.ConnectionError("Connection refused")
        mock_client.return_value = mock_instance

        with self.assertRaises(SmsAeroConnectionError) as context:
            self.client.send_sms("+79991234567", "Test message")

        self.assertIn("белый список", str(context.exception))
        mock_instance.connect.assert_called_once()

    @patch("smpplib.client.Client")
    def test_disconnect_error(self, mock_client):
        """Тест обработки ошибки при отключении."""
        mock_instance = Mock()
        mock_instance.disconnect.side_effect = Exception("Disconnect error")
        mock_client.return_value = mock_instance

        # Настраиваем мок для PDU ответа
        mock_resp_pdu = Mock()
        mock_resp_pdu.command = "submit_sm_resp"
        mock_resp_pdu.message_id = b"test_message_id"
        mock_instance.read_pdu.return_value = mock_resp_pdu

        # Настраиваем sequence для PDU отправки
        mock_send_pdu = Mock()
        mock_send_pdu.sequence = 1
        mock_instance.send_message.return_value = mock_send_pdu

        result = self.client.send_sms("+79991234567", "Test message")

        expected_result = {
            "status": "success",
            "messages": [{"sequence": 1, "message_id": "test_message_id"}],
            "parts_count": 1,
        }

        self.assertEqual(result, expected_result)

    def test_send_sms_validation_error(self):
        """Тест обработки ошибки валидации при отправке SMS."""
        with self.assertRaises(ValueError):
            self.client.send_sms("invalid", "Test message")

    @patch("smpplib.client.Client")
    def test_sms_status_success(self, mock_client):
        """Тест успешного получения статуса сообщения."""
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        # Настраиваем мок для PDU ответа
        mock_resp_pdu = Mock()
        mock_resp_pdu.command = "query_sm_resp"
        mock_resp_pdu.message_state = 2  # DELIVERED
        mock_resp_pdu.error_code = None
        mock_resp_pdu.command_status = None
        mock_instance.read_pdu.return_value = mock_resp_pdu

        result = self.client.sms_status("test_message_id")

        expected_result = {"message_id": "test_message_id", "status": "delivered", "error_code": None, "final": True}

        self.assertEqual(result, expected_result)
        mock_instance.connect.assert_called_once()
        mock_instance.bind_transceiver.assert_called_once()
        mock_instance.query_message.assert_called_once()
        mock_instance.unbind.assert_called_once()
        mock_instance.disconnect.assert_called_once()

    @patch("smpplib.client.Client")
    def test_sms_status_enroute(self, mock_client):
        """Тест получения промежуточного статуса сообщения."""
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        # Настраиваем мок для PDU ответа
        mock_resp_pdu = Mock()
        mock_resp_pdu.command = "query_sm_resp"
        mock_resp_pdu.message_state = 1  # ENROUTE
        mock_resp_pdu.error_code = None
        mock_resp_pdu.command_status = None
        mock_instance.read_pdu.return_value = mock_resp_pdu

        result = self.client.sms_status("test_message_id")

        expected_result = {"message_id": "test_message_id", "status": "enroute", "error_code": None, "final": False}

        self.assertEqual(result, expected_result)

    def test_sms_status_invalid_id(self):
        """Тест запроса статуса с некорректным message_id."""
        with self.assertRaises(ValueError):
            self.client.sms_status("")

    @patch("smpplib.client.Client")
    def test_sms_status_connection_error(self, mock_client):
        """Тест обработки ошибки подключения при запросе статуса."""
        mock_instance = Mock()
        mock_instance.connect.side_effect = smpplib.exceptions.ConnectionError("Connection refused")
        mock_client.return_value = mock_instance

        with self.assertRaises(SmsAeroConnectionError) as context:
            self.client.sms_status("test_message_id")

        self.assertIn("белый список", str(context.exception))
        mock_instance.connect.assert_called_once()

    @patch("smpplib.client.Client")
    def test_send_and_check_status_delivered(self, mock_client):
        """Тест отправки SMS и проверки успешной доставки."""
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        # Настраиваем мок для PDU ответа при отправке
        mock_send_resp_pdu = Mock()
        mock_send_resp_pdu.command = "submit_sm_resp"
        mock_send_resp_pdu.message_id = b"test_message_id"

        # Настраиваем мок для PDU ответа при проверке статуса
        mock_status_resp_pdu = Mock()
        mock_status_resp_pdu.command = "query_sm_resp"
        mock_status_resp_pdu.message_state = 2  # DELIVERED
        mock_status_resp_pdu.error_code = None
        mock_status_resp_pdu.command_status = None

        # Настраиваем sequence для PDU отправки
        mock_send_pdu = Mock()
        mock_send_pdu.sequence = 1

        # Настраиваем последовательность ответов
        mock_instance.read_pdu.side_effect = [mock_send_resp_pdu, mock_status_resp_pdu]
        mock_instance.send_message.return_value = mock_send_pdu

        # Отправляем сообщение
        send_result = self.client.send_sms("+79991234567", "Test message")
        expected_send_result = {
            "status": "success",
            "messages": [{"sequence": 1, "message_id": "test_message_id"}],
            "parts_count": 1,
        }
        self.assertEqual(send_result, expected_send_result)

        message_id = send_result["messages"][0]["message_id"]
        self.assertEqual(message_id, "test_message_id")

        # Проверяем статус
        status_result = self.client.sms_status(message_id)
        expected_status = {"message_id": "test_message_id", "status": "delivered", "error_code": None, "final": True}
        self.assertEqual(status_result, expected_status)

    @patch("smpplib.client.Client")
    def test_send_and_check_status_undeliverable(self, mock_client):
        """Тест отправки SMS и получения статуса недоставки."""
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        # Настраиваем мок для PDU ответа при отправке
        mock_send_resp_pdu = Mock()
        mock_send_resp_pdu.command = "submit_sm_resp"
        mock_send_resp_pdu.message_id = b"test_message_id"

        # Настраиваем мок для PDU ответа при проверке статуса
        mock_status_resp_pdu = Mock()
        mock_status_resp_pdu.command = "query_sm_resp"
        mock_status_resp_pdu.message_state = 5  # UNDELIVERABLE
        mock_status_resp_pdu.error_code = None
        mock_status_resp_pdu.command_status = None

        # Настраиваем sequence для PDU отправки
        mock_send_pdu = Mock()
        mock_send_pdu.sequence = 1

        # Настраиваем последовательность ответов
        mock_instance.read_pdu.side_effect = [mock_send_resp_pdu, mock_status_resp_pdu]
        mock_instance.send_message.return_value = mock_send_pdu

        # Отправляем сообщение
        send_result = self.client.send_sms("+79991234567", "Test message")
        expected_send_result = {
            "status": "success",
            "messages": [{"sequence": 1, "message_id": "test_message_id"}],
            "parts_count": 1,
        }
        self.assertEqual(send_result, expected_send_result)
        message_id = send_result["messages"][0]["message_id"]

        # Проверяем статус
        status_result = self.client.sms_status(message_id)
        expected_status = {
            "message_id": "test_message_id",
            "status": "undeliverable",
            "error_code": None,
            "final": True,
        }
        self.assertEqual(status_result, expected_status)

    @patch("smpplib.client.Client")
    def test_send_and_check_status_expired(self, mock_client):
        """Тест отправки SMS и получения статуса истечения срока доставки."""
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        # Настраиваем моки для отправки и проверки статуса
        mock_send_pdu = Mock(sequence=1)
        mock_instance.send_message.return_value = mock_send_pdu

        mock_instance.read_pdu.side_effect = [
            Mock(command="submit_sm_resp", message_id=b"test_message_id"),
            Mock(
                command="query_sm_resp",
                message_state=3,  # EXPIRED
                error_code=None,
                command_status=None,
            ),
        ]

        # Отправляем сообщение
        send_result = self.client.send_sms("+79991234567", "Test message")
        expected_send_result = {
            "status": "success",
            "messages": [{"sequence": 1, "message_id": "test_message_id"}],
            "parts_count": 1,
        }
        self.assertEqual(send_result, expected_send_result)
        message_id = send_result["messages"][0]["message_id"]

        # Проверяем статус
        status_result = self.client.sms_status(message_id)
        expected_status = {"message_id": "test_message_id", "status": "expired", "error_code": None, "final": True}
        self.assertEqual(status_result, expected_status)

    @patch("smpplib.client.Client")
    def test_timeout(self, mock_client):
        """Тест таймаута при подключении."""
        mock_instance = Mock()
        mock_instance.connect.side_effect = TimeoutError("Connection timeout")
        mock_client.return_value = mock_instance

        client = SmsAeroSmpp(login="test_login", password="test_password", timeout=0.1)._test_mode()

        with self.assertRaises(SmsAeroConnectionError) as context:
            client.send_sms("+79991234567", "Test message")

        self.assertIn("белый список", str(context.exception))
        mock_instance.connect.assert_called_once()

    @patch("smpplib.client.Client")
    def test_check_connection_success(self, mock_client):
        """Тест успешной проверки подключения."""
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        result = self.client.check_connection()
        self.assertTrue(result)
        mock_instance.connect.assert_called_once()
        mock_instance.bind_transceiver.assert_called_once()

    @patch("smpplib.client.Client")
    def test_check_connection_failure(self, mock_client):
        """Тест неудачной проверки подключения."""
        mock_instance = Mock()
        mock_instance.connect.side_effect = smpplib.exceptions.ConnectionError("Connection refused")
        mock_client.return_value = mock_instance

        result = self.client.check_connection()
        self.assertFalse(result)
        mock_instance.connect.assert_called_once()

    @patch("smpplib.client.Client")
    def test_retry_mechanism(self, mock_client):
        """Тест механизма повторных попыток."""
        # Создаем клиент с включенными ретраями (без _test_mode!)
        client = SmsAeroSmpp(
            login="test_login", password="test_password", retry_max_attempts=3, retry_delay=0.1, retry_backoff=1.0
        )

        mock_instance = Mock()
        mock_instance.connect.side_effect = [
            smpplib.exceptions.ConnectionError("First attempt"),
            smpplib.exceptions.ConnectionError("Second attempt"),
            None,  # Успешное подключение на третьей попытке
        ]
        mock_client.return_value = mock_instance

        # Настраиваем мок для PDU ответа
        mock_resp_pdu = Mock()
        mock_resp_pdu.command = "submit_sm_resp"
        mock_resp_pdu.message_id = b"test_message_id"
        mock_instance.read_pdu.return_value = mock_resp_pdu

        # Настраиваем sequence для PDU отправки
        mock_send_pdu = Mock()
        mock_send_pdu.sequence = 1
        mock_instance.send_message.return_value = mock_send_pdu

        result = client.send_sms("+79991234567", "Test message")
        expected_result = {
            "status": "success",
            "messages": [{"sequence": 1, "message_id": "test_message_id"}],
            "parts_count": 1,
        }

        self.assertEqual(result, expected_result)
        self.assertEqual(mock_instance.connect.call_count, 3)

    @patch("smpplib.client.Client")
    def test_no_retry(self, mock_client):
        """Тест работы без ретраев."""
        client = SmsAeroSmpp(
            login="test_login",
            password="test_password",
            retry_max_attempts=1,  # Отключаем ретраи
        )

        mock_instance = Mock()
        mock_instance.connect.side_effect = smpplib.exceptions.ConnectionError("Connection error")
        mock_client.return_value = mock_instance

        with self.assertRaises(SmsAeroConnectionError):
            client.send_sms("+79991234567", "Test message")

        self.assertEqual(mock_instance.connect.call_count, 1)  # Только одна попытка


class TestValidators(unittest.TestCase):
    """Тесты для функций валидации."""

    def test_validate_phone(self):
        """Тест валидации номера телефона."""
        # Правильные номера
        self.assertEqual(validate_phone("+79991234567"), "+79991234567")

        # Неправильные номера
        with self.assertRaises(ValueError):
            validate_phone("invalid")
        with self.assertRaises(ValueError):
            validate_phone("+7999")

    def test_validate_ip(self):
        """Тест валидации IP адреса."""
        # Правильные IP
        self.assertEqual(validate_ip("127.0.0.1"), "127.0.0.1")
        self.assertEqual(validate_ip("192.168.1.1"), "192.168.1.1")

        # Неправильные IP
        with self.assertRaises(ValueError):
            validate_ip("256.256.256.256")
        with self.assertRaises(ValueError):
            validate_ip("invalid")

    def test_validate_port(self):
        """Тест валидации номера порта."""
        # Правильные порты
        self.assertEqual(validate_port(1), 1)
        self.assertEqual(validate_port(65535), 65535)

        # Неправильные порты
        with self.assertRaises(ValueError):
            validate_port(0)
        with self.assertRaises(ValueError):
            validate_port(65536)

    def test_validate_message(self):
        """Тест валидации текста сообщения."""
        # Правильные сообщения
        self.assertEqual(validate_message("Test"), "Test")
        self.assertEqual(validate_message("А" * 960), "А" * 960)

        # Неправильные сообщения
        with self.assertRaises(ValueError):
            validate_message("")
        with self.assertRaises(ValueError):
            validate_message("А" * 961)


if __name__ == "__main__":
    unittest.main()
