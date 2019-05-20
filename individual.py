import numpy as np
import utils
import itertools
from game import Game


class Individual(object):
    SENSOR_MAPPING = ['food', 'wall', 'body']

    def __init__(self):
        self.game = None

    def fitness(self):
        self.game = Game()
        direction = 0

        while self.game.tick(direction) != Game.DIED:
            direction = self.get_output(self.get_input())

    def crossover(self, other):
        raise NotImplementedError

    def mutate(self):
        raise NotImplementedError

    def get_input(self):
        sensor_directions = [
            -np.pi / 2,
            0,
            np.pi / 2,
        ]
        rotation_matrices = [utils.get_rotation_matrix(d) for d in sensor_directions]

        results = []
        for rotation_matrix in rotation_matrices:
            seen_objects = []
            direction = rotation_matrix @ self.game.snake.direction
            direction = direction / np.linalg.norm(direction)
            ray_vector = [self.game.snake.head_position + x for x in [0, direction]]

            image = self.detect_point(ray_vector, self.game.food.pos, self.game.food.width)
            if image is not None:
                seen_objects.append((image, 'food'))

            for body_point in itertools.islice(self.game.snake.body, self.game.snake.ignore_collision, None):
                image = self.detect_point(ray_vector, body_point, self.game.snake.width)
                if image is not None:
                    seen_objects.append((image, 'body'))

            for wall in self.game.walls:
                for point in wall.endpoints:
                    image = self.detect_point(ray_vector, point, wall.width)
                    if image is not None:
                        seen_objects.append((image, 'wall'))

                # credit: https://rootllama.wordpress.com/2014/06/20/ray-line-segment-intersection-test-in-2d/
                v1 = self.game.snake.head_position - wall.endpoints[0]
                v2 = wall.endpoints[1] - wall.endpoints[0]
                v3 = np.array([-direction[1], direction[0]])
                denominator = v2 @ v3
                if denominator == 0:
                    continue  # in this case it will be handled by endpoints
                t_ray = -abs(np.cross(v2, v1)) / denominator
                t_wall = (v1 @ v3) / denominator

                if 0 <= t_wall <= 1 and t_ray >= 0:
                    seen_objects.append((t_ray, 'wall'))

            if not seen_objects:
                raise ValueError("Snake has seen beyond the edge of the world")
            seen_object = min(seen_objects)
            results.append(np.array([seen_object[0]]))
            object_type = np.zeros(len(self.SENSOR_MAPPING))
            object_type[self.SENSOR_MAPPING.index(seen_object[1])] = 1
            results.append(object_type)

        return np.concatenate(results)

    @staticmethod
    def detect_point(direction_vector, point, width):
        t = utils.projection_relative(*direction_vector, point)
        if t < 0:
            return None
        projection = direction_vector[0] + t * (direction_vector[1] - direction_vector[0])
        if utils.distance(projection, point) < width:
            return t
        return None

    def get_output(self, inputs):
        raise NotImplementedError
