from . import calc
from . import const
from . import screen
from . import keyboard
from time import sleep_ms

def init():
    calc.init()
    sleep_ms(15)
    calc.connect()
