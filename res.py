from cwio import *
from cwio.const import *
from cwio.screen import MonoImage

class ui:
    
    num_0 = MonoImage(5, 7, bytes([0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E])) # 0
    num_1 = MonoImage(5, 7, bytes([0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E])) # 1
    num_2 = MonoImage(5, 7, bytes([0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F])) # 2
    num_3 = MonoImage(5, 7, bytes([0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E])) # 3
    num_4 = MonoImage(5, 7, bytes([0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02])) # 4
    num_5 = MonoImage(5, 7, bytes([0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E])) # 6
    num_6 = MonoImage(5, 7, bytes([0x0E, 0x10, 0x1C, 0x12, 0x12, 0x12, 0x0C])) # 6
    num_7 = MonoImage(5, 7, bytes([0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08])) # 7
    num_8 = MonoImage(5, 7, bytes([0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E])) # 8
    num_9 = MonoImage(5, 7, bytes([0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C])) # 9

    _NUMBERS = (
        num_0, num_1, num_2, num_3, num_4,
        num_5, num_6, num_7, num_8, num_9
    )

    @classmethod
    def circled(cls, n: int):
        if 0 <= n <= 9:
            return cls._NUMBERS[n]
        return cls._NUMBERSP[0]

    info    = MonoImage(24, 24, bytes([0, 0, 0, 0, 126, 0, 1, 255, 128, 7, 129, 224, 14, 0, 112, 28, 0, 56, 24, 28, 24, 48, 28, 12, 48, 0, 12, 96, 120, 6, 96, 120, 6, 96, 56, 6, 96, 120, 6, 96, 112, 6, 96, 240, 6, 48, 230, 12, 48, 254, 12, 24, 124, 24, 28, 0, 56, 14, 0, 112, 7, 129, 224, 1, 255, 128, 0, 126, 0, 0, 0, 0]))
    warning = MonoImage(24, 24, bytes([0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 126, 0, 0, 102, 0, 0, 195, 0, 0, 195, 0, 1, 129, 128, 1, 153, 128, 3, 24, 192, 3, 24, 192, 6, 24, 96, 6, 24, 96, 12, 24, 48, 12, 24, 48, 24, 24, 24, 24, 0, 24, 48, 24, 12, 48, 24, 12, 96, 0, 6, 112, 0, 14, 63, 255, 252, 31, 255, 248, 0, 0, 0]))
    error   = MonoImage(24, 24, bytes([0, 0, 0, 0, 126, 0, 1, 255, 128, 7, 129, 224, 14, 0, 112, 28, 0, 56, 24, 195, 24, 48, 195, 12, 48, 231, 12, 96, 102, 6, 96, 126, 6, 96, 60, 6, 96, 60, 6, 96, 126, 6, 96, 102, 6, 48, 231, 12, 48, 195, 12, 24, 195, 24, 28, 0, 56, 14, 0, 112, 7, 129, 224, 1, 255, 128, 0, 126, 0, 0, 0, 0]))