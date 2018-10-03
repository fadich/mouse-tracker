import sys

from queue import Queue
from typing import Tuple
from functools import partial
from threading import Event, Thread
from collections import OrderedDict

from tabulate import tabulate

from tracker import Tracker
from history import History, Executor, BaseCommand
from mouse import ClickRegisterer, get_position, move_to, click


class MoveCommand(BaseCommand):

    def __init__(self, do_pos: Tuple, undo_pos: Tuple):
        super().__init__()
        self.do_pos = do_pos
        self.undo_pos = undo_pos

    def do(self):
        return move_to(self.do_pos)

    def undo(self):
        return move_to(self.undo_pos)

    def __str__(self):
        return 'Move ({}, {})'.format(*self.do_pos)


class ClickCommand(BaseCommand):

    def do(self):
        return click()

    def undo(self):
        return click()

    def __str__(self):
        return 'Click'


def get_command():
    queue = Queue()

    def register_position():
        while True:
            pos = get_position()
            queue.put(MoveCommand(pos, pos))

    def register_click():
        c = ClickRegisterer(partial(queue.put, ClickCommand()))
        # try:
        #     c.run()
        # except KeyboardInterrupt:
        #     c.stop()

    Thread(target=register_click, daemon=True).start()
    Thread(target=register_position, daemon=True).start()

    while True:
        if not queue.empty():
            yield queue.get()


def display_table(history: History):
    rows_data = [(i[0], str(i[1])) for i in history.commands.items()]
    table = tabulate(rows_data, headers=('Time', 'Event'),
                     tablefmt='grid', stralign='left', numalign='center')

    print(table)


def execute(history: History, reverse: bool = False):
    e = Executor(history)
    e.run(reverse)


def main(*args):
    history = History()
    break_event = Event()

    tracker = Tracker(history=history, event_list=get_command(), break_event=break_event)

    print('Tracking the mouse cursor moving.')
    print('Press [Ctrl+C] to stop the tracker...')

    try:
        tracker.start()
    except KeyboardInterrupt:
        tracker.stop()

    options = OrderedDict([
        ('1', 'Display history'),
        ('2', 'Execute'),
        ('3', 'Reversed'),
        ('0', 'Exit'),
    ])

    menu = tabulate(options.items(), headers=('Key', 'Option'),
                    tablefmt='grid', stralign='left', numalign='center')

    try:
        while True:
            option = input('{}\n{}'.format(menu, 'Type the option: '))

            if option not in options.keys():
                continue
            elif option == '0':
                break
            elif option == '1':
                display_table(history)
            elif option == '2':
                execute(history)
            elif option == '3':
                execute(history, True)

    except KeyboardInterrupt:
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
