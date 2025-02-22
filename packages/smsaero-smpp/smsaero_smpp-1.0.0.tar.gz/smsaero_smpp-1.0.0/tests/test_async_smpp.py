"""
Тесты для асинхронного SMPP клиента.
"""

import unittest
from unittest.mock import patch
import asyncio

from smsaero_smpp import AsyncSmsAeroSmpp


class TestAsyncSmsAeroSmpp(unittest.TestCase):
    """Тесты для класса AsyncSmsAeroSmpp."""

    def setUp(self):
        """Инициализация тестового клиента."""
        self.client = AsyncSmsAeroSmpp(login="test_login", password="test_password")

    @patch("smsaero_smpp.smpp.SmsAeroSmpp.send_sms")
    def test_send_sms(self, mock_send):
        """Тест асинхронной отправки SMS."""
        mock_send.return_value = {"status": "success", "messages": [], "parts_count": 1}

        async def test():
            result = await self.client.send_sms("+79991234567", "Test message")
            self.assertEqual(result["status"], "success")

        asyncio.run(test())
        mock_send.assert_called_once()

    @patch("smsaero_smpp.smpp.SmsAeroSmpp.sms_status")
    def test_sms_status(self, mock_status):
        """Тест асинхронной проверки статуса."""
        mock_status.return_value = {"message_id": "test_id", "status": "delivered", "error_code": None, "final": True}

        async def test():
            result = await self.client.sms_status("test_id")
            self.assertEqual(result["status"], "delivered")

        asyncio.run(test())
        mock_status.assert_called_once()
