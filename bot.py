import telebot
import ast
import time
from telebot import types

bot = telebot.TeleBot("BOT_API_HERE")

stringList = {"1": "Nitesh", "2": "Yash", "3": "Kiran", "4": "Rohit"}
rollcall = []
crossIcon = u"\u274C"
tickIcon = u"\u2705"


def makeKeyboard():
    markup = types.InlineKeyboardMarkup()
    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=value, callback_data="['value', '" + value + "', '" + key + "']"),
                   types.InlineKeyboardButton(text=tickIcon, callback_data="['key', '" + key + "']"))

    return markup


def editKeyboard(rollno):
    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        for no in rollcall:
            if no == key:
                add = True
            else:
                add = False

        if key == rollno or add == True:
            markup.add(types.InlineKeyboardButton(text=value, callback_data="['value', '" + value + "', '" + key + "']"),
                       types.InlineKeyboardButton(text=crossIcon, callback_data="['key', '" + key + "']"))
        else:
            markup.add(types.InlineKeyboardButton(text=value, callback_data="['value', '" + value + "', '" + key + "']"),
                       types.InlineKeyboardButton(text=tickIcon, callback_data="['key', '" + key + "']"))

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
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(
            f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text="You Selected " + valueFromCallBack + " and Roll No. is " + keyFromCallBack)

    if (call.data.startswith("['key'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        rollcall.append(keyFromCallBack)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the Roll Calls of the Students",
                              message_id=call.message.message_id,
                              reply_markup=editKeyboard(keyFromCallBack),
                              parse_mode='HTML')


while True:
    try:
        print("Running")
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)
