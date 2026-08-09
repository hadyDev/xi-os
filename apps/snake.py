from cwio import *
from cwio.const import *
from random import randint
from time import sleep_ms

name = "Snake"

def main():
    GRID_SIZE = 3
    MARGIN = 5
    cols = SCR.WIDTH // GRID_SIZE
    rows = SCR.HEIGHT // GRID_SIZE
    
    snake = [(cols // 2, rows // 2)]
    dx, dy = 1, 0
    next_dx, next_dy = 1, 0 
    
    food = (randint(MARGIN, cols - 1 - MARGIN), randint(MARGIN, rows - 1 - MARGIN))
    score = 0
    
    while True:
        if keyboard.pressed_any():
            key = keyboard.get_next()
            if key == KB.KEY.UP and dy == 0: 
                next_dx, next_dy = 0, -1
            elif key == KB.KEY.DOWN and dy == 0: 
                next_dx, next_dy = 0, 1
            elif key == KB.KEY.LEFT and dx == 0: 
                next_dx, next_dy = -1, 0
            elif key == KB.KEY.RIGHT and dx == 0: 
                next_dx, next_dy = 1, 0
            elif key == KB.KEY.HOME: 
                return

        dx, dy = next_dx, next_dy
        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        
        if (new_head[0] < 0 or new_head[0] >= cols or 
            new_head[1] < 0 or new_head[1] >= rows):
            break

        if len(snake) > 1 and new_head in snake:
            break

        if new_head == food:
            snake.insert(0, new_head)
            score += 1
            while True:
                food = (randint(MARGIN, cols - 1 - MARGIN), randint(MARGIN, rows - 1 - MARGIN))
                if food not in snake: break
        else:
            snake.insert(0, new_head)
            snake.pop()

        screen.clear()
        
        for part in snake:
            screen.rect(part[0] * GRID_SIZE, part[1] * GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1, SCR.COLOR.BLACK)
            
        screen.rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1, SCR.COLOR.BRIGHT)
        
        screen.write(f"Score:{score}", 0, 0, SCR.COLOR.BLACK, font.miniwi)
        screen.apply()
        
        sleep_ms(150)

    screen.clear()
    screen.write("GAME OVER", 10, 20, SCR.COLOR.BLACK, font.miniwi)
    screen.write(f"FINAL SCORE: {score}", 10, 35, SCR.COLOR.BLACK, font.miniwi)
    screen.apply()
    while not keyboard.pressed_any(): pass
    keyboard.get_next()