import utime
from cwio import *
from cwio.const import *

name = "3D-Test"

SIN_TABLE = tuple(int(round(__import__('math').sin(__import__('math').radians(i)) * 1000)) for i in range(360))
COS_TABLE = tuple(int(round(__import__('math').cos(__import__('math').radians(i)) * 1000)) for i in range(360))

CUBE_NODES = ((-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1))
CUBE_EDGES = ((0,1),(1,3),(3,2),(2,0),(4,5),(5,7),(7,6),(6,4),(0,4),(1,5),(2,6),(3,7))

PYRAMID_NODES = ((0.0,1.5,0.0),(-1.2,-1.0,-1.2),(1.2,-1.0,-1.2),(1.2,-1.0,1.2),(-1.2,-1.0,1.2))
PYRAMID_EDGES = ((1,2),(2,3),(3,4),(4,1),(0,1),(0,2),(0,3),(0,4))

HUMAN_NODES = (
    (-0.3,1.8,-0.3),(0.3,1.8,-0.3),(0.3,2.4,-0.3),(-0.3,2.4,-0.3),
    (-0.3,1.8,0.3),(0.3,1.8,0.3),(0.3,2.4,0.3),(-0.3,2.4,0.3),
    (-0.6,0.2,-0.3),(0.6,0.2,-0.3),(0.6,1.6,-0.3),(-0.6,1.6,-0.3),
    (-0.6,0.2,0.3),(0.6,0.2,0.3),(0.6,1.6,0.3),(-0.6,1.6,0.3),
    (-1.2,0.2,0.0),(-0.6,1.4,0.0),(1.2,0.2,0.0),(0.6,1.4,0.0),
    (-0.4,-1.6,0.0),(-0.3,0.2,0.0),(0.4,-1.6,0.0),(0.3,0.2,0.0)
)
HUMAN_EDGES = (
    (0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7),
    (8,9),(9,10),(10,11),(11,8),(12,13),(13,14),(14,15),(15,12),(8,12),(9,13),(10,14),(11,15),
    (0,11),(1,10),(16,17),(18,19),(20,21),(22,23)
)

XIOS_NODES = (
    (-2.5,0.8,0),(-1.5,-0.8,0),(-1.5,0.8,0),(-2.5,-0.8,0),
    (-0.8,0.8,0),(-0.8,-0.8,0),(-1.1,0.8,0),(-0.5,0.8,0),
    (-0.2,0.8,0),(0.8,0.8,0),(0.8,-0.8,0),(-0.2,-0.8,0),
    (2.2,0.8,0),(1.2,0.8,0),(1.2,0.0,0),(2.2,0.0,0),(1.2,-0.8,0)
)
XIOS_EDGES = (
    (0,1),(2,3),(4,5),(6,7),(8,9),(9,10),(10,11),(11,8),(12,13),(13,14),(14,15),(15,16)
)


def main():
    MODELS = (
        (CUBE_NODES, CUBE_EDGES, 12),
        (PYRAMID_NODES, PYRAMID_EDGES, 11),
        (HUMAN_NODES, HUMAN_EDGES, 8),
        (XIOS_NODES, XIOS_EDGES, 10)
    )
    current_model = 0

    deg_x = 0
    deg_y = 0
    cam_dist = 5.5

    proj_x = [0] * 24
    proj_y = [0] * 24

    fps_timer = utime.ticks_ms()
    fps_count = 0
    fps_display = "0 FPS"

    CENTER_X = 96
    CENTER_Y = 31

    s_set = screen.set
    s_clear = screen.clear_screen
    s_apply = screen.apply
    s_write = screen.write

    while True:
        now = utime.ticks_ms()

        if keyboard.pressed_any():
            key = keyboard.get_next(show_icon=False)

            if key in (KB.KEY.HOME, KB.KEY.AC, KB.KEY.BACK):
                return
            elif key == KB.KEY.RIGHT:
                current_model = (current_model + 1) % len(MODELS)
            elif key == KB.KEY.LEFT:
                current_model = (current_model - 1) % len(MODELS)
            elif key == KB.KEY.UP:
                cam_dist -= 0.3
                if cam_dist < 2.0: cam_dist = 2.0
            elif key == KB.KEY.DOWN:
                cam_dist += 0.3
                if cam_dist > 12.0: cam_dist = 12.0

        fps_count += 1
        if utime.ticks_diff(now, fps_timer) >= 500:
            fps_display = str(fps_count * 2) + " FPS"
            fps_count = 0
            fps_timer = now

        nodes, edges, base_scale = MODELS[current_model]

        deg_x = (deg_x + 3) % 360
        deg_y = (deg_y + 5) % 360

        cx, sx = COS_TABLE[deg_x], SIN_TABLE[deg_x]
        cy, sy = COS_TABLE[deg_y], SIN_TABLE[deg_y]

        for i in range(len(nodes)):
            x, y, z = nodes[i]

            y1 = (y * cx - z * sx) / 1000.0
            z1 = (y * sx + z * cx) / 1000.0

            x2 = (x * cy + z1 * sy) / 1000.0
            z2 = (-x * sy + z1 * cy) / 1000.0

            focal = cam_dist / (cam_dist + z2)

            proj_x[i] = int(CENTER_X + x2 * base_scale * focal)
            proj_y[i] = int(CENTER_Y + y1 * base_scale * focal)

        s_clear()

        for e0, e1 in edges:
            x0 = proj_x[e0]
            y0 = proj_y[e0]
            x1 = proj_x[e1]
            y1 = proj_y[e1]

            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx_dir = 1 if x0 < x1 else -1
            sy_dir = 1 if y0 < y1 else -1
            err = dx - dy

            while True:
                if 0 <= x0 < 192 and 0 <= y0 < 63:
                    s_set(x0, y0, SCR.COLOR.BLACK)

                if x0 == x1 and y0 == y1:
                    break

                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x0 += sx_dir
                if e2 < dx:
                    err += dx
                    y0 += sy_dir

        s_write(fps_display, 2, 0, SCR.COLOR.DARK, font.miniwi)
        s_apply()
