import ui
from cwio import *
from cwio.const import *

name = "Viewer"

def main():
    file = ui.choose_file()
    if file == -1: 
        return
    try:
        with open(file, "r") as f:
            l_lines = f.read().splitlines()
    except Exception:
        l_lines = ["Ralat membaca fail."]
        
    if not l_lines: 
        l_lines = [""]

    top = 0 
    total_lines = len(l_lines)
    s_clear = screen.clear
    s_write = screen.write
    s_apply = screen.apply
    kb_get = keyboard.get_next
    f_mini = font.miniwi
    color_b = SCR.COLOR.BLACK

    MAX_VISIBLE_CHARS = 32 
    dirty = True

    while True:
        if dirty:
            dirty = False
            s_clear()
            for i in range(8):
                idx = top + i
                if idx < total_lines:
                    line_view = l_lines[idx][:MAX_VISIBLE_CHARS]
                    s_write(line_view, 0, i * 8, color_b, f_mini)
            
            s_apply()

        key = kb_get()
        dirty = True
        
        if key == KB.KEY.DOWN:
            if top < total_lines - 8:
                top += 1

        elif key == KB.KEY.UP:
            if top > 0:
                top -= 1
        elif key in (KB.KEY.RIGHT, KB.KEY.PG_DOWN):
            if top + 8 < total_lines:
                top = min(total_lines - 8, top + 8)

        elif key in (KB.KEY.LEFT, KB.KEY.PG_UP):
            top = max(0, top - 8)
        elif key in (KB.KEY.HOME, KB.KEY.BACK, KB.KEY.AC):
            return