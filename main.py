import telebot
from datetime import datetime
from time import sleep

bot=telebot.TeleBot('5540761456:AAHbhGv1J1dpV3ygCCmGCAncrYam05gdE-s')

@bot.message_handler(commands=["start"])

def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')
    bot.register_next_step_handler(m, time_lesson)


@bot.message_handler(content_types=['text'])

def handler_text(message):
    if message.text.strip() == 'создай список покупок':
        bot.send_message(message.chat.id, 'отлично! начинай перечислять продукты в одну строку!!')
        bot.register_next_step_handler(message, list_buy)
    elif message.text.strip()=='факториал':
        bot.send_message(message.chat.id, 'напиши число')
        bot.register_next_step_handler(message, factorial)

def time_lesson(message):
    global dt_now
    while True:
        dt_now=datetime.now().strftime('%H:%M')
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
    mes=message.text.split()
    count=0
    for i in mes:
        if type(i)==str and i!='':
            count+=1
            bot.send_message(message.chat.id, f'{count}) {i}')

def factorial(message):
    cif=int(message.text.strip())
    counter=1
    for i in range(1,cif+1):
        counter*=i
    bot.send_message(message.chat.id, f'{counter}')

while True:
    try:
        bot.polling()
    except:
        sleep(15)
