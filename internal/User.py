from telebot import types, apihelper

class User():
    def __init__(self, id, user_step=""):
        self.__id = id
        self.__userStep = user_step
        self.__last_message = 0
        self.__rights = { 
            "admin": 0,
            "banned": 0
        }

    def getUserRights(self):
        return self.__rights

    def setUserRights(self, rights):
        self.__rights = rights
        return self.__rights

    def setUserAdmin(self, _set):
        self.__rights["admin"] = _set
        
    def getUserStep(self):
        return self.__userStep

    def setUserStep(self, step):
        self.__userStep = step

    def resetUserStep(self):
        return self.setUserStep("")
    def getId(self):
        return self.__id

    def getLastMessage(self):
        return self.__last_message

    def setLastMessage(self, message: types.Message):
        self.__last_message = message
        return self.getLastMessage()