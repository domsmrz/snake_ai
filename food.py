import numpy as np


class Food(object):

    def __init__(self, pos, width):
        self.pos = pos
        self.width = width

    def detect_collision(self, point, width):
        distance = np.linalg.norm(point - self.pos)
        return distance < width + self.width
