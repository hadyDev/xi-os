from cwio import *
from cwio.const import *
import machine

def deepsleep():
    screen.clear()
    screen.set_icon(SCR.ICON.POWER, SCR.COLOR.BLACK)
    screen.apply()
    print("[EASE] Waiting for calculator to detach")
    while calc.raw.pread(0):
        pass
    print("[PWRM] Deep sleep")
    machine.deepsleep()

