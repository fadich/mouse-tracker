import sys

from collections import OrderedDict

from tabulate import tabulate

from tracker import Tracker, Event
from history import History, Executor
from mouse import get_position, move_to


def display_table(history: History):
    rows_data = [(i[0], *i[1]) for i in history.events.items()]
    table = tabulate(rows_data, headers=('Time', 'X', 'Y'),
                     tablefmt='grid', stralign='left', numalign='center')

    print(table)


def execute(history: History):
    e = Executor(history, move_to)
    e.run()


def main(*args):
    pos_history = History()
    break_event = Event()

    t = Tracker(history=pos_history, event_registerer=get_position,
                break_event=break_event)
    # t.start_in_thread()

    try:
        print('Tracking the mouse cursor moving.')
        print('Press [Ctrl+C] to stop the tracker...')
        t.start()
    except KeyboardInterrupt:
        t.stop()

    options = OrderedDict([
        ('1', 'Display history'),
        ('2', 'Execute'),
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
                display_table(pos_history)
            elif option == '2':
                execute(pos_history)

    except KeyboardInterrupt:
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main())
