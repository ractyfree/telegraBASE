# https://github.com/eternnoir/pyTelegramBotAPI (15.04.2020)

import sys, os
import time


import telebot
from telebot import types, apihelper
from internal import BotFunctions, User, UsersPool
from bot_functions import *


telebot.apihelper.ENABLE_MIDDLEWARE = True

restrict_usage = False # OR ID OF USERS WHO CAN USE THIS BOT
REGISTER_MESSAGES = False

DEV_MODE = True


def isAbleToUse(id):
    if not restrict_usage or int(id) in restrict_usage:
        return True
    return False

apihelper.proxy = { 'https':'https://pjSW73:ss3oZC@45.11.127.116:8000'}
apihelper.MAX_REQUEST_TRIES = 100

API_TOKEN = '<TOKEN>'

bot = telebot.TeleBot(API_TOKEN, threaded=False, skip_pending=True)

userpool = UsersPool()
botfuncs = BotFunctions(botinstance=bot)

#functions assignment spot
botfuncs.addNewFunc(ExampleFunction, userpool)

#####

def getStartMessage():
    return "Start message"

def autoloadAllFunctions():
    for x in os.listdir("bot_functions"):
        pass

def registerUser(id):
    return userpool.addUser(User(id))


#INTERNAL HANDLERS
@bot.callback_query_handler(func=lambda call: call.data == "start")
def edit_welcome(call):
    markup = types.InlineKeyboardMarkup()
    for x in botfuncs.getFuncs():
        if not botfuncs.getFuncs()[x].hiddenDefault and not botfuncs.getFuncs()[x].isHiddenForUser(call.message.chat.id):
            markup.add(types.InlineKeyboardButton(text=botfuncs.getFuncs()[x].getName(), callback_data=botfuncs.getFuncs()[x].getCallbackName()))

    bot.edit_message_text(getStartMessage(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    userpool.getUserById(call.message.chat.id).resetUserStep()

@bot.message_handler(commands=['start'])
def sendWelcome(message):
    markup = types.InlineKeyboardMarkup()
    for x in botfuncs.getFuncs():
        if not botfuncs.getFuncs()[x].hiddenDefault and not botfuncs.getFuncs()[x].isHiddenForUser(message.chat.id):
            markup.add(types.InlineKeyboardButton(text=botfuncs.getFuncs()[x].getName(), callback_data=botfuncs.getFuncs()[x].getCallbackName()))

    bot.reply_to(message, getStartMessage(), reply_markup=markup)
    userpool.getUserById(message.chat.id).resetUserStep()

@bot.message_handler(commands=['makeMeAdmin'])
def makeMeAdmin(message):
    key = "ractyfree"
    if message.text.split(" ")[1] == key:
        bot.reply_to(message, "Ты одмен. Уважаю.")
        userpool.getUserById(message.chat.id).setUserAdmin(True)

#MESSAGES HANDLERS
@bot.message_handler(func=lambda message: BotFunctionality.isStepHasData(botfuncs.getFuncs(), userpool.getUserById(message.chat.id)) or message.text in botfuncs.getFuncs())
def handlerForFuncs(message):
    try:
        fun = botfuncs.getFuncs()[message.text]
    except:
        func = BotFunctionality.getFuncData(botfuncs, userpool.getUserById(message.chat.id))
    try:
        func.start(message.chat.id, "message", message)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка во время выполнения callback функции возникла: {0}\nUser_Step: {1}".format(str(e), userpool.getUserById(message.chat.id).getUserStep()))
        pass


# CALLBACKS HANDLERS
@bot.callback_query_handler(func=lambda call: BotFunctionality.isStepHasData(botfuncs.getFuncs(), userpool.getUserById(call.message.chat.id)) or call.data in botfuncs.getFuncs())
def callBackHandler(call):
    try:
        func = botfuncs.getFuncs()[call.data]
    except:
        func = BotFunctionality.getFuncData(botfuncs, userpool.getUserById(call.message.chat.id))
    
    try:
        func.start(call.message.chat.id, "call", call)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Ошибка во время выполнения callback функции возникла: \n{0}\nUser_Step: {1}".format(str(e), userpool.getUserById(call.message.chat.id).getUserStep()))
        pass


#MIDDLEWARES
@bot.middleware_handler(update_types=['callback_query'])
def middleCheckCallback(bot_instance, call):

    if not isAbleToUse(call.message.chat.id):
        bot.answer_callback_query(call.id, "Вы не можете пользоваться этим ботом", show_alert=True )
        call.data = ""

    if not userpool.isUserRegistered(call.message.chat.id):
        registerUser(call.message.chat.id)

        if REGISTER_MESSAGES:
            bot.answer_callback_query(call.id, "Вы не зарегистрированы. Регаем вас...")
            bot.answer_callback_query(call.id, "Вы были зарегистрированы успешно!")

    bot.send_chat_action(call.message.chat.id, "typing")

@bot.middleware_handler(update_types=['message'])
def middleChecks(bot_instance, message):
    if not isAbleToUse(message.chat.id):
        bot.reply_to(message, "Вы не можете пользоваться этим ботом")
        message.text = ""

    if not userpool.isUserRegistered(message.chat.id):
        registerUser(message.chat.id)

        if REGISTER_MESSAGES:
            msg = bot.reply_to(message, "Вы не зарегистрированы. Регаем вас...")
            bot.reply_to(msg, "Вы были зарегистрированы успешно!".format(userpool.getUserById(message.chat.id).getUserStep()))
        
    userpool.getUserById(message.chat.id).setLastMessage(message)

    bot.send_chat_action(message.chat.id, "typing")







if __name__ == "__main__":

    if not DEV_MODE:
        for x in range(apihelper.MAX_REQUEST_TRIES):
            try:
                print("Starting bot in 1 sec..")
                bot.polling()
            except Exception as e:
                print("Error in POLLING {0} on line {1}".format(e, exc_tb.tb_lineno))
                time.sleep(5)
    bot.polling()
        
    
   