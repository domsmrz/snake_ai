from collections import deque
import numpy as np
import itertools


class Snake(object):

    add_per_food = 5
    step = 0.01
    width = 0.05
    ignore_collision = 10

    def __init__(self, pos=None):
        self.direction = np.array([0, self.step])
        self.to_grow = self.add_per_food - 1
        if pos is None:
            pos = np.array([0, 0])
        self.body = deque([pos])

    @property
    def head_position(self):
        return self.body[0]

    def tick(self, angle=0):
        c, s = np.cos(angle), np.sin(angle)
        rotation_matrix = np.array([[c, -s], [s, c]])
        self.direction = rotation_matrix @ self.direction

        # Normalize to fix exploding direction vector over time
        self.direction = self.step * (self.direction / np.linalg.norm(self.direction))

        pos = self.head_position + self.direction
        self.body.appendleft(pos)
        if self.to_grow:
            self.to_grow -= 1
        else:
            self.body.pop()

    def detect_collision(self, point, width):
        for body_point in itertools.islice(self.body, self.ignore_collision, None):
            if np.linalg.norm(body_point - point) < self.width + width:
                return True
        return False

    def food_eaten(self):
        self.to_grow += self.add_per_food
