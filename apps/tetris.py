import utime
from random import choice
from cwio import *
from cwio.const import *

name = "Tetris"

def main():
    GRID_SIZE = 2
    COLS = 12
    ROWS = 14
    
    BOARD_W = COLS * GRID_SIZE
    BOARD_H = ROWS * GRID_SIZE
    
    OFFSET_X = (SCR.WIDTH - BOARD_W) // 2
    OFFSET_Y = (SCR.HEIGHT - BOARD_H) // 2
    
    FRAME_DELAY_MS = 41
    
    drop_speed = 750
    last_drop_time = utime.ticks_ms()
    last_frame_time = utime.ticks_ms()
    
    board = [[0] * COLS for _ in range(ROWS)]
    
    SHAPES = {
        'I': [[(0,1), (1,1), (2,1), (3,1)], [(2,0), (2,1), (2,2), (2,3)]],
        'O': [[(0,0), (1,0), (0,1), (1,1)]],
        'T': [[(1,0), (0,1), (1,1), (2,1)], [(1,0), (1,1), (2,1), (1,2)], [(0,1), (1,1), (2,1), (1,2)], [(1,0), (0,1), (1,1), (1,2)]],
        'S': [[(1,0), (2,0), (0,1), (1,1)], [(1,0), (1,1), (2,1), (2,2)]],
        'Z': [[(0,0), (1,0), (1,1), (2,1)], [(2,0), (1,1), (2,1), (1,2)]],
        'J': [[(0,0), (0,1), (1,1), (2,1)], [(1,0), (2,0), (1,1), (1,2)], [(0,1), (1,1), (2,1), (2,2)], [(1,0), (1,1), (0,2), (1,2)]],
        'L': [[(2,0), (0,1), (1,1), (2,1)], [(1,0), (1,1), (1,2), (2,2)], [(0,1), (1,1), (2,1), (0,2)], [(0,0), (1,0), (1,1), (1,2)]]
    }

    def get_new_piece():
        return {'type': choice(list(SHAPES.keys())), 'rot': 0, 'x': COLS // 2 - 2, 'y': 0}

    def draw_block(bx, by, color):
        px = OFFSET_X + (bx * GRID_SIZE)
        py = OFFSET_Y + (by * GRID_SIZE)
        screen.rect(px, py, GRID_SIZE, GRID_SIZE, color)

    curr = get_new_piece()
    score = 0
    dirty = True

    while True:
        now = utime.ticks_ms()
        if keyboard.pressed_any():
            key = keyboard.get_next(show_icon=False)
            if key in (KB.KEY.HOME, KB.KEY.AC):
                return
            
            old_x, old_rot, old_y = curr['x'], curr['rot'], curr['y']
            
            if key == KB.KEY.LEFT:
                curr['x'] -= 1
            elif key == KB.KEY.RIGHT:
                curr['x'] += 1
            elif key in (KB.KEY.UP, KB.KEY.OK):
                curr['rot'] = (curr['rot'] + 1) % len(SHAPES[curr['type']])
            elif key == KB.KEY.DOWN:
                last_drop_time = 0
            elif key == KB.KEY.EXE:
                while True:
                    can_drop = True
                    for px, py in SHAPES[curr['type']][curr['rot']]:
                        if curr['y'] + py + 1 >= ROWS or (curr['y'] + py + 1 >= 0 and board[curr['y'] + py + 1][curr['x'] + px]):
                            can_drop = False
                            break
                    if can_drop: curr['y'] += 1
                    else: break
                last_drop_time = 0
            for px, py in SHAPES[curr['type']][curr['rot']]:
                nx, ny = curr['x'] + px, curr['y'] + py
                if nx < 0 or nx >= COLS or ny >= ROWS or (ny >= 0 and board[ny][nx]):
                    curr['x'], curr['rot'], curr['y'] = old_x, old_rot, old_y
                    break
            
            dirty = True
            utime.sleep_ms(30)
        if utime.ticks_diff(now, last_drop_time) >= max(120, drop_speed - (score * 2)):
            last_drop_time = now
            dirty = True
            
            can_move = True
            for px, py in SHAPES[curr['type']][curr['rot']]:
                nx, ny = curr['x'] + px, curr['y'] + py + 1
                if ny >= ROWS or (ny >= 0 and board[ny][nx]):
                    can_move = False
                    break
            
            if can_move:
                curr['y'] += 1
            else:
                score += 5
                for px, py in SHAPES[curr['type']][curr['rot']]:
                    if curr['y'] + py >= 0:
                        board[curr['y'] + py][curr['x'] + px] = 1
                new_board = [row for row in board if any(col == 0 for col in row)]
                cleared = ROWS - len(new_board)
                if cleared > 0:
                    score += (cleared ** 2) * 150
                    for _ in range(cleared):
                        new_board.insert(0, [0] * COLS)
                    board = new_board
                
                curr = get_new_piece()
                
                # Semak Game Over
                for px, py in SHAPES[curr['type']][curr['rot']]:
                    if board[curr['y'] + py][curr['x'] + px]:
                        screen.clear_screen()
                        screen.write("GAME OVER", 20, 20, SCR.COLOR.BLACK, font.miniwi)
                        screen.write(f"Score: {score}", 20, 35, SCR.COLOR.BLACK, font.miniwi)
                        screen.apply()
                        keyboard.wait()
                        return
        if dirty and utime.ticks_diff(now, last_frame_time) >= FRAME_DELAY_MS:
            last_frame_time = now
            dirty = False

            screen.clear_screen()
            
            for r in range(ROWS):
                for c in range(COLS):
                    if board[r][c]:
                        draw_block(c, r, SCR.COLOR.BLACK)
            
            for px, py in SHAPES[curr['type']][curr['rot']]:
                draw_block(curr['x'] + px, curr['y'] + py, SCR.COLOR.DARK)
                
            screen.write(f"S:{score}", 2, 2, SCR.COLOR.DARK, font.miniwi)
            screen.apply()