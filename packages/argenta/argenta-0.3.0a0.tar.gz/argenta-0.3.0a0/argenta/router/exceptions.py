class InvalidDescriptionInstanceException(Exception):
    def __str__(self):
        return "Invalid Description Instance"


class UnknownCommandHandlerHasAlreadyBeenCreatedException(Exception):
    def __str__(self):
        return "Only one unknown command handler can be declared"


class RepeatedCommandException(Exception):
    def __str__(self):
        return "Commands in handler cannot be repeated"


class RepeatedFlagNameException(Exception):
    def __str__(self):
        return "Repeated flag name in register command"
