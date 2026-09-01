import utime
from random import randint
from cwio import *
from cwio.const import *

name = "Snake"

def main():
    GRID_SIZE = 1
    COLS = SCR.WIDTH // GRID_SIZE  
    ROWS = SCR.HEIGHT // GRID_SIZE 
    
    FRAME_DELAY_MS = 41 
    
    move_speed = 70  
    last_move_time = utime.ticks_ms()
    last_frame_time = utime.ticks_ms()
    
    snake = [(30, 30), (31, 30), (32, 30)]
    dx, dy = 1, 0
    next_dx, next_dy = 1, 0
    
    can_change_dir = True

    def get_valid_food():
        while True:
            fx = randint(2, COLS - 3)
            fy = randint(2, ROWS - 3)
            if (fx, fy) not in snake:
                return (fx, fy)

    food = get_valid_food()
    score = 0
    dirty = True

    while True:
        now = utime.ticks_ms()
        
        if keyboard.pressed_any():
            key = keyboard.get_next(show_icon=False)
            
            if key in (KB.KEY.HOME, KB.KEY.AC):
                return
            
            if can_change_dir:
                if key == KB.KEY.UP and dy == 0:
                    next_dx, next_dy = 0, -1
                    can_change_dir = False
                elif key == KB.KEY.DOWN and dy == 0:
                    next_dx, next_dy = 0, 1
                    can_change_dir = False
                elif key == KB.KEY.LEFT and dx == 0:
                    next_dx, next_dy = -1, 0
                    can_change_dir = False
                elif key == KB.KEY.RIGHT and dx == 0:
                    next_dx, next_dy = 1, 0

        if utime.ticks_diff(now, last_move_time) >= move_speed:
            last_move_time = now
            dx, dy = next_dx, next_dy
            can_change_dir = True
            
            head_x, head_y = snake[-1]
            new_head = (head_x + dx, head_y + dy)
            
            if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
                break
                
            if new_head in snake:
                break

            snake.append(new_head)
            
            if new_head[0] == food[0] and new_head[1] == food[1]:
                score += 1
                food = get_valid_food()
                move_speed = max(30, move_speed - 1) 
            else:
                snake.pop(0)  
                
            dirty = True

        if dirty and utime.ticks_diff(now, last_frame_time) >= FRAME_DELAY_MS:
            last_frame_time = now
            dirty = False

            screen.clear_screen()
            
            screen.set(food[0], food[1], SCR.COLOR.BLACK)
            
            for part in snake:
                screen.set(part[0], part[1], SCR.COLOR.BLACK)
                
            screen.write(f"S:{score}", 2, 0, SCR.COLOR.DARK, font.miniwi)
            screen.apply()

    screen.clear_screen()
    screen.write("GAME OVER", 20, 20, SCR.COLOR.BLACK, font.miniwi)
    screen.write(f"SCORE: {score}", 20, 35, SCR.COLOR.BLACK, font.miniwi)
    screen.apply()
    keyboard.wait()