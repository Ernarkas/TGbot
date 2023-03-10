import telebot
import traceback

from config import *
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = """Вас приветствует ШиракКурс! С помощью команды /values выберите доступные валюты.
    
Выберите из списка валюту, которую Вы хотите конвертировать, затем "денежку", к эквиваленту которой 
хотите привести первую, а также интересующую сумму.

Например: доллар тенге 8500"""

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) !=3:
            raise APIException("Необходимо ввести три параметра")

        answer = Converter.get_price(*values)

    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.infinity_polling()
