import numpy as np
import utils


class Wall(object):

    def __init__(self, a, b, width):
        self.endpoints = (a, b)
        self.width = width

        self.dir_vector = a - b
        self.squared_length = np.inner(self.dir_vector, self.dir_vector)

    def compute_distance(self, point):
        # credit: https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
        if self.squared_length == 0:
            return np.linalg.norm(self.endpoints[0] - point)
        projection = utils.projection_line_segment(*self.endpoints, point, self.squared_length)
        return np.linalg.norm(point - projection)

    def detect_collision(self, point, width):
        distance = self.compute_distance(point)
        return distance < self.width + width
