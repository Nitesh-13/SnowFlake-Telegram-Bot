import telebot
import ast
import time
from telebot import types

bot = telebot.TeleBot("BOT_API_HERE")

stringList = {"1": "Nitesh", "2": "Yash", "3": "Kiran", "4": "Rohit"}
rollcall = []
submitstatus = False
crossIcon = u"\u2705"
tickIcon = u"\u2610"


def makeKeyboard():
    markup = types.InlineKeyboardMarkup()
    print(rollcall)
    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=key+". "+value, callback_data="['value', '" + value + "', '" + key + "']"),
                   types.InlineKeyboardButton(text=tickIcon, callback_data="['key', '" + key + "']"))
    markup.add(types.InlineKeyboardButton(
        text="Submit Attendance", callback_data="submit"))

    return markup


def editKeyboard(rollno):
    markup = types.InlineKeyboardMarkup()
    print(rollcall)
    for key, value in stringList.items():
        if key in rollcall:
            add = True
        else:
            add = False

        if (key == rollno and add == True) or add == True:
            markup.add(types.InlineKeyboardButton(text=key+". "+value, callback_data="['value', '" + value + "', '" + key + "']"),
                       types.InlineKeyboardButton(text=crossIcon, callback_data="['key', '" + key + "']"))
        else:
            markup.add(types.InlineKeyboardButton(text=key+". "+value, callback_data="['value', '" + value + "', '" + key + "']"),
                       types.InlineKeyboardButton(text=tickIcon, callback_data="['key', '" + key + "']"))
    if rollno == -1 or submitstatus == True:
        markup.add(types.InlineKeyboardButton(
            text= crossIcon+" Attendance Submitted", callback_data="submit"))
    else:
        markup.add(types.InlineKeyboardButton(
            text="Submit Attendance", callback_data="submit"))

    return markup


@bot.message_handler(commands=['start'])
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Here are the Roll Calls of the Students",
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if (call.data.startswith("['value'")):
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text="Students name is " + valueFromCallBack + " and Roll No. is " + keyFromCallBack)

    if (call.data.startswith("['key'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]

        if keyFromCallBack in rollcall:
            rollcall.remove(keyFromCallBack)
        else:
            rollcall.append(keyFromCallBack)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the Roll Calls of the Students",
                              message_id=call.message.message_id,
                              reply_markup=editKeyboard(keyFromCallBack),
                              parse_mode='HTML')

    if (call.data == 'submit'):
        global submitstatus
        if submitstatus == False:
            submitstatus = True
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  text="Here are the Roll Calls of the Students",
                                  message_id=call.message.message_id,
                                  reply_markup=editKeyboard(-1),
                                  parse_mode='HTML')
            bot.send_message(chat_id=call.message.chat.id,
                             text="Attendance submitted Successfully",
                             parse_mode='HTML')
            present = "Roll No's Present are : "
            for x in rollcall:
                if rollcall[len(rollcall)-1] == x:
                    present = present + x + "."
                else:
                    present = present + x + ", "
            bot.send_message(chat_id=call.message.chat.id,
                             text=present,
                             parse_mode='HTML')

        else:
            bot.send_message(chat_id=call.message.chat.id,
                             text="Attendance already submitted",
                             parse_mode='HTML')


while True:
    try:
        print("Running")
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)
