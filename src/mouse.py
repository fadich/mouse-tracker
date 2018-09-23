import pyautogui

from time import sleep


pyautogui.FAILSAFE = False


def get_position():
    sleep(0.01)
    return pyautogui.position()


def move_to(positions):
    pyautogui.moveTo(positions, duration=0.0, pause=0.0)
