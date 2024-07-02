# extensions.py
import requests
import json


class APIException(Exception):
    """Исключение для обработки ошибок, связанных с API запросами."""

    def __init__(self, message):
        self.message = message


class CurrencyConverter:
    """Класс для конвертации валют и криптовалют."""

    # Список топовых мировых валют
    fiat_currencies = ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'SEK', 'NZD']
    # Список популярных криптовалют
    crypto_currencies = ['bitcoin', 'ethereum', 'tether', 'binancecoin', 'usd-coin', 'ripple', 'cardano', 'dogecoin',
                         'solana', 'polkadot']

    @staticmethod
    def get_fiat_price(base, quote, amount):
        """
        Получает стоимость указанного количества базовой фиатной валюты в указанной фиатной валюте.
        :param base: Имя базовой валюты (например, 'USD')
        :param quote: Имя валюты, в которой нужно узнать цену (например, 'EUR')
        :param amount: Количество базовой валюты
        :return: Стоимость базовой валюты в указанной валюте
        """
        url = f'https://api.exchangerate-api.com/v4/latest/{base}'
        response = requests.get(url)
        data = response.json()

        if 'rates' not in data:
            raise APIException('Ошибка при запросе курса фиатной валюты.')

        rates = data['rates']
        if quote not in rates:
            raise APIException(f'Валюта {quote} не найдена в API.')

        rate = rates[quote]
        return rate * float(amount)

    @staticmethod
    def get_crypto_price(base, quote, amount):
        """
        Получает стоимость указанного количества базовой криптовалюты в указанной фиатной валюте.
        :param base: Имя базовой криптовалюты (например, 'bitcoin')
        :param quote: Имя валюты, в которой нужно узнать цену (например, 'USD')
        :param amount: Количество базовой криптовалюты
        :return: Стоимость базовой криптовалюты в указанной валюте
        """
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={base}&vs_currencies={quote}'
        response = requests.get(url)
        data = response.json()

        if base not in data or quote not in data[base]:
            raise APIException('Ошибка при запросе курса криптовалюты.')

        rate = data[base][quote]
        return rate * float(amount)

    @staticmethod
    def get_price(base, quote, amount):
        """
        Получает стоимость указанного количества базовой валюты в указанной валюте.
        :param base: Имя базовой валюты (например, 'USD' или 'bitcoin')
        :param quote: Имя валюты, в которой нужно узнать цену (например, 'EUR' или 'USD')
        :param amount: Количество базовой валюты
        :return: Стоимость базовой валюты в указанной валюте
        """
        base = base.lower()
        quote = quote.lower()

        if base in CurrencyConverter.crypto_currencies:
            return CurrencyConverter.get_crypto_price(base, quote, amount)
        elif base.upper() in CurrencyConverter.fiat_currencies:
            return CurrencyConverter.get_fiat_price(base.upper(), quote.upper(), amount)
        else:
            raise APIException(f'Валюта {base} не поддерживается.')


class CurrencyHandler:
    """Класс для обработки запросов пользователя и подготовки ответа."""

    @staticmethod
    def handle(message):
        """
        Обрабатывает сообщение пользователя, извлекает параметры и конвертирует валюту.
        :param message: Сообщение пользователя
        :return: Ответ с результатом конвертации или сообщением об ошибке
        """
        try:
            params = message.text.split()
            if len(params) != 3:
                raise APIException('Неправильное количество параметров.')

            base, quote, amount = params
            amount = float(amount)
            if amount <= 0:
                raise APIException('Количество валюты должно быть положительным числом.')

            result = CurrencyConverter.get_price(base.lower(), quote.lower(), amount)
            return f'{amount} {base.upper()} = {result:.2f} {quote.upper()}'
        except ValueError:
            raise APIException('Количество валюты должно быть числом.')
        except APIException as e:
            return f'Ошибка: {e.message}'