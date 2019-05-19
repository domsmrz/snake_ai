import random
import time
import tkinter as tk
from game import *

#####
### TODO:
### 1. zatvaranie aplikacie nereaguje na ESC a na krizik zleti
### 2. nejak ti nesedi kruh na konci priamky
#####

def draw_scaled_line(canvas, endpoint1, endpoint2, line_width, scaling_factor = None):
    if scaling_factor is None:
        scaling_factor = scaling

    (x, y), (m, n) = endpoint1, endpoint2
    s = scaling_factor
    canvas.create_line(x*s, y*s, m*s, n*s, width = line_width*s)

def draw_wall(canvas, endpoint1, endpoint2, line_width, scaling_factor = None):
    draw_scaled_line(canvas, endpoint1, endpoint2, line_width * 2, scaling_factor)
    draw_scaled_circle(canvas, endpoint1, line_width, scaling_factor)
    draw_scaled_circle(canvas, endpoint2, line_width, scaling_factor)

def draw_scaled_circle(canvas, coor, radius, scaling_factor = None, *args, **kwargs):
    if scaling_factor is None:
        scaling_factor = scaling

    x,y = coor
    x, y, radius = x*scaling_factor, y*scaling_factor, radius*scaling_factor
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, *args, **kwargs)


game = Game()

scaling = 100
line_width = 5

root = tk.Tk()
root.title("AI-Snake")
canvas = tk.Canvas(root, width=game.width * scaling, height=game.height * scaling, background="white")
canvas.pack()

while True:
    result = game.tick(random.random() - 1/2)

    # Food
    draw_scaled_circle(canvas, game.food.pos, game.food.width, fill="red")

    # Walls
    for wall in game.walls:
        draw_wall(canvas, *wall.endpoints, wall.width)

    # Snake
    for snake_piece in game.snake.body:
        draw_scaled_circle(canvas, snake_piece, game.snake.width, fill="black")
    draw_scaled_circle(canvas, game.snake.head_position, game.snake.width, fill="green")

    root.update_idletasks()
    root.update()

    time.sleep(0.1)
    canvas.delete("all")

