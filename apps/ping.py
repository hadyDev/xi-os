import ui
import utime
import urandom
from cwio import *
from cwio.const import *

name = "Ping Pong"


def main():
    SW, SH = 192, 64
    HALF_W = 96
    PADDLE_H = 12

    s_set = screen.set
    s_clear = screen.clear_screen
    s_apply = screen.apply
    s_write = screen.write

    COLOR_BLK = SCR.COLOR.BLACK
    COLOR_DRK = SCR.COLOR.DARK
    FONT_MINI = font.miniwi

    EXIT_KEYS = (KB.KEY.HOME, KB.KEY.AC, KB.KEY.BACK)
    KEY_UP = KB.KEY.UP
    KEY_DOWN = KB.KEY.DOWN

    py = 26
    ai_y = 26

    bx, by = 96, 32
    b_dx = 2
    b_dy = 1 if urandom.randint(0, 1) else -1

    p_score = 0
    ai_score = 0
    p_score_str = "0"
    ai_score_str = "0"

    kb_pressed = keyboard.pressed
    kb_pressed_any = keyboard.pressed_any
    kb_get = keyboard.get_next

    while True:
        if kb_pressed_any():
            key = kb_get(show_icon=False)
            if key in EXIT_KEYS:
                return
            elif key == KEY_UP:
                py = max(0, py - 3)
            elif key == KEY_DOWN:
                py = min(52, py + 3)

        if kb_pressed(KEY_UP):
            py = max(0, py - 2)
        elif kb_pressed(KEY_DOWN):
            py = min(52, py + 2)

        bx += b_dx
        by += b_dy

        if by <= 0:
            by = 0
            b_dy = -b_dy
        elif by >= 63:
            by = 63
            b_dy = -b_dy

        if bx > 96:
            ai_center = ai_y + 6
            if ai_center < by:
                if ai_y < 52:
                    ai_y += 1
            elif ai_center > by:
                if ai_y > 0:
                    ai_y -= 1

        if bx <= 6:
            if py <= by <= py + 12:
                bx = 6
                b_dx = abs(b_dx)
                b_dy = 1 if (by - py - 6) >= 0 else -1

        elif bx >= 185:
            if ai_y <= by <= ai_y + 12:
                bx = 185
                b_dx = -abs(b_dx)

        if bx < 0:
            ai_score += 1
            ai_score_str = str(ai_score)
            bx, by = 96, 32
            b_dx = 2
            b_dy = 1 if urandom.randint(0, 1) else -1
        elif bx > 192:
            p_score += 1
            p_score_str = str(p_score)
            bx, by = 96, 32
            b_dx = -2
            b_dy = 1 if urandom.randint(0, 1) else -1

        s_clear()

        for my in range(0, 64, 6):
            s_set(96, my, COLOR_DRK)
            s_set(96, my + 1, COLOR_DRK)

        for i in range(12):
            py_i = py + i
            s_set(4, py_i, COLOR_BLK)
            s_set(5, py_i, COLOR_BLK)

            ai_y_i = ai_y + i
            s_set(186, ai_y_i, COLOR_BLK)
            s_set(187, ai_y_i, COLOR_BLK)

        bx_1 = bx + 1
        by_1 = by + 1
        s_set(bx, by, COLOR_BLK)
        s_set(bx_1, by, COLOR_BLK)
        s_set(bx, by_1, COLOR_BLK)
        s_set(bx_1, by_1, COLOR_BLK)

        s_write(p_score_str, 76, 2, COLOR_BLK, FONT_MINI)
        s_write(ai_score_str, 110, 2, COLOR_BLK, FONT_MINI)

        s_apply()
        utime.sleep_ms(20)