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


@bot.message_handler(commands=['start'])
def sendWelcome(message):
    markup = types.InlineKeyboardMarkup()
    for x in botfuncs.getFuncs():
        if not botfuncs.getFuncs()[x].hidden:
            markup.add(types.InlineKeyboardButton(text=botfuncs.getFuncs()[x].getName(), callback_data=botfuncs.getFuncs()[x].getCallbackName()))

    bot.reply_to(message, getStartMessage(), reply_markup=markup)
    userpool.getUserById(message.chat.id).resetUserStep()


@bot.message_handler(func=lambda message: BotFunctionality.isStepHasData(botfuncs.getFuncs(), userpool.getUserById(message.chat.id)))
def handlerForFuncs(message):

    func = BotFunctionality.getFuncData(botfuncs, userpool.getUserById(message.chat.id))
    try:
        func.startNext(message=message)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка во время выполнения функции возникла: {0}\nUser_Step: {1}".format(str(e), userpool.getUserById(call.message.chat.id).getUserStep()))
        pass


@bot.message_handler(func=lambda message: message.text in botfuncs.getFuncs(), content_types=['text'])
def invokeFunc(message):
    
    funClass = botfuncs.getFuncs()[message.text]
    try:
        funClass.start(message=message)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка во время выполнения функции возникла: {0}\nUser_Step: {1}".format(str(e), userpool.getUserById(call.message.chat.id).getUserStep()))
        pass


# GetSpamText.somestuff
@bot.callback_query_handler(func=lambda call: BotFunctionality.isStepHasData(botfuncs.getFuncs(), userpool.getUserById(call.message.chat.id)))
def handlerForFuncs(call):
    func = BotFunctionality.getFuncData(botfuncs, userpool.getUserById(call.message.chat.id))
    try:
        func.startNext(call=call)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Ошибка во время выполнения функции возникла: {0}\nUser_Step: {1}".format(str(e), userpool.getUserById(call.message.chat.id).getUserStep()))
        pass

@bot.callback_query_handler(func=lambda call: call.data in botfuncs.getFuncs())
def invokeFunc(call):
    funClass = botfuncs.getFuncs()[call.data]
    try:
        funClass.start(call=call)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Ошибка во время выполнения функции возникла: {0}\nUser_Step: {1}".format(str(e), userpool.getUserById(call.message.chat.id).getUserStep()))
        pass

@bot.middleware_handler(update_types=['callback_query'])
def middleCheckCallback(bot_instance, call):
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
        
    
   