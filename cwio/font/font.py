class Font:
    def __init__(self, name: str):
        self.name = name
        
    


class MonoFont(Font):
    def __init__(self, name: str, w: int, h: int):
        super().__init__(name=name)
        self.w = w
        self.h = h
        
    
    # char variable is obtained (for 'A' it's c41)
    # c41: bytes = ...
    # obtained value (bytes object) is then split based on width and height
    # and displayed to the screen with 1bpp depth (0 is transparent)
    # if the char function doesn't exist, a blank character is drawn.
