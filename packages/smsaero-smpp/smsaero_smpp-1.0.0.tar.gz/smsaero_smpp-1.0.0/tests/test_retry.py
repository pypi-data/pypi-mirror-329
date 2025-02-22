"""
Тесты для механизма повторных попыток.
"""

import unittest
from unittest.mock import Mock

from smsaero_smpp.errors import SmsAeroConnectionError
from smsaero_smpp.retry import retry


class TestRetry(unittest.TestCase):
    """Тесты для декоратора retry."""

    def test_successful_execution(self):
        """Тест успешного выполнения функции."""
        mock_func = Mock(return_value="success")
        decorated = retry()(mock_func)

        result = decorated()

        self.assertEqual(result, "success")
        mock_func.assert_called_once()

    def test_retry_on_error(self):
        """Тест повторных попыток при ошибке."""
        mock_func = Mock(side_effect=[SmsAeroConnectionError(), SmsAeroConnectionError(), "success"])
        decorated = retry(max_attempts=3, delay=0.1)(mock_func)

        result = decorated()

        self.assertEqual(result, "success")
        self.assertEqual(mock_func.call_count, 3)

    def test_max_attempts_exceeded(self):
        """Тест превышения максимального количества попыток."""
        mock_func = Mock(side_effect=SmsAeroConnectionError("Test error"))
        decorated = retry(max_attempts=3, delay=0.1)(mock_func)

        with self.assertRaises(SmsAeroConnectionError):
            decorated()

        self.assertEqual(mock_func.call_count, 3)
