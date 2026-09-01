import utime
import urandom
from cwio import *
from cwio.const import *

name = "CMatrix"

def main():
    # 1. LOCAL CONSTANTS (Laju daripada baca Global Variable)
    SCREEN_W = 192
    SCREEN_H = 64
    CHAR_W = 4
    CHAR_H = 4
    COLS = 48  # SCREEN_W // CHAR_W
    COLOR_BLK = SCR.COLOR.BLACK

    # 2. BYTEARRAY (Sifar pembaziran RAM)
    drops_y = bytearray(COLS)
    drops_speed = bytearray(COLS)
    drops_len = bytearray(COLS)

    for i in range(COLS):
        drops_y[i] = urandom.randint(0, 16)
        drops_speed[i] = urandom.randint(1, 2)
        drops_len[i] = urandom.randint(3, 8)

    # 3. LOCAL FUNCTION BINDING
    s_set = screen.set
    s_clear = screen.clear_screen
    s_apply = screen.apply
    kb_pressed = keyboard.pressed_any
    kb_get = keyboard.get_next

    # Pre-cache key tuples
    EXIT_KEYS = (KB.KEY.HOME, KB.KEY.AC, KB.KEY.BACK)

    while True:
        if kb_pressed():
            if kb_get(show_icon=False) in EXIT_KEYS:
                return

        s_clear()

        # 4. FAST LOOP RENDERING
        for x_col in range(COLS):
            x_px = x_col * CHAR_W
            x_px_1 = x_px + 1
            
            y_head = drops_y[x_col] - 16
            speed = drops_speed[x_col]
            length = drops_len[x_col]

            # Guna addition untuk ganti multiplication
            y_px = y_head * CHAR_H

            for i in range(length):
                # Check bounding skrin dulu sebelum buat apa-apa
                if 0 <= y_px < SCREEN_H:
                    if i == 0:
                        # Kepala titisan (2x2 pixel)
                        y_px_1 = y_px + 1
                        s_set(x_px, y_px, COLOR_BLK)
                        s_set(x_px_1, y_px, COLOR_BLK)
                        s_set(x_px, y_px_1, COLOR_BLK)
                        s_set(x_px_1, y_px_1, COLOR_BLK)
                    elif (i + x_col) & 1 == 0:
                        # Ekor
                        s_set(x_px, y_px, COLOR_BLK)

                # Anjak y_px ke atas untuk ekor seterusnya (secara penambahan)
                y_px -= CHAR_H

            # Update pergerakan
            new_y = y_head + speed
            drops_y[x_col] = new_y + 16

            # Reset bila dah hilang sepenuhnya dari skrin
            if (new_y - length) * CHAR_H > SCREEN_H:
                drops_y[x_col] = 16 - urandom.randint(2, 10)
                drops_speed[x_col] = urandom.randint(1, 2)
                drops_len[x_col] = urandom.randint(3, 8)

        s_apply()

if __name__ == "__main__":
    main()