from telebot import types

crossIcon = u"\u2705"
tickIcon = u"\u2610"


def sociallinks():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text="⚇ Github", url="https://github.com/Nitesh-13/SnowFlake-Telegram-Bot"))
    return markup


def makeKeyboard(stringList, userid):
    markup = types.InlineKeyboardMarkup()
    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=key+". "+value, callback_data="['value', '" + value + "', '" + key + "', '"+str(userid)+"']"),
                   types.InlineKeyboardButton(text=tickIcon, callback_data="['key', '" + key + "', '"+str(userid)+"']"))

    markup.add(types.InlineKeyboardButton(
        text="Submit Attendance", callback_data="['submit', '"+str(userid)+"']"))
    return markup


def editKeyboard(rollno, stringList, rollcall, submitstatus,userid):
    markup = types.InlineKeyboardMarkup()
    print(rollcall)
    for key, value in stringList.items():
        if key in rollcall:
            add = True
        else:
            add = False
        if (key == rollno and add == True) or add == True:
            markup.add(types.InlineKeyboardButton(text=key+". "+value, callback_data="['value', '" + value + "', '" + key + "', '"+str(userid)+"']"),
                       types.InlineKeyboardButton(text=crossIcon, callback_data="['key', '" + key + "', '"+str(userid)+"']"))
        else:
            markup.add(types.InlineKeyboardButton(text=key+". "+value, callback_data="['value', '" + value + "', '" + key + "', '"+str(userid)+"']"),
                       types.InlineKeyboardButton(text=tickIcon, callback_data="['key', '" + key + "', '"+str(userid)+"']"))

    if rollno == -1 or submitstatus == True:
        markup.add(types.InlineKeyboardButton(
            text=crossIcon+" Attendance Submitted", callback_data="['submit', '"+str(userid)+"']"))
    else:
        markup.add(types.InlineKeyboardButton(
            text="Submit Attendance", callback_data="['submit', '"+str(userid)+"']"))
    return markup