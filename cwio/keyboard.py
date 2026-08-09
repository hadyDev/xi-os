from . import calc
from . import screen
from .const import *

def init() -> None:
    calc.write(KB.IN_MASK, 255)
    calc.write(KB.OUT_MASK, 128)


def pressed_any() -> bool:
    calc.write(KB.OUT, 127)
    return calc.read(KB.IN) != 255


def pressed(code: int) -> bool:
    x = (code & 56) >> 3
    y = code & 7
    calc.write(KB.OUT, 1 << x)
    return not (calc.read(KB.IN) & (1 << y))


def wait_for(code: int, show_icon: bool = True) -> None:
    if pressed(code):
        return None
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.BLACK)
        screen.apply_icons()
    while not pressed(code):
        pass
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.WHITE)
        screen.apply_icons()


def wait(show_icon: bool = True) -> None:
    if pressed_any():
        pass
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.BLACK)
        screen.apply_icons()
    while not pressed_any():
        pass
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.WHITE)
        screen.apply_icons()


def get() -> int:
    for key in range(0, 63+1, 1):
        if pressed(key):
            return key
    return -1


def get_next(show_icon: bool = True) -> int:
    if pressed_any():
        for key in range(0, 63+1, 1):
            if pressed(key):
                return key
    k = -1
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.BLACK)
        screen.apply_icons()
    wait(show_icon = False)
    for key in range(0, 63+1, 1):
        if pressed(key):
            k = key
            break
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.WHITE)
        screen.apply_icons()
    return k
