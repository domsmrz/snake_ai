import numpy as np
import utils
import itertools
from game import Game
from neural_network import NeuralNetwork
from collections import deque


class Individual(object):
    SENSOR_MAPPING = ['food', 'wall', 'body']
    sensor_directions = [
        -np.pi / 4,
        -np.pi / 8,
        -np.pi / 16,
        -np.pi / 64,
        np.pi / 64,
        np.pi / 16,
        np.pi / 8,
        np.pi / 4,

    ]
    memory_size = 1

    def __init__(self):
        self.game = None
        self.brain = [NeuralNetwork(len(self.sensor_directions) * len(self.SENSOR_MAPPING) * self.memory_size, [64, 32]) for _ in range(1)]
        self.inputs = None
        self.neat_network = None

    def fitness(self):
        f = list(map(self.single_fitness, range(5)))
        f.sort()
        return f[1]

    def single_fitness(self, game_seed=None):
        fitness = 0
        last_food_distance = 999999
        self.game = Game(seed=game_seed)
        self.inputs = deque(maxlen=self.memory_size)

        max_ticks = 5000
        tick = 0
        max_ticks_food = 300
        tick_food = 0
        result = self.game.NOTHING
        while result != Game.DIED and tick < max_ticks and tick_food < max_ticks_food:
            direction = self.get_output(self.get_input())
            result = self.game.tick(direction)
            tick += 1
            tick_food += 1
            if result == Game.FOOD_EATEN:
                tick_food = 0

            distance_to_food = utils.distance(self.game.food.pos, self.game.snake.head_position)
            if distance_to_food < last_food_distance:
                fitness += 10
            else:
                fitness -= 20

            fitness -= 1

        fitness += 1000 * self.game.score
        # return 1000 * self.game.score + 600 - 200 * utils.distance(self.game.food.pos, self.game.snake.head_position)
        return fitness

    def crossover(self, other, probability):
        if np.random.rand() < probability:
            return
        crossover_point = np.random.randint(1, len(self.brain[0].weights))
        self.brain[0].weights, other.brain[0].weights = \
            self.brain[0].weights[:crossover_point] + other.brain[0].weights[crossover_point:], \
            other.brain[0].weights[:crossover_point] + self.brain[0].weights[crossover_point:]
        #self.brain, other.brain = [self.brain[0], other.brain[1]], [other.brain[0], other.brain[1]]

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
                    seen_objects.append((image, 'body')) #### TODO: HACK HACK HACK change back to body

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
            #results.append(np.array([seen_object[0]]))
            object_type = np.zeros(len(self.SENSOR_MAPPING)) + 2.5
            object_type[self.SENSOR_MAPPING.index(seen_object[1])] = seen_object[0]
            results.append(object_type)

            if canvas is not None:
                x, y = self.game.snake.head_position
                x, y = x * scale, y * scale
                m = x + direction[0] * seen_object[0] * scale
                n = y + direction[1] * seen_object[0] * scale
                canvas.create_line(x, y, m, n, width=1, fill="red")

        current_input = np.concatenate(results)
        self.inputs.append(current_input)

        result = self.inputs
        if len(result) < self.memory_size:
            return np.array(self.memory_size * list(result[-1]))
        return np.concatenate(result)

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
        return self.neat_network.activate(inputs)[0]
        #network = self.brain[np.random.random() < 0.5]
        #network = self.brain[0]
        #return network.evaluate(inputs)
