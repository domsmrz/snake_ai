import numpy as np


class Individual(object):
    _fitness = None

    def fitness(self):
        if self._fitness is None:
            self._fitness = np.random.rand()
        return self._fitness

    def crossover(self, other, probability):
        if np.random.rand() < probability:
            return


    def mutate(self, probability):
        if np.random.rand() < probability:
            return

    def get_input(self):
        raise NotImplementedError
    