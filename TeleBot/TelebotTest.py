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

        if quote not in keys.keys():
            for _ in keys.keys():
                if quote[0:3] == _[0:3] or quote[0] == _[0] and quote[-1] == _[-1]:
                    quote = _
            bot.reply_to(message, f'Не верный ввод данных возможно вы имели ввиду {quote}')


        if base not in keys.keys():
            for _ in keys.keys():
                if base[0:3] == _[0:3] or base[0] == _[0] and base[-1] == _[-1]:
                    base = _
            bot.reply_to(message, f'Не верный ввод данных возможно вы имели ввиду {base}')

        total_price = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {keys[quote]} в {keys[base]} = {total_price*int(amount)} {keys[base]}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)