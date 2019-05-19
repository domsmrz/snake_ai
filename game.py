from snake import Snake
from food import Food
from wall import Wall
import numpy as np


class Game(object):

    NOTHING = 0
    DIED = 1
    FOOD_EATEN = 2

    food_width = 0.05

    def __init__(self, walls=None):
        self.width = 2
        self.height = 2
        self.snake = Snake(np.array([1, 1]))
        self.ended = False
        self.food = None

        if walls is not None:
            self.walls = walls
        else:
            self.walls = []
            endpoints = [
                ((0, 0), (0, 2)),
                ((0, 2), (2, 2)),
                ((2, 2), (2, 0)),
                ((2, 0), (0, 0)),
            ]
            for a, b in endpoints:
                self.walls.append(Wall(np.array(a), np.array(b), 0.05))

        self.gen_food()

    def check_all_collisions(self, point, width):
        if any(wall.detect_collision(point, width) for wall in self.walls):
            return True
        if self.snake.detect_collision(point, width):
            return True
        return False

    def gen_food(self):
        board_size = np.array([self.height, self.width])
        position_candidate = np.random.random(2) * board_size
        while self.check_all_collisions(position_candidate, self.food_width):
            position_candidate = np.random.random(2) * board_size
        self.food = Food(position_candidate, self.food_width)

    def tick(self, angle):
        if self.ended:
            return None

        self.snake.tick(angle)
        if self.check_all_collisions(self.snake.head_position, self.snake.width):
            self.ended = True
            return self.DIED

        if self.food.detect_collision(self.snake.head_position, self.snake.width):
            self.gen_food()
            self.snake.food_eaten()
            return self.FOOD_EATEN

        return self.NOTHING
