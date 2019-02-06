#!/usr/bin/python3.6
import time

from pynput.keyboard import Key, Controller

keyboard = Controller()

while True:
    keyboard.press(Key.ctrl)
    print('ctrl key has been sent')
    keyboard.release(Key.ctrl)
    print('ctrl key has been release')
    time.sleep(3)
