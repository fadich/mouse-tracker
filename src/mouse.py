from time import sleep

from pyautogui import position, moveTo


def get_position():
    sleep(0.01)
    return position()


def move_to(positions):
    moveTo(positions, duration=0.0, pause=0.0)
