class BotFunctions():
    def __init__(self, botinstance):
        self.funcs = {}
        self._botinstance = botinstance

    def addNewFunc(self, _class, *args):
        _class = _class(self._botinstance, args)
        self.funcs[_class.getCallbackName()] = _class

    def getFuncs(self):
        return self.funcs