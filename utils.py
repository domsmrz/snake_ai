import numpy as np


def projection_relative(a, b, p, squared_length=None):
    if squared_length is None:
        dir_vector = a - b
        squared_length = np.inner(dir_vector, dir_vector)
    return ((p - a) @ (b - a)) / squared_length


def projection_line(a, b, p, squared_length=None):
    t = projection_relative(a, b, p, squared_length)
    return a + t * (b - a)


def projection_line_segment(a, b, p, squared_length=None):
    t = projection_relative(a, b, p, squared_length)
    if t < 0:
        t = 0
    if t > 1:
        t = 1
    return a + t * (b - a)


def distance(a, b):
    return np.linalg.norm(a - b)


def get_rotation_matrix(theta):
    s = np.sin(theta)
    c = np.cos(theta)
    return np.array([
        [c, -s],
        [s, c],
    ])
