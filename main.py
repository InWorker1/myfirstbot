import telebot
from datetime import datetime
from time import sleep
from telebot import types

bot = telebot.TeleBot('5891292416:AAHDoVsvYKOhVmGGNugX3nOFoM-GeYiKOuc')

@bot.message_handler(commands=["start"])    #начальная комманда старта
def start(message):

    inline_markup=types.InlineKeyboardMarkup(row_width=1)
    item=types.InlineKeyboardButton('создай список покупок', callback_data='buy_list_bt')
    item2=types.InlineKeyboardButton('начни следить за временем', callback_data='time_lesson_bt')
    item3=types.InlineKeyboardButton('поставить напоминалку', callback_data='reminder')
    inline_markup.add(item,item2,item3)
    bot.send_message(message.chat.id, 'привет, друг!', reply_markup=inline_markup)
    # bot.register_next_step_handler(message, time_lesson)

@bot.callback_query_handler(func=lambda call: True)       #комманда ответа на кнопку
def callback(call):
    match call.data:
        case 'buy_list_bt':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='перечисляй продукты в одну строку через пробел')
            bot.register_next_step_handler(call.message, list_buy)
        case 'tiem_lesson_bt':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='хорошо я слежу за временем, иди пока отдохни, а я напишу за 3 минуты до урока')
            bot.register_next_step_handler(call.message, time_lesson)
        case 'restart':
            for i in range(count_lb+2):
                bot.delete_message(call.message.chat.id, call.message.message_id - i)
            start(call.message)
        case 'delete':  # callback который отвечает за удаление сообщения бота по нажатию кнопки
            bot.delete_message(call.message.chat.id, call.message.message_id)
        case 'reminder':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='введите что будет сегодня и во сколько это будет')
            bot.register_next_step_handler(call.message, reminder)
        case 'delete_remind':
            time_remind=''
            str_remind=''
            bot.register_next_step_handler(call.message, start)



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
            case 'привет':
                start(message)
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
            case time_remind:
                remind_markup=types.InlineKeyboardMarkup(row_width=1)
                rbt1=types.InlineKeyboardButton('выполнено', callback_data='delete_remind')
                remind_markup.add(rbt1)
                bot.send_message(message.chat.id, f'{str_remind}', reply_markup=remind_markup)


        sleep(60)

def list_buy(message):
    global count_lb
    mes = message.text.split()
    count_lb = 0
    lb_markup = types.InlineKeyboardMarkup(row_width=1)
    lbbt = types.InlineKeyboardButton('удалить из списка', callback_data='delete')
    lb_markup.add(lbbt)
    for i in range(len(mes)):
        if type(mes[i]) == str and mes[i] != '':
            count_lb += 1
            if count_lb == len(mes):
                restart_lb=types.InlineKeyboardButton('вернуться к выбору команды', callback_data='restart')
                lb_markup.add(restart_lb)
                bot.send_message(message.chat.id, f'{count_lb}) {mes[i]}', reply_markup=lb_markup)
                break
            bot.send_message(message.chat.id, f'{count_lb}) {mes[i]}', reply_markup=lb_markup)



def factorial(message):
    cif = int(message.text.strip())
    counter = 1
    for i in range(1, cif + 1):
        counter *= i
    bot.send_message(message.chat.id, f'факториал {cif} равен {counter}')

def reminder(message):
    global time_remind, str_remind
    a=[message.text.split() for i in range(1)]
    time_remind=a[0][-1]
    str_remind=a[0][0]
    print(time_remind, str_remind)
    bot.register_next_step_handler(message, time_lesson)


while True:
    try:
        bot.polling()
    except:
        sleep(15)
