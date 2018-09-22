from typing import Dict, Any, Callable
from datetime import datetime
from time import sleep


class History(object):
    events = {}  # type: Dict[str, Any]

    def commit_event(self, event: Any):
        self.events[datetime.now().isoformat()] = event


class Executor(object):
    action = None  # type: Callable
    history = None  # type: History

    def __init__(self, history: History, action: Callable):
        self.action = action
        self.history = history

    def run(self):
        i = 0
        items = self.history.events.items()
        steps = len(items) - 1
        events = list(items)

        while True:
            event = events[i]
            self.action(event[1])

            if i + 1 > steps:
                break

            fmt = '%Y-%m-%dT%H:%M:%S.%f'
            current_at = datetime.strptime(event[0], fmt)
            next_at = datetime.strptime(events[i + 1][0], fmt)
            delta = next_at - current_at
            sleep(delta.microseconds / 1_000_000)

            i += 1
