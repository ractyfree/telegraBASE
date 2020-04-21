from .User import User


class UsersPool():
    def __init__(self):
        self.__usersList = {}

    def getUserById(self, id):
        try:
            return self.__usersList[id]
        except KeyError:
            return None

    def isUserRegistered(self, id):
        return self.getUserById(id)

    def addUser(self, User: User):
        self.__usersList[User.getId()] = User