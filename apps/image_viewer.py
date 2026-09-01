from cwio import *
from cwio.const import *
from cwio.screen import MonoImage
import ui
import os

name = "Image Viewer"

def main():
    raw = ui.choose_file()
    screen.clear()
    with open(raw, "rb") as f:
        screen.image(MonoImage(192, 63, f.read()), 0, 0, SCR.COLOR.BLACK)
    
    screen.apply()
    keyboard.wait()

