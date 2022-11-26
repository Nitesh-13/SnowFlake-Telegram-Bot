import telebot
import ast
import os
import requests
import mysql.connector
import time
import urllib

from telebot import types
from uuid import uuid4

import userFunc
import inlines
import fun

bot = telebot.TeleBot("BOT_API_HERE")
stud_db = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

sql_query = stud_db.cursor()
sql_query.execute("SELECT rollId,name FROM studentData")
result = sql_query.fetchall()

stringList = {}
user = {}
submitstatus = {}
for names in result :
    stringList.update({str(names[0]):names[1]})

# submitstatus = False
warningIcon = u"\u26A0"



#Message Handlers
@bot.message_handler(commands=['photo'])
def handle_command_adminwindow(message):
    print("Photo sent")
    url = fun.get_url()
    bot.send_photo(message.chat.id, url)

@bot.message_handler(commands=['fact'])
def handle_command_adminwindow(message):
    print("fact sent")
    fact = fun.get_fact()
    bot.send_message(chat_id=message.chat.id, text=fact)


@bot.message_handler(commands=['startatt'])
def handle_command_adminwindow(message):
    userid = message.from_user.id
    userstatus = userFunc.checkIfExist(userid, user,submitstatus)
    
    bot.send_message(chat_id=message.chat.id,
                     text="Here are the Roll Calls of the Students",
                     reply_markup=inlines.makeKeyboard(stringList,userid),
                     parse_mode='HTML')


@bot.message_handler(commands=['showatt'])
def handle_command_adminwindow(message):
    userid = message.from_user.id
    userstatus = userFunc.checkIfExist(userid, user,submitstatus)
    user[str(userid)].sort()
    present = "Roll No's Present are : "
    present = userFunc.showRollCall(userid, user, present)
    bot.reply_to(message, present)


@bot.message_handler(commands=['clearatt'])
def handle_command_adminwindow(message):
    userid = message.from_user.id
    userstatus = userFunc.checkIfExist(userid, user,submitstatus)
    submitstatus[str(userid)] = False
    userFunc.resetRollCall(userid, user)
    cleared = 'Attendance List cleared, now you can start new attendance..\nTo do so, use the following command : \n/startatt'
    bot.reply_to(message, cleared)


@bot.message_handler(commands=['start'])
def handle_command_adminwindow(message):
    username = message.chat.first_name
    userid = message.from_user.id
    userstatus = userFunc.checkIfExist(userid, user,submitstatus)
    if userstatus == 1 :
        print("Existing User")
    elif userstatus == 0:
        print("New User")
    bot.send_message(chat_id=message.chat.id,
                     text="Welcome "+username + " 😇" +
                     "!\nI am ❄️ <b>SnowFlake</b>, an Attendance Bot 🤖 made by <i>Nitesh</i>.\n\nHere are few commands to get started with...\n/start - Display Welcome message\n/startatt - Start Attendance\n/showatt - Show Attendance\n/clearatt - Clear Attendance",
                     parse_mode='HTML')


@bot.message_handler(commands=['socialprofiles'])
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="👨‍💻 Social Profiles : ",
                     reply_markup=inlines.sociallinks(),
                     parse_mode='HTML')




#Callback Query Handler
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    userid = 0
    if (call.data.startswith("['key'")):
        userid = ast.literal_eval(call.data)[2]

    if (call.data.startswith("['value'")):
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        userid = ast.literal_eval(call.data)[3]
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text="Students name is " + valueFromCallBack + " and Roll No. is " + keyFromCallBack)

    if (call.data.startswith("['key'")) and submitstatus[str(userid)] == False:
        keyFromCallBack = ast.literal_eval(call.data)[1]
        if keyFromCallBack in user[str(userid)]:
            user[str(userid)].remove(keyFromCallBack)
        else:
            user[str(userid)].append(keyFromCallBack)
        rollcall = user[str(userid)]
        status = submitstatus[str(userid)]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the Roll Calls of the Students",
                              message_id=call.message.message_id,
                              reply_markup=inlines.editKeyboard(keyFromCallBack,stringList,rollcall,status,userid),
                              parse_mode='HTML')
        user[str(userid)].sort()

    if (call.data.startswith("['key'")) and submitstatus[str(userid)] == True:
        bot.send_message(chat_id=call.message.chat.id,
                         text=warningIcon+" Attendance already submitted.\n\nUse the following command to clear attendance and retake it :\n/clearatt",
                         parse_mode='HTML')

    if (call.data.startswith("['submit'")):
        userid = ast.literal_eval(call.data)[1]
        if submitstatus[str(userid)] == False:
            submitstatus[str(userid)] = True
            print("status changed to : ",submitstatus[str(userid)])
            user[str(userid)].sort()
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  text="Here are the Roll Calls of the Students",
                                  message_id=call.message.message_id,
                                  reply_markup=inlines.editKeyboard(-1,stringList,user[str(userid)],submitstatus[str(userid)],userid),
                                  parse_mode='HTML')
            print("Middleway")
            bot.send_message(chat_id=call.message.chat.id,
                             text="Attendance submitted Successfully",
                             parse_mode='HTML')
            present = "Roll No's Present are : "
            present = userFunc.showRollCall(userid, user, present)
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
