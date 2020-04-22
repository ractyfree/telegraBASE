from abc import ABC
from telebot import types

class BotFunctionality(ABC):
    stepDelimiter = ">>>"

    def __init__(self, bot):
        self._bot = bot
        stepDelimiter = ">>>"
        self.hiddenDefault = 0
   
    def getName(self):
        pass

    def getToStartKeyboard(self):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("<<< Вернуться назад", callback_data="start"))
        return markup
        
    def isHiddenForUser(self, user_id):
        pass
        
    def getCallbackName(self):
        return self.getName()

    def setDataStep(self, User, data):
        """
        Sets User's user_step with prefix of it's function
        """
        User.setUserStep("{0}{1}{2}".format(self.getCallbackName(), self.stepDelimiter, data))

    @staticmethod
    def isStepHasData(funcs, User):
        """
        Determines whether User's user_step has func's prefix or not.
        """
        try:
            return User.getUserStep().split(BotFunctionality.stepDelimiter)[0] in funcs
        except:
            return

    @staticmethod
    def getFuncData(funcs, User):
        """
        Gets func from Users's user_step and returns pointer
        """
        return funcs.getFuncs()[User.getUserStep().split(BotFunctionality.stepDelimiter)[0]]

    def start(self, **kwargs):
        pass