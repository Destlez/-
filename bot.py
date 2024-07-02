# bot.py
import telebot
from config import TOKEN
from extensions import CurrencyHandler, APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Обрабатывает команду /start и /help, отправляет приветственное сообщение с инструкциями.
    """
    text = (
        "Привет! Я бот для конвертации валют и криптовалют. "
        "Для получения стоимости валюты отправьте сообщение в формате:\n"
        "<имя валюты> <в какой валюте узнать цену> <количество>\n"
        "Пример: EUR USD 100\n"
        "Доступные команды:\n"
        "/start или /help - вывод инструкции\n"
        "/values - список доступных валют\n"
        "/cryptos - список доступных криптовалют"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def send_values(message):
    """
    Обрабатывает команду /values, отправляет список доступных фиатных валют.
    """
    text = "Доступные валюты:\n" + "\n".join(CurrencyConverter.fiat_currencies)
    bot.reply_to(message, text)

@bot.message_handler(commands=['cryptos'])
def send_cryptos(message):
    """
    Обрабатывает команду /cryptos, отправляет список доступных криптовалют.
    """
    text = "Доступные криптовалюты:\n" + "\n".join(CurrencyConverter.crypto_currencies)
    bot.reply_to(message, text)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    """
    Обрабатывает сообщения пользователей, которые не являются командами, выполняет конвертацию валют.
    """
    try:
        response = CurrencyHandler.handle(message)
        bot.reply_to(message, response)
    except APIException as e:
        bot.reply_to(message, f'Ошибка: {e.message}')

if __name__ == '__main__':
    bot.polling(none_stop=True)