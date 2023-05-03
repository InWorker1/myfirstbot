import telebot
from datetime import datetime
from time import sleep
from telebot import types
from threading import Thread
import texts
import sqlite3
import functools
import parser as pr


def convert_tuple(c_tuple):
    stroka = ''
    for i in c_tuple:
        stroka += i
    return stroka


def edit_tuple(self):
    self = str(self)
    for i in "(''),":
        try:
            self = self.replace(i, '')
        except:
            pass
    try:
        return self
    except:
        return int(self)


bot = telebot.TeleBot('5891292416:AAHDoVsvYKOhVmGGNugX3nOFoM-GeYiKOuc')

time_remind = ' '
str_remind = ' '
dt_now = ' '
tr = ' '
sr = ' '
mes_id = 0
count_lb = 0
tempa = pr.getWeather('intgradus')
veter = pr.getWeather('intwind')

markup_delete = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('удалить', callback_data='delete'))


@bot.message_handler(commands=["start"])  # начальная комманда старта
def start(message):
    # начало работы с базой данных
    connect = sqlite3.connect('users.db')

    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(id INTEGER, remind TEXT, remind_time TEXT)""")
    connect.commit()

    people_id = message.chat.id
    cursor.execute(f'SELECT id FROM login_id WHERE id = {people_id}')
    data_u = cursor.fetchone()
    if data_u is None:
        user_id = message.chat.id
        cursor.execute("INSERT INTO login_id VALUES(?, ?, ?);", (user_id, str_remind, time_remind))
        connect.commit()
    # конец работы с бд

    global mes_id
    mes_id = message.chat.id
    inline_markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('создать список покупок', callback_data='buy_list_bt')
    item2 = types.InlineKeyboardButton('начать следить за временем', callback_data='time_lesson_bt')
    item3 = types.InlineKeyboardButton('поставить напоминалку', callback_data='reminder')
    item4 = types.InlineKeyboardButton('посмотреть курс валют', callback_data='curs')
    inline_markup.add(item, item2, item3, item4)
    bot.send_message(message.chat.id, 'привет, друг! Ты можешь прописать /info, чтобы узнать какие еще есть функции',
                     reply_markup=inline_markup)
    time_tracking()


@bot.message_handler(commands=['delete_id'])
def delete_id(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    people_id = message.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
    connect.commit()


@bot.message_handler(commands=['factorial'])  # Комманда факториал
def start_factorial(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, texts.start_factorial), factorial)


@bot.message_handler(commands=['info'])  # Комманда инвормации
def getinfo(message):
    bot.send_message(message.chat.id, texts.info)


@bot.message_handler(commands=['getweather'])
def getWeather(message):
    bot.send_message(message.chat.id, f'{pr.getWeather("text")} {pr.getWeather("gradus")}. {pr.getWeather("wind")}')
    if (pr.getWeather('intgradus') > 0 and pr.getWeather('intgradus') < 5) and (
            pr.getWeather('intwind') > 3 and pr.getWeather('intwind') < 8):
        bot.send_message(message.chat.id, 'Нужно надеть куртку шапку и если чувствительны к холоду - шарф')
    elif (pr.getWeather('intgradus') >= 12 and pr.getWeather('intgradus') <= 14) and pr.getWeather('intwind') >= 2:
        bot.send_message(message.chat.id, 'На улице тепло, но не очень приятно. Советую одеть на кофту куртку.')
    elif tempa >= 7 and tempa < 12 and veter >= 0 and veter <= 3:
        bot.send_message(message.chat.id, 'Прохладно, легкая куртка')
    elif tempa >=7 and tempa <12 and veter >= 3 and veter <= 6:
        bot.send_message(message.chat.id, 'Прохладно легкая куртка , если чувствительны к холоду шапка')
    elif tempa >= 7 and tempa < 12 and veter >= 6 and veter <= 9:
        bot.send_message(message.chat.id, 'Лучше легкая куртка , лучше надеть вещи с капюшоном или надеть шапку если чувствительны к холоду то взять с собой шарф не помешает')
    elif tempa >= 12 and tempa <= 15 and veter >= 0 and veter <= 9:
        bot.send_message(message.chat.id, 'легкая куртка')
    elif tempa >= 16 and tempa <= 17 and veter >= 0 and veter <= 9:
        bot.send_message(message.chat.id, 'кофта или толстовка , если чувствительны к холоду можно надеть легкую куртку')
    elif tempa >= 17 and tempa <= 20 and veter >= 0 and veter <= 6:
        bot.send_message(message.chat.id, 'кофта или толстовка')
    elif tempa >= 17 and tempa <= 20 and veter >= 6 and veter <= 9:
        bot.send_message(message.chat.id, 'тепло кофта или толстовка с капюшоном если чувствительны к холоду , легкая курткa')
    elif (pr.getWeather('intgradus') == 0) and pr.getWeather('intwind') > 1:
        bot.send_message(message.chat.id, 'Одень, пожалуй, крутку с кофтой. Шапка бы тоже не помешала')


@bot.callback_query_handler(func=lambda call: True)  # комманда ответа на кнопку
def callback(call):
    global count_lb
    match call.data:
        case 'buy_list_bt':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='перечисляй продукты в одну строку через пробел')
            bot.register_next_step_handler(call.message, list_buy)
        case 'time_lesson_bt':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='хорошо я слежу за временем, иди пока отдохни, а я напишу за 3 минуты до урока')
            time_tracking()
        case 'delete_lb':
            for i in range(count_lb + 2):
                bot.delete_message(call.message.chat.id, call.message.message_id - i)
                count_lb -= 1
            start(call.message)
        case 'delete':  # callback который отвечает за удаление сообщения бота по нажатию кнопки
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if count_lb > 0:
                count_lb -= 1
            bot.delete_message(call.message.chat.id, call.message.message_id)
        case 'reminder':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='введите что будет сегодня и во сколько это будет')
            bot.register_next_step_handler(call.message, reminder)
        case 'delete_remind':
            for i in range(4):
                bot.delete_message(call.message.chat.id, call.message.message_id - i)
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE login_id SET remind_time = '{None}' WHERE id = '{mes_id}'")
            conn.commit()
            start(call.message)
        case 'curs':
            curs_money(call.message)


@bot.message_handler(content_types=['text'])  # ответы и шаги после определенного сообщения
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


def time_tracking():
    global dt_now, mes_id, sr
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    print('все работает')
    while True:
        remind_time = cursor.execute("SELECT remind_time FROM login_id")
        dt_now = datetime.now().strftime('%H:%M')
        match str(dt_now):
            case '9:28':
                bot.send_message(mes_id, 'пора на урок')
            case '10:33':
                bot.send_message(mes_id, 'пора на урок')
            case '11:28':
                bot.send_message(mes_id, 'пора на урок')
            case '12:33':
                bot.send_message(mes_id, 'пора на урок')
            case '13:38':
                bot.send_message(mes_id, 'пора на урок')
            case '14:33':
                bot.send_message(mes_id, 'пора на урок')
            case '15:20':
                bot.send_message(mes_id, 'иди отдохни домой дружок)')
                break
        for tt in remind_time:
            tt = convert_tuple(tt)
            for i in "(''),":
                tt = tt.replace(f"{i}", '')
            if str(dt_now) == tt:
                mes_id = cursor.execute(f"SELECT id FROM login_id WHERE remind_time = '{tt}'")
                mes_id = edit_tuple(functools.reduce(lambda x: int(x), mes_id))
                sr = edit_tuple(cursor.execute(f"SELECT remind FROM login_id WHERE id = {mes_id}").fetchone())
                remind_markup = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton('выполнено', callback_data='delete_remind'))
                bot.send_message(mes_id, f'{sr}', reply_markup=remind_markup)
        print(f'проверка времени работает стабильно: {dt_now}')
        sleep(60)
    print('проверка времени закончила работу')


def list_buy(message):
    global count_lb
    mes = message.text.split()
    count_lb = 0
    for i in range(len(mes)):
        if type(mes[i]) == str and mes[i] != '':
            count_lb += 1
            if count_lb == len(mes):
                restart_lb = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton('вернуться к выбору комманды', callback_data='delete_lb'))
                bot.send_message(message.chat.id, f'{count_lb}) {mes[i]}', reply_markup=restart_lb)
                break
            bot.send_message(message.chat.id, f'{count_lb}) {mes[i]}', reply_markup=markup_delete)


def factorial(message):
    cif = int(message.text.strip())
    counter = 1
    for i in range(1, cif + 1):
        counter *= i
    bot.register_next_step_handler(
        bot.send_message(message.chat.id, f'факториал {cif} равен {counter}', reply_markup=markup_delete), start)


def reminder(message):
    a = message.text.split()
    global time_remind, str_remind, mes_id, tr, sr
    mes_id = message.chat.id
    time_remind = a[-1]
    str_remind = a[:-1]
    str_remind = ' '.join(str_remind)
    print(time_remind, str_remind)
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"""UPDATE login_id SET remind = '{str_remind}' WHERE id = '{mes_id}';""")
    cursor.execute(f"""UPDATE login_id SET remind_time = '{time_remind}' WHERE id = '{mes_id}'""")
    connect.commit()

    tr = str(cursor.execute(f"SELECT remind_time FROM login_id WHERE id = '{message.chat.id}'").fetchone())
    sr = str(cursor.execute(f"SELECT remind FROM login_id WHERE id = '{message.chat.id}'").fetchone())
    for i in "(''),":
        tr = tr.replace(f"{i}", '')
        sr = sr.replace(f"{i}", '')
    remind_markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('удалить напоминание', callback_data='delete_remind'))
    bot.send_message(message.chat.id, text=f'отлично в {tr} будет отправленно сообщение: {sr}',
                     reply_markup=remind_markup)
    # Thread(target=time_lesson).start()


def curs_money(message):
    bot.send_message(message.chat.id, f'1 доллар на данный момент равен: {pr.getDollar()}', reply_markup=markup_delete)
    bot.send_message(message.chat.id, f'1 евро на данный момент равен: {pr.getEuro()}', reply_markup=markup_delete)


# def proverka():
#     while True:
#         print(count_lb)
#         sleep(10)
# Thread(target=proverka).start()

while True:
    try:
        bot.polling()
    except:
        sleep(15)
