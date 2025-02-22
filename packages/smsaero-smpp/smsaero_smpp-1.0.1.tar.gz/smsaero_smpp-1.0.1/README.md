# Python библиотека для отправки SMS сообщений через SMPP протокол на сервис SMS Aero 

[![PyPI version](https://badge.fury.io/py/smsaero-smpp.svg)](https://badge.fury.io/py/smsaero-smpp)
[![Python Versions](https://img.shields.io/pypi/pyversions/smsaero-smpp.svg)](https://pypi.org/project/smsaero-smpp/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](MIT-LICENSE)

## Установка с использованием пакетного менеджера pip:

```bash
pip install smsaero-smpp
```

## Пример использования в коде:

Логин и пароль Вы можете добавить в настройках аккаунта, включая статический IP-адрес
на странице https://smsaero.ru/cabinet/settings/apikey/, в секции "SMPP-доступы".

```python
from smsaero_smpp import SmsAeroSmpp


SMSAERO_USER = 'ваш логин'
SMSAERO_PASS = 'ваш пароль'


def send_sms(phone: str, message: str) -> None:
    """
    Отправка SMS сообщения

    Параметры:
    phone (int): Номер телефона.
    message (str): Содержание SMS сообщения.
    """
    client = SmsAeroSmpp(
        login=SMSAERO_USER,
        password=SMSAERO_PASS,
        source='SMS Aero',
    )
    
    try:
        result = client.send_sms(phone, message)
        print(result)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
    except ConnectionError as e:
        print(f"Ошибка подключения: {e}")


if __name__ == '__main__':
    send_sms('+79038805678', 'Привет, мир!')
```

## Использование в командной строке (полезно для автоматизации):

```bash
export SMSAERO_USER="ваш логин"
export SMSAERO_PASS="ваш пароль"

smsaero_smpp_send \
    --login "$SMSAERO_USER" \
    --password "$SMSAERO_PASS" \
    --phone +79038805678 \
    --message 'Привет, мир!' \
    --debug  # опционально для включения подробного логирования
```

## Запуск в Docker (demo):

```bash
docker pull 'smsaero/smsaero_python_smpp:latest'

docker run -it --rm smsaero/smsaero_python_smpp:latest \
    smsaero_smpp_send \
    --login "ваш логин" \
    --password "ваш пароль" \
    --phone +79038805678 \
    --message 'Привет, мир!'
```

## Исключения

* `SmsAeroConnectionError` - исключение при ошибке подключения к SMPP серверу (например, IP не в белом списке)
* `ValueError` - исключение при некорректных входных данных (неверный формат телефона, IP, порта и т.д.)

### Дополнительные параметры командной строки

- `--ip` - IP адрес SMPP сервера (по умолчанию: 82.202.194.38)
- `--port` - Порт SMPP сервера (по умолчанию: 2775)
- `--source` - Имя отправителя (по умолчанию: SMS Aero)

## Особенности

- Поддержка длинных сообщений (до 960 символов)
- Автоматическая валидация номера телефона
- Поддержка международного формата номеров
- Подробное логирование при необходимости

## Требования

- Python 3.6+
- smpplib
- phonenumbers

## Лицензия

MIT License
