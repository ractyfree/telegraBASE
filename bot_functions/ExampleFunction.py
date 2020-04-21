from internal.BotFunctionality import BotFunctionality

class ExampleFunction(BotFunctionality):
    def __init__(self, bot, userpool):
        super().__init__(bot)
        self.name = "ExampleFunction"
        self._userpool = userpool

    def getName(self):
        return self.name

    def start(self, **kwargs):
        self._bot.reply_to(kwargs['call'].message, "test")
        

    def startNext(self, **kwargs):
        return