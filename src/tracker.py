from typing import Callable
from threading import Thread, Event

from history import History


class Tracker(object):
    history = None  # type: History
    break_event = None  # type: Event
    event_registerer = None  # type: Callable

    _thread = None  # type: Thread

    def __init__(self, history: History, event_registerer: Callable,
                 break_event: Event):
        super().__init__()
        self.history = history
        self.break_event = break_event
        self.event_registerer = event_registerer

    def start(self):
        """Run the Tracker until the break event is set."""

        if not self.history:
            raise RuntimeError('The history property does not set')

        while not self.break_event.is_set():
            self.history.commit_event(self.event_registerer())

    def start_in_thread(self):
        """Run the Tracker **in thread** until the break event is set."""

        self._thread = Thread(target=self.start)
        self._thread.start()

    def stop(self):
        """Stop tracking."""

        if isinstance(self.break_event, Event) \
                and not self.break_event.is_set():
            self.break_event.set()

        if isinstance(self._thread, Thread) and self._thread.is_alive():
            self._thread.join()


