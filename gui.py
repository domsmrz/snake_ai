import glob
import os
import time
import tkinter as tk
import pickle

from game import *
from individual import Individual
from collections import deque


def draw_scaled_line(canvas, endpoint1, endpoint2, line_width, scaling_factor=None):
    if scaling_factor is None:
        scaling_factor = scaling

    (x, y), (m, n) = endpoint1, endpoint2
    x, y, m, n = x * scaling_factor, y * scaling_factor, m * scaling_factor, n * scaling_factor
    line_width = line_width * scaling_factor

    canvas.create_line(x, y, m, n, width=line_width)


def draw_scaled_circle(canvas, coor, radius, scaling_factor=None, *args, **kwargs):
    if scaling_factor is None:
        scaling_factor = scaling

    x, y, radius = coor[0] * scaling_factor, coor[1] * scaling_factor, radius * scaling_factor
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, *args, **kwargs)


def draw_wall(canvas, endpoint1, endpoint2, line_width, scaling_factor=None):
    wall_color = "black"
    draw_scaled_line(canvas, endpoint1, endpoint2, line_width * 2, scaling_factor)
    draw_scaled_circle(canvas, endpoint1, line_width, scaling_factor, fill=wall_color)
    draw_scaled_circle(canvas, endpoint2, line_width, scaling_factor, fill=wall_color)


def get_score_message(score):
    return "Score: {}".format(score)


def close_window():
    global running
    running = False


angle = 0


def arrowKey(event):
    global angle
    if event.type is tk.EventType.KeyRelease:
        angle = 0
    else:
        if event.keysym == "Left":
            angle = -1
        elif event.keysym == "Right":
            angle = 1


game = Game()
#individual = Individual()
list_of_files = glob.glob('logs/*.txt') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

with open(latest_file, "rb") as f:
    individual = pickle.load(f)
individual.game = game
individual.inputs = deque(maxlen=individual.memory_size)

scaling = 100
line_width = 5

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", close_window)
root.bind('<Left>', arrowKey)
root.bind('<KeyRelease-Left>', arrowKey)
root.bind('<Right>', arrowKey)
root.bind('<KeyRelease-Right>', arrowKey)

root.title("AI-Snake")

canvas = tk.Canvas(root, width=game.width * scaling, height=game.height * scaling, background="white")
canvas.pack()

score_message = tk.StringVar()
score_label = tk.Label(root, textvariable=score_message)
score_label.pack()

running = True

result = None
tick = 0
while result is not game.DIED and running:
    tick += 1
    canvas.delete("all")
    individual_angle = individual.get_output(individual.get_input())
    result = game.tick(individual_angle)
    print(individual_angle)
    #result = game.tick(angle)

    individual.get_input(canvas, scaling)

    # Score
    if result == game.DIED:
        score_message.set("GAME OVER, score: {}".format(game.score))
    else:
        score_message.set(get_score_message(game.score) + ", tick: " + str(tick))

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

while running:
    root.update()
    time.sleep(0.1)
