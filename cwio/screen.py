from . import calc
from .const import *
from .font import Font
import utime
from . import raw_screen as raw

def on() -> None:
    calc.write(SCR.POWER, SCR.ENUM.POWER.RESET)
    utime.sleep_ms(1)
    calc.write(SCR.POWER, SCR.ENUM.POWER.ON)
    utime.sleep_ms(1)


def off() -> None:
    calc.write(SCR.POWER, SCR.ENUM.POWER.OFF)
    utime.sleep_ms(1)


def init() -> None:
    calc.write(SCR.MODE, SCR.ENUM.MODE.BUFFER | SCR.ENUM.MODE.ALL | SCR.ENUM.MODE.FLIP_X | SCR.ENUM.MODE.COLOR)
    calc.write(SCR.CONTRAST, 18)
    utime.sleep_ms(1)


empty = [bytearray((b"\x00" * SCR.SIZE)), bytearray((b"\x00" * SCR.SIZE))]
oldbuf = None
buf = [empty[0][0:], empty[1][0:]]

def in_rect(x: int, y: int, w: int, h: int) -> bool:
    return raw.in_bounds(x, y, w, h)


def in_bounds(x: int, y: int) -> bool:
    return raw.in_bounds(x, y, SCR.WIDTH, SCR.HEIGHT)


def clear() -> None:
    for plane in buf:
        raw.clear(plane, 0, SCR.SIZE)


def clear_screen() -> None:
    for plane in buf:
        raw.clear(plane, 0, SCR.SIZE - SCR.HEADER * SCR.WIDTH_B)


def clear_icons() -> None:
    for plane in buf:
        raw.clear(plane, SCR.TRUE_HEIGHT - SCR.HEADER * SCR.WIDTH_B, SCR.HEADER * SCR.WIDTH_B)


def get_group(x: int, y: int, pl: int) -> int:
    if not in_bounds(x, y):
        return 0
    return buf[pl][y * SCR.WIDTH_B + x // 8]


def set_group(x: int, y: int, pl: int, v: int) -> None:
    if not in_bounds(x, y):
        return None
    buf[pl][y * SCR.WIDTH_B + x // 8] = v


def paint_group(x: int, y: int, pl: int, b: int, m: bool) -> None:
    if not in_bounds(x, y):
        return None
    i = y * SCR.WIDTH_B + x // 8
    if m:
        buf[pl][i] |= b
    else:
        buf[pl][i] &= ~b


def set_raw(x: int, y: int, pl: int, v: bool) -> None:
    if not in_bounds(x, y):
        return None
    ox = x % 8
    paint_group(x, y, pl, 1 << (7 - ox), v)


def set(x: int, y: int, v: int) -> None:
    if not in_bounds(x, y):
        return None
    set_raw(x, y, 0, v & SCR.COLOR.BRIGHT)
    set_raw(x, y, 1, v & SCR.COLOR.DARK)


def set_byte(x: int, y: int, v: int) -> None:
    if not in_bounds(x, y):
        return None
    set_group(x, y, 0, (v & SCR.COLOR.BRIGHT) * 255)
    set_group(x, y, 1, ((v & SCR.COLOR.DARK) >> 1) * 255)


def set_icon(icon: int, v: int) -> None:
    if not (0 <= icon <= 23):
        return None
    buf[0][SCR.SIZE - SCR.HEADER * SCR.WIDTH_B + icon] = (v & SCR.COLOR.BRIGHT) * 255
    buf[1][SCR.SIZE - SCR.HEADER * SCR.WIDTH_B + icon] = ((v & SCR.COLOR.DARK) >> 1) * 255


def apply() -> None:
    global oldbuf
    global buf
    for i, (plane) in enumerate([SCR.ENUM.SELECT.PLANE0, SCR.ENUM.SELECT.PLANE1]):
        raw.apply(calc.write, SCR.SELECT, SCR.BUFFER, SCR.WIDTH_B, SCR.TRUE_WIDTH_B, SCR.HEIGHT, SCR.HEADER, buf[i], (oldbuf[i] if oldbuf else None), plane, 0, 0, SCR.WIDTH_B, SCR.HEIGHT)
    oldbuf = [buf[0][0:], buf[1][0:]]


def apply_icons() -> None:
    global buf
    for p, (rp) in enumerate([SCR.ENUM.SELECT.PLANE0, SCR.ENUM.SELECT.PLANE1]):
        calc.write(SCR.SELECT, rp)
        for y in range(0, SCR.HEADER, 1):
            for x in range(0, SCR.WIDTH_B, 1):
                i = (SCR.HEIGHT + y) * SCR.WIDTH_B + x
                calc.write(SCR.BUFFER + y * SCR.TRUE_WIDTH_B + x, buf[p][i])


def line_h(x: int, y: int, l: int, v: int):
    draw = False
    s = 0
    rx = x
    rl = x + l
    while rx < rl:
        if not draw:
            draw = in_bounds(rx, y)
        if draw:
            if not in_bounds(rx, y):
                return None
            if s == 0:
                if rx % 8:
                    set(rx, y, v)
                    rx += 1
                else:
                    s = 1
            elif s == 1:
                if rl - rx >= 8:
                    set_byte(rx, y, v)
                    rx += 8
                else:
                    s = 2
            else:
                set(rx, y, v)
                rx += 1


def line_v(x: int, y: int, l: int, v: int):
    draw = False
    for oy in range(0, l, 1):
        if not draw:
            draw = in_bounds(x, y + oy)
        if draw:
            if not in_bounds(x, y + oy):
                return None
            set(x, y + oy, v)


def box(x: int, y: int, w: int, h: int, v: int):
    line_h(x, y, w, v)
    line_h(x, y + h - 1, w, v)
    line_v(x, y + 1, h - 2, v)
    line_v(x + w - 1, y + 1, h - 2, v)


def rect(x: int, y: int, w: int, h: int, v: int):
    draw = False
    for oy in range(0, h, 1):
        if not draw:
            draw = in_bounds(x, y + oy)
        if draw:
            if not in_bounds(x, y + oy):
                return None
            line_h(x, y + oy, w, v)


class Image:
    def __init__(self, w: int, h: int, data: bytes):
        self.w = w
        self.h = h
        self.data = data
        
    


class MonoImage(Image):
    pass


def image(img: MonoImage, x: int, y: int, v: int) -> None:
    raw.image(x, y, img.w, img.h, v, SCR.COLOR.BRIGHT, SCR.COLOR.DARK, SCR.WIDTH, SCR.HEIGHT, paint_group, img.data)


def write_char(c: str, x: int, y: int, v: int, font: Font) -> None:
    f = font()
    char = getattr(f, "c" + (str(hex(ord(c))))[2:].upper(), None)
    if not char:
        return None
    image(MonoImage(f.w, f.h, char), x, y, v)


def write(s: str, x: int, y: int, v: int, font: Font) -> None:
    f = font()
    ox = 0
    oy = 0
    for c in s:
        if c == "\n":
            ox = 0
            oy += 1
        elif c == "\r":
            ox = 0
        elif c == "\b":
            ox -= (1 if ox > 0 else 0)
        else:
            write_char(c, x + ox * f.w, y + oy * f.h, v, font)
            ox += 1
