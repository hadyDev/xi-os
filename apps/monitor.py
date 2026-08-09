from cwio import *
from cwio.const import *
from machine import ADC
import time

name = "Monitor"
v_adc = ADC(3)

def get_v():
    t = 0
    for _ in range(20):
        t += v_adc.read_u16()
    return (t / 20) * (3.3 / 65535) * 3

def main():

    while True:
        v = get_v()
        p = ((v - 0.1) / (1.5 - 0.1)) * 100
        p = max(0, min(100, p))
        
        screen.clear()
        
        screen.write("MONITOR", 5, 2, SCR.COLOR.BLACK, font.classwiz_cw)
        
        screen.write(f"Raw volt: {v:.3f} V", 5, 20, SCR.COLOR.BLACK, font.miniwi)
        screen.write(f"Percent : {int(p)} %", 5, 30, SCR.COLOR.BLACK, font.miniwi)
        screen.write("Press ALPHA to back", 58, 50, SCR.COLOR.BLACK, font.miniwi)
        
        if v < 0.5:
            screen.write("CHECK WIRING!", 140, 25, SCR.COLOR.BLACK, font.miniwi)
        else:
            screen.write("SIGNAL OK", 140, 25, SCR.COLOR.BLACK, font.miniwi)

        screen.apply()
        
        if keyboard.pressed_any():
            if keyboard.get_next() == KB.KEY.HOME: return