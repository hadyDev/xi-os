import ui
import utime
import ujson
from cwio import *
from cwio.const import *

name = "Drawing"

SAVE_FILE = "drawing_grid.json"
SW, SH = SCR.WIDTH, SCR.HEIGHT

def save_canvas(grid):
    try:
        with open(SAVE_FILE, "w") as f:
            ujson.dump(grid, f)
    except Exception:
        pass


def load_canvas():
    try:
        with open(SAVE_FILE, "r") as f:
            return ujson.load(f)
    except Exception:
        return [[0 for _ in range(SH)] for _ in range(SW)]


def main():
    x, y = SW // 2, SH // 2
    KEY_DRAW = KB.KEY.EXE

    s_set = screen.set
    s_clear = screen.clear_screen
    s_apply = screen.apply

    COLOR_BLK = SCR.COLOR.BLACK
    COLOR_DRK = SCR.COLOR.DARK
    COLOR_WHT = SCR.COLOR.WHITE
    grid = load_canvas()

    s_clear()
    for px in range(SW):
        for py in range(SH):
            if grid[px][py] == 1:
                s_set(px, py, COLOR_BLK)

    dirty = True
    MOVE_DELAY_MS = 20
    brush_size = 1
    is_eraser_mode = False

    while True:
        is_drawing = keyboard.pressed(KEY_DRAW)

        if is_drawing:
            fill_val = 0 if is_eraser_mode else 1
            color_val = COLOR_WHT if is_eraser_mode else COLOR_BLK

            for bx in range(brush_size):
                for by in range(brush_size):
                    px, py = x + bx, y + by
                    if px < SW and py < SH:
                        grid[px][py] = fill_val  
                        s_set(px, py, color_val)
            dirty = True
        if dirty:
            dirty = False

            if not is_drawing:
                for bx in range(brush_size):
                    for by in range(brush_size):
                        px, py = x + bx, y + by
                        if px < SW and py < SH:
                            s_set(px, py, COLOR_DRK)

            s_apply()

            if not is_drawing:
                for bx in range(brush_size):
                    for by in range(brush_size):
                        px, py = x + bx, y + by
                        if px < SW and py < SH:
                            orig_color = (
                                COLOR_BLK if grid[px][py] == 1 else COLOR_WHT
                            )
                            s_set(px, py, orig_color)

        if keyboard.pressed_any():
            key = keyboard.get_next(show_icon=False)
            dirty = True

            if key == KB.KEY.LEFT:
                x = max(0, x - 1)
            elif key == KB.KEY.RIGHT:
                x = min(SW - brush_size, x + 1)
            elif key == KB.KEY.UP:
                y = max(0, y - 1)
            elif key == KB.KEY.DOWN:
                y = min(SH - brush_size, y + 1)

            elif key == KB.KEY.N0:
                is_eraser_mode = True

            elif key == KB.KEY.N1:
                brush_size = 1
                is_eraser_mode = False
            elif key == KB.KEY.N2:
                brush_size = 2
                is_eraser_mode = False
            elif key == KB.KEY.N3:
                brush_size = 3
                is_eraser_mode = False
            elif key == KB.KEY.N4:
                brush_size = 4
                is_eraser_mode = False

            elif key == KB.KEY.ANS:
                save_canvas(grid)

            elif key in (KB.KEY.BACK, KB.KEY.BKSPACE):
                grid = [[0 for _ in range(SH)] for _ in range(SW)]
                s_clear()

            elif key == KB.KEY.HOME:
                save_canvas(grid)
                return

            utime.sleep_ms(MOVE_DELAY_MS)