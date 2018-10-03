import pyautogui

from time import sleep
from typing import Callable

from pymouse import PyMouseEvent


pyautogui.FAILSAFE = False


class ClickRegisterer(PyMouseEvent):

    def __init__(self, cb: Callable):
        super().__init__(self)
        self.cb = cb

    def click(self, x, y, button, press):
        # self.cb()
        # print(locals())
        # pyautogui.click()
        return True


def get_position():
    sleep(0.01)
    return pyautogui.position()


def move_to(positions):
    pyautogui.moveTo(positions, duration=0.0, pause=0.0)


def click():
    pyautogui.click()
