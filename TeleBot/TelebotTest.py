import telebot
from classExcept import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message):
    text = 'Чтоб начать работу, введите команду боту в следующем формате: ' \
           '\n< имя валюты >' \
           '\n< в какую валюту перевести >' \
           '\n< количество переводимой валюты >' \
           '\n  ___________________________' \
           '\n                  Пример: ' \
           '\n\n          биткоин доллар 2 ' \
           '  ___________________________\n' \
           '\n< Увидеть список всех доступных валют /values >'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
       text = f'{text}\n - {key}'
    bot.reply_to(message, text)

@bot.message_handler()
def convert(message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertionException('Не верное кол-во параметров')

        quote, base, amount = values
        total_price = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {keys[quote]} в {keys[base]} = {total_price*int(amount)} {keys[base]}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)