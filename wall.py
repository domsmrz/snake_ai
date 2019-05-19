import numpy as np


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
        t = max(0, min(1, ((point - self.endpoints[0]) @ (self.endpoints[1] - self.endpoints[0])) / self.squared_length))
        projection = self.endpoints[0] + t * (self.endpoints[1] - self.endpoints[0])
        return np.linalg.norm(point - projection)

    def detect_collision(self, point, width):
        distance = self.compute_distance(point)
        print("{} ?< {}".format(distance, self.width + width))
        return distance < self.width + width
