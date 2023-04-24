import telebot
from datetime import datetime
from time import sleep
from telebot import types
bot = telebot.TeleBot('токен')
# from KeyBoard import markup


@bot.message_handler(commands=["start"])    #начальная комманда старта
def start(message):
    markup=types.InlineKeyboardMarkup(row_width=1)
    item=types.InlineKeyboardButton('создай список покупок', callback_data='buy_list_bt')
    markup.add(item)
    bot.send_message(message.chat.id, 'привет, друг!', reply_markup=markup)
    # bot.register_next_step_handler(message, time_lesson)

@bot.callback_query_handler(func=lambda call: True)       #комманда ответа на кнопку
def callback(call):
    if call.message:
        if call.data=='buy_list_bt':
            bot.send_message(call.message.chat.id, 'перечисляй продукты в одну строку через пробел')
            bot.register_next_step_handler(call.message, list_buy)

@bot.message_handler(content_types=['text'])      #ответы и шаги после определенного сообщения
def handler_text(message):
    try:
        match message.text.strip().lower():
            case 'создай список покупок':
                bot.send_message(message.chat.id, 'отлично! начинай перечислять продукты в одну строку!!')
                bot.register_next_step_handler(message, list_buy)
            case 'факториал':
                bot.send_message(message.chat.id, 'напиши число')
                bot.register_next_step_handler(message, factorial)
    except:
        bot.send_message(message.chat.id, 'не понял вас. посмотрите комманды и повторите, что хотели мне сказать')


def time_lesson(message):        
    global dt_now
    while True:
        dt_now = datetime.now().strftime('%H:%M')
        match str(dt_now):
            case '9:28':
                bot.send_message(message.chat.id, 'пора на урок')
            case '10:33':
                bot.send_message(message.chat.id, 'пора на урок')
            case '11:28':
                bot.send_message(message.chat.id, 'пора на урок')
            case '12:33':
                bot.send_message(message.chat.id, 'пора на урок')
            case '13:38':
                bot.send_message(message.chat.id, 'пора на урок')
            case '14:33':
                bot.send_message(message.chat.id, 'пора на урок')
            case '15:20':
                bot.send_message(message.chat.id, 'иди отдохни домой дружок)')

        sleep(60)


def list_buy(message):
    mes = message.text.split()
    count = 0
    for i in mes:
        if type(i) == str and i != '':
            count += 1
            bot.send_message(message.chat.id, f'{count}) {i}')

def factorial(message):
    cif = int(message.text.strip())
    counter = 1
    for i in range(1, cif + 1):
        counter *= i
    bot.send_message(message.chat.id, f'{counter}')


while True:
    try:
        bot.polling()
    except:
        sleep(15)
