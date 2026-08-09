from cwio import *
from cwio.const import *
from random import choice

name = "Tetris"

def main():
    GRID_SIZE = 4
    COLS = 12
    ROWS = 14 # Kurangkan 1 lagi supaya tak rapat sangat dengan atas
    
    OFFSET_X = (SCR.WIDTH - (COLS * GRID_SIZE)) // 2
    OFFSET_Y = SCR.HEIGHT - (ROWS * GRID_SIZE)
    
    base_speed = 30000 
    drop_timer = 0
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    
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
        shape_type = choice(list(SHAPES.keys()))
        return {'type': shape_type, 'rot': 0, 'x': COLS // 2 - 2, 'y': 0}

    curr = get_new_piece()
    score = 0

    while True:
        if keyboard.pressed_any():
            key = keyboard.get_next()
            if key == KB.KEY.HOME: return
            
            old_x, old_rot, old_y = curr['x'], curr['rot'], curr['y']
            
            if key == KB.KEY.LEFT: 
                curr['x'] -= 1
            elif key == KB.KEY.RIGHT: 
                curr['x'] += 1
            elif key == KB.KEY.UP or key == KB.KEY.OK:
                curr['rot'] = (curr['rot'] + 1) % len(SHAPES[curr['type']])
            elif key == KB.KEY.DOWN:
                drop_timer = 999999 
            elif key == KB.KEY.EXE:
                while True:
                    can_drop = True
                    for px, py in SHAPES[curr['type']][curr['rot']]:
                        if curr['y'] + py + 1 >= ROWS or (curr['y'] + py + 1 >= 0 and board[curr['y'] + py + 1][curr['x'] + px]):
                            can_drop = False
                            break
                    if can_drop: curr['y'] += 1
                    else: break
                drop_timer = 999999

            for px, py in SHAPES[curr['type']][curr['rot']]:
                nx, ny = curr['x'] + px, curr['y'] + py
                if nx < 0 or nx >= COLS or ny >= ROWS or (ny >= 0 and board[ny][nx]):
                    curr['x'], curr['rot'], curr['y'] = old_x, old_rot, old_y
                    break

        drop_timer += 5000 
        current_limit = max(4000, base_speed - (score * 12))
        
        if drop_timer >= current_limit:
            drop_timer = 0
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
                        new_board.insert(0, [0 for _ in range(COLS)])
                    board = new_board
                
                curr = get_new_piece()
                for px, py in SHAPES[curr['type']][curr['rot']]:
                    if board[curr['y'] + py][curr['x'] + px]:
                        screen.clear()
                        screen.write("GAME OVER", 20, 25, SCR.COLOR.BLACK, font.miniwi)
                        screen.write(f"Score: {score}", 20, 40, SCR.COLOR.BLACK, font.miniwi)
                        screen.apply()
                        while not keyboard.pressed_any(): pass
                        keyboard.get_next()
                        return 

        screen.clear()
        
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c]:
                    screen.rect(OFFSET_X + (c * GRID_SIZE), OFFSET_Y + (r * GRID_SIZE), GRID_SIZE-1, GRID_SIZE-1, SCR.COLOR.BLACK)
        
        for px, py in SHAPES[curr['type']][curr['rot']]:
            screen.rect(OFFSET_X + (curr['x'] + px) * GRID_SIZE, OFFSET_Y + (curr['y'] + py) * GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1, SCR.COLOR.DARK)
            
        screen.write(f"S:{score}", 2, 2, SCR.COLOR.DARK, font.miniwi)
        screen.apply()