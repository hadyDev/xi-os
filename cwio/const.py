class SCR:
    class ENUM:
        class MODE:
            NONE = 0
            ALL = 1
            HEADER = 2
            BUFFER = 4
            FLIP_X = 16
            FLIP_Y = 32
            COLOR = 64
        
        class CONTRAST:
            MIN = 0
            MAX = 31
        
        class SELECT:
            PLANE0 = 0
            PLANE1 = 4
        
        class POWER:
            OFF = 0
            ON = 1
            RESET = 2
        
        class BUFFER:
            SHIFT = 63489
            SCREEN = 63520
        
    
    class COLOR:
        WHITE = 0
        BRIGHT = 1
        DARK = 2
        BLACK = 3
    
    class ICON:
        SHIFT = 1
        MATHIO = 3
        DEG = 4
        RAD = 5
        GRA = 6
        FIX = 7
        SCI = 8
        ENG = 10
        COMP = 11
        POLAR = 12
        ARROW = 13
        OK = 14
        LEFT = 16
        DOWN = 17
        UP = 18
        RIGHT = 19
        PAUSE = 21
        POWER = 22
    
    RANGE = 61488
    MODE = 61489
    CONTRAST = 61490
    BRIGHTNESS = 61491
    INTERVAL = 61492
    SCAN_OPT = 61493
    SCAN_ENABLE = 61494
    SELECT = 61495
    OFFSET = 61497
    SCAN = 61499
    POWER = 61501
    #         = 0xF03E UNKNOWN
    #         = 0xF03F UNKNOWN
    BUFFER = 63488
    SIZE = 1536
    TRUE_SIZE = 2048
    
    WIDTH = 192
    WIDTH_B = 24
    HEIGHT = 63
    HEADER = 1
    TRUE_WIDTH = 256
    TRUE_WIDTH_B = 32
    TRUE_HEIGHT = 64


class KB:
    class KEY:
        N1 = 0
        N4 = 1
        N7 = 2
        ANS = 49
        X = 46
        SHIFT = 7
        SETTINGS = 6
        N2 = 8
        N5 = 9
        N8 = 10
        SIN = 28
        FRACTION = 5
        VARIABLE = 3
        BACK = 26
        HOME = 15
        N3 = 16
        N6 = 17
        N9 = 18
        COS = 36
        SQRT = 13
        FUNCTION = 11
        LEFT = 22
        ADD = 24
        MULTIPLY = 25
        BKSPACE = 26
        TAN = 44
        POWER = 29
        DOWN = 30
        OK = 48
        UP = 23
        SUBTRACT = 32
        DIVIDE = 33
        AC = 34
        LPAREN = 19
        POWER_2 = 21
        CATALOG = 14
        RIGHT = 31
        RPAREN = 27
        LOG = 37
        TOOLS = 39
        EXE = 48
        POWER_10 = 50
        DOT = 51
        N0 = 52
        # 991EX only
        INTEGRAL = 38
        LN = 45
        NEGATIVE = 4
        DRG = 12
        POWER_M1 = 20
        S_D = 35
        MEMORY = 43
        # 991CW only
        PG_DOWN = -46
        PG_UP = -47
        FORMAT = 35
    
    IN = 61504
    IN_PULL_UP = 61505
    IN_MASK = 61506
    #         = 0xF043 only LSB of 0xF044 are used, so this is useless
    OUT_MASK = 61508
    #         = 0xF045 only LSB of 0xF046 are used, so this is useless
    OUT = 61510

