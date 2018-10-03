from abc import ABCMeta, abstractmethod
from typing import Dict, List, Callable, Union
from datetime import datetime
from time import sleep


class BaseCommand(object, metaclass=ABCMeta):

    @abstractmethod
    def do(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class History(object):
    commands = {}  # type: Dict[str, BaseCommand]

    def add_command(self, command: BaseCommand):
        self.commands[datetime.now().isoformat()] = command


class Executor(object):
    history = None  # type: History

    def __init__(self, history: History):
        self.history = history

    def run(self, reverse: bool = False):
        i = 0
        items = self.history.commands.items()
        steps = len(items) - 1
        commands = list(items)  # type: List[Union[str, BaseCommand]]
        method = 'do'
        delta_factor = 1

        if reverse:
            commands.reverse()
            method = 'undo'
            delta_factor = -1

        while True:
            command = commands[i]
            getattr(command[1], method)()  # Call specific method

            if i + 1 > steps:
                break

            fmt = '%Y-%m-%dT%H:%M:%S.%f'
            current_at = datetime.strptime(command[0], fmt)
            next_at = datetime.strptime(commands[i + 1][0], fmt)
            delta = (next_at - current_at) * delta_factor
            sleep(delta.microseconds / 1_000_000)

            i += 1
