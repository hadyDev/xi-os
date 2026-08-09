from cwio import *
from cwio.const import *
from cwio.screen import MonoImage
import os
import fs
import res

def notify(title: str, msg: str, icon: MonoImage | None = None, wait: bool = True):
    screen.clear()
    if icon:
        screen.image(icon, 0, 0, SCR.COLOR.BLACK)
        screen.write(title, 26, 6, SCR.COLOR.BLACK, font.classwiz_cw)
    else:
        screen.write(title, 0, 6, SCR.COLOR.BLACK, font.classwiz_cw)
    screen.write(msg, 0, 24, SCR.COLOR.BLACK, font.miniwi)
    screen.apply()
    if wait:
        keyboard.wait()


def choose(items: list[str], msg: str | None = None) -> int:
    refresh = True
    x = 0
    y = 0
    f = font.miniwi
    h = f().h
    oldsel = 0
    sel = 0
    oldpage = None
    page = 0
    while True:
        page = sel // 4
        curr = items[page * 4:(page + 1) * 4]
        if oldpage != page:
            oldpage = page
            refresh = True
        if refresh:
            refresh = False
            screen.clear()
            screen.write("XIOS MENU", 74, 2, SCR.COLOR.BLACK, font.miniwi)
            if msg:
                screen.write(msg, 0, 0, SCR.COLOR.BLACK, font.miniwi)
            for i, (item) in enumerate(curr):
                ix = x + 2
                iy = (y + (h + 2) * i) + 12
                screen.image(res.ui.circled(i + 1), ix, iy, SCR.COLOR.BLACK)
                screen.write(item, ix + 12, iy + 1, SCR.COLOR.BLACK, f)
        for i, (item) in enumerate(curr):
            if i == sel % 4 or i == oldsel % 4:
                screen.box(x + 12, y + (h + 2) * i + 12, SCR.WIDTH - 12, h + 2, (SCR.COLOR.BLACK if i == sel % 4 else SCR.COLOR.WHITE))
        screen.apply()
        while keyboard.pressed(KB.KEY.OK):
            pass
        key = keyboard.get_next()
        oldsel = sel
        if key == KB.KEY.UP:
            sel = (sel - 1) % len(items)
        elif key == KB.KEY.DOWN:
            sel = (sel + 1) % len(items)
        elif key == KB.KEY.PG_UP:
            sel = (sel - 4) % len(items)
        elif key == KB.KEY.PG_DOWN:
            sel = (sel + 4) % len(items)
        elif key == KB.KEY.OK:
            return sel
        elif key == KB.KEY.BACK:
            return -1
        elif key == KB.KEY.N1:
            return page * 4
        elif key == KB.KEY.N2:
            return page * 4 + 1
        elif key == KB.KEY.N3:
            return page * 4 + 2
        elif key == KB.KEY.N4:
            return page * 4 + 3
        


def choose_file(start: str = "/"):
    curr = os.listdir(start)
    path = choose(curr, start)
    if path == -1:
        return -1
    
    path = start + curr[path]
    if fs.isfile(path):
        return path
    elif fs.isdir(path):
        return choose_file(path + "/")
    
    
    return -1


keypad = {"8": ["a", "b", "c"], "9": ["d", "e", "f"], "4": ["g", "h", "i"], "5": ["j", "k", "l"], "6": ["m", "n", "o"], "1": ["p", "q", "r", "s"], "2": ["t", "u", "v"], "3": ["w", "x", "y", "z"], "0": [" "]}

def ask(msg: str | None = None, default: str = ""):
    buf = default
    shift = False
    while True:
        screen.clear()
        if msg:
            screen.write(msg, 0, 0, SCR.COLOR.BLACK, font.miniwi)
        screen.write(buf + "|", 0, (8 if msg else 0), SCR.COLOR.BLACK, font.miniwi)
        screen.apply()
        while keyboard.pressed_any():
            pass
        key = keyboard.get_next()
        if key == KB.KEY.SHIFT:
            shift = not shift
            
        elif key == KB.KEY.FORMAT and len(buf):
            last = buf[-1]
            if last.isdigit():
                count = 0
                for c in reversed(buf):
                    if c != last:
                        break
                    ((count := count+1)-1)
                if last in keypad:
                    letters = keypad[last]
                    if count <= len(letters):
                        letter = letters[count - 1]
                        if shift:
                            shift = False
                            letter = letter.upper()
                        buf = buf[:-count] + letter
        elif shift:
            shift = False
            if key == KB.KEY.SUBTRACT:
                buf += "_"
        else:
            if key == KB.KEY.EXE:
                return buf
            elif key == KB.KEY.AC:
                buf = ""
            elif key == KB.KEY.BKSPACE:
                buf = buf[:-1]
            elif key == KB.KEY.N0:
                buf += "0"
            elif key == KB.KEY.N1:
                buf += "1"
            elif key == KB.KEY.N2:
                buf += "2"
            elif key == KB.KEY.N3:
                buf += "3"
            elif key == KB.KEY.N4:
                buf += "4"
            elif key == KB.KEY.N5:
                buf += "5"
            elif key == KB.KEY.N6:
                buf += "6"
            elif key == KB.KEY.N7:
                buf += "7"
            elif key == KB.KEY.N8:
                buf += "8"
            elif key == KB.KEY.N9:
                buf += "9"
            elif key == KB.KEY.DIVIDE:
                buf += "/"
            


class Widget:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    
    
    def __render__(self, ox: int, oy: int):
        pass
    
    def __update__(self):
        pass
    


class Label(Widget):
    def __init__(self, x, y, text, color, font):
        super().__init__(x=x, y=y)
        self.text = text
        self.color = color
        self.font = font
        
    
    
    def __render__(self, ox: int, oy: int):
        screen.write(self.text, self.x + ox, self.y + oy, self.color, self.font)
    


class Image(Widget):
    def __init__(self, x, y, img, color):
        super().__init__(x=x, y=y)
        self.img = img
        self.color = color
        
    
    
    def __render__(self, ox: int, oy: int):
        screen.image(self.img, self.x + ox, self.y + oy, self.color)
    


class SizableWidget:
    def __init__(self, x, y, w, h):
        super().__init__(x=x, y=y)
        self.w = w
        self.h = h
        
    


class Container(SizableWidget):
    def __init__(self, x, y, w, h):
        super().__init__(x=x, y=y, w=w, h=h)
        self.children = []
    
    
    def __render__(self, ox: int, oy: int):
        for w in self.children:
            w.__render__(self.x + ox, self.y + oy)
    
    
    def add(self, w: Widget) -> None:
        self.children.append(w)
    


class Screen:
    def __init__(self):
        self.children = []
    
    
    def render(self):
        for w in self.children:
            w.__render__(0, 0)
    
    
    def add(self, w: Widget) -> None:
        self.children.append(w)
        return self
    
    
    def __add__(self, w: Widget):
        self.add(w)
        return self
    
