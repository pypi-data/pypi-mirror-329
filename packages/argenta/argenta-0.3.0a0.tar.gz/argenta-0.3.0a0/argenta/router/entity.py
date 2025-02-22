from typing import Callable, Any
from ..command.entity import Command
from ..command.input_comand.entity import InputCommand
from ..command.input_comand.exceptions import InvalidInputFlagException
from ..command.params.flag.flags_group.entity import FlagsGroup
from ..router.exceptions import (UnknownCommandHandlerHasAlreadyBeenCreatedException,
                                 RepeatedCommandException, RepeatedFlagNameException)


class Router:
    def __init__(self,
                 title: str = 'Commands group title:',
                 name: str = 'subordinate'):

        self.title = title
        self.name = name

        self._command_entities: list[dict[str, Callable[[], None] | Command]] = []
        self.unknown_command_func: Callable[[str], None] | None = None
        self._is_main_router: bool = False
        self.ignore_command_register: bool = False


    def command(self, command: Command) -> Callable[[Any],  Any]:
        command.validate_commands_params()
        self._validate_command(command)

        def command_decorator(func):
            self._command_entities.append({'handler_func': func,
                                           'command': command})
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        return command_decorator


    def unknown_command(self, func):
        if self.unknown_command_func is not None:
            raise UnknownCommandHandlerHasAlreadyBeenCreatedException()

        self.unknown_command_func: Callable = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


    def input_command_handler(self, input_command: InputCommand):
        input_command_name: str = input_command.get_string_entity()
        for command_entity in self._command_entities:
            if input_command_name.lower() == command_entity['command'].get_string_entity().lower():
                if self.ignore_command_register:
                    if input_command.get_input_flags():
                        for flag in input_command.get_input_flags():
                            is_valid = command_entity['command'].validate_input_flag(flag)
                            if not is_valid:
                                raise InvalidInputFlagException(flag)
                        return command_entity['handler_func'](input_command.get_input_flags())
                    else:
                        return command_entity['handler_func']()
                else:
                    if input_command_name == command_entity['command'].get_string_entity():
                        if input_command.get_input_flags():
                            for flag in input_command.get_input_flags():
                                is_valid = command_entity['command'].validate_input_flag(flag)
                                if not is_valid:
                                    raise InvalidInputFlagException(flag)
                            return command_entity['handler_func'](input_command.get_input_flags())
                        else:
                            return command_entity['handler_func']()


    def unknown_command_handler(self, unknown_command):
        self.unknown_command_func(unknown_command)


    def _validate_command(self, command: Command):
        command_name: str = command.get_string_entity()
        if command in self.get_all_commands():
            raise RepeatedCommandException()
        if self.ignore_command_register:
            if command_name.lower() in [x.lower() for x in self.get_all_commands()]:
                raise RepeatedCommandException()

        flags: FlagsGroup = command.get_flags()
        if flags:
            flags_name: list = [x.get_string_entity().lower() for x in flags]
            if len(set(flags_name)) < len(flags_name):
                raise RepeatedFlagNameException()


    def set_router_as_main(self):
        if self.name == 'subordinate':
            self.name = 'main'
        self._is_main_router = True


    def set_ignore_command_register(self, ignore_command_register: bool):
        self.ignore_command_register = ignore_command_register


    def get_command_entities(self) -> list[dict[str, Callable[[], None] | Command]]:
        return self._command_entities


    def get_name(self) -> str:
        return self.name


    def get_title(self) -> str:
        return self.title


    def get_router_info(self) -> dict:
        return {
            'title': self.title,
            'name': self.name,
            'ignore_command_register': self.ignore_command_register,
            'attributes': {
                'command_entities': self._command_entities,
                'unknown_command_func': self.unknown_command_func,
                'is_main_router': self._is_main_router
            }

        }


    def get_all_commands(self) -> list[str]:
        all_commands: list[str] = []
        for command_entity in self._command_entities:
            all_commands.append(command_entity['command'].get_string_entity())

        return all_commands

    def get_all_flags(self) -> list[FlagsGroup]:
        all_flags: list[FlagsGroup] = []
        for command_entity in self._command_entities:
            all_flags.append(command_entity['command'].get_flags())

        return all_flags
