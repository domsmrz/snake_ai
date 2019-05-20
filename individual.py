import numpy as np
import utils
import itertools
from game import Game
from neural_network import NeuralNetwork


class Individual(object):
    SENSOR_MAPPING = ['food', 'wall', 'body']
    sensor_directions = [
        -np.pi / 2,
        -np.pi / 4,
        -np.pi / 8,
        -np.pi / 16,
        0,
        np.pi / 16,
        np.pi / 8,
        np.pi / 4,
        np.pi / 2,
    ]

    def __init__(self):
        self.game = None
        self.brain = [NeuralNetwork(len(self.sensor_directions) * 4, [5, 5]) for _ in range(2)]

    def fitness(self):
        f = list(map(self.single_fitness, range(5)))
        return sum(f) / len(f)

    def single_fitness(self, rubbish=None):
        self.game = Game()

        max_ticks = 1000
        tick = 0
        max_ticks_food = 100
        tick_food = 0
        result = self.game.NOTHING
        while result != Game.DIED and tick < max_ticks and tick_food < max_ticks_food:
            direction = self.get_output(self.get_input())
            result = self.game.tick(direction)
            tick += 1
            tick_food += 1
            if result == Game.FOOD_EATEN:
                tick_food = 0

        return 1000 * self.game.score + 600 - 200 * utils.distance(self.game.food.pos, self.game.snake.head_position)

    def crossover(self, other, probability):
        if np.random.rand() < probability:
            return
        self.brain, other.brain = [self.brain[0], other.brain[1]], [other.brain[0], other.brain[1]]

    def mutate(self, probability):
        for network in self.brain:
            for layer in network.weights:
                to_change = np.random.rand(*layer.shape) < probability
                std = np.std(layer)
                add = np.random.normal(scale=std, size=layer.shape)
                layer += add * to_change

    def get_input(self, canvas=None, scale=None):
        rotation_matrices = [utils.get_rotation_matrix(d) for d in self.sensor_directions]

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

            if canvas is not None:
                x, y = self.game.snake.head_position
                x, y = x * scale, y * scale
                m = x + direction[0] * seen_object[0] * scale
                n = y + direction[1] * seen_object[0] * scale
                canvas.create_line(x, y, m, n, width=1, fill="red")

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
        network = self.brain[np.random.random() < 0.5]
        return network.evaluate(inputs)
