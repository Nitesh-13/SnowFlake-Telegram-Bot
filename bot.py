import telebot
import ast
import os
import requests
import time
import urllib
from telebot import types
from uuid import uuid4

bot = telebot.TeleBot("BOT_API_HERE")

stringList = {"1": "Nitesh", "2": "Yash", "3": "Kiran", "4": "Rohit"}
rollcall = []
submitstatus = False
crossIcon = u"\u2705"
tickIcon = u"\u2610"
warningIcon = u"\u26A0"

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def get_fact():
    contents = requests.get('https://uselessfacts.jsph.pl/random.json?language=en').json()
    fact = contents['text']
    return fact


def sociallinks():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text="⚇ Github", url="https://github.com/Nitesh-13"))
    return markup


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
            text=crossIcon+" Attendance Submitted", callback_data="submit"))
    else:
        markup.add(types.InlineKeyboardButton(
            text="Submit Attendance", callback_data="submit"))

    return markup


@bot.message_handler(commands=['photo'])
def handle_command_adminwindow(message):
    url = get_url()
    bot.send_photo(message.chat.id, url)

@bot.message_handler(commands=['fact'])
def handle_command_adminwindow(message):
    fact = get_fact()
    bot.send_message(chat_id=message.chat.id, text=fact)

@bot.message_handler(commands=['startatt'])
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Here are the Roll Calls of the Students",
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')


@bot.message_handler(commands=['showatt'])
def handle_command_adminwindow(message):
    present = "Roll No's Present are : "
    for x in rollcall:
        if rollcall[len(rollcall)-1] == x:
            present = present + x + "."
        else:
            present = present + x + ", "
    bot.reply_to(message, present)


@bot.message_handler(commands=['clearatt'])
def handle_command_adminwindow(message):
    global submitstatus
    submitstatus = False
    rollcall.clear()
    cleared = 'Attendance List cleared, now you can start new attendance..\nTo do so, use the following command : \n/startatt'
    bot.reply_to(message, cleared)


@bot.message_handler(commands=['start'])
def handle_command_adminwindow(message):
    username = message.chat.first_name
    bot.send_message(chat_id=message.chat.id,
                     text="Welcome "+username + " 😇" +
                     "!\nI am ❄️ <b>SnowFlake</b>, an Attendance Bot 🤖 made by <i>Nitesh</i>.\n\nHere are few commands to get started with...\n/start - Display Welcome message\n/startatt - Start Attendance\n/showatt - Show Attendance\n/clearatt - Clear Attendance",
                     parse_mode='HTML')


@bot.message_handler(commands=['socialprofiles'])
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="👨‍💻 Social Profiles : ",
                     reply_markup=sociallinks(),
                     parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global submitstatus
    if (call.data.startswith("['value'")):
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text="Students name is " + valueFromCallBack + " and Roll No. is " + keyFromCallBack)

    if (call.data.startswith("['key'")) and submitstatus == False:
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

    if (call.data.startswith("['key'")) and submitstatus == True:
        bot.send_message(chat_id=call.message.chat.id,
                         text=warningIcon+" Attendance already submitted.\n\nUse the following command to clear attendance and retake it :\n/clearatt",
                         parse_mode='HTML')

    if (call.data == 'submit'):
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
                             text=warningIcon+" Attendance already submitted.\n\nUse the following command to clear attendance and retake it :\n/clearatt",
                             parse_mode='HTML')


while True:
    try:
        print("Running")
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)
