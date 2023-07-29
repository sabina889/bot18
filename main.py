import telebot
from config import keys, TOKEN
from extensions import ConvertionException, TelegramBotConventer

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Добро пожаловать в TelegramBot по конвертации волюты! \nПомощь по боту  "/help"'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать напишите сообщение через пробел! \n1.Имя валюты, цену которой хотите узнать ' \
           '\n2.Имя валюты, по которой будем конвертировать ' \
           '\n3.Количество первой валюты \nСписок всех доступных валют:  "/values"'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException(f'Cлишком много параметров.')
        quote, base, amount = values
        total_base = TelegramBotConventer.convert(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду  \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()