import numpy as np

from individual import Individual


class EvolutionaryAlgorithm():
    MAX_GEN = 50
    POP_SIZE = 15
    TOURNAMENT_BETTER_WIN_PROB = 0.8
    CROSSOVER_PROB = 0.8
    MUTATION_PROB = 0.05

    def run(self, starting_population):
        elites = self.gen_alg(starting_population, self.MAX_GEN, self.POP_SIZE, self.TOURNAMENT_BETTER_WIN_PROB,
                     self.CROSSOVER_PROB, self.MUTATION_PROB)
        self.last_run_elites = elites

    def tour_sel(self, population, fitnesses, prob_better_win):
        selected_idx = list(np.random.choice(len(fitnesses), 2, replace=False))
        better_bin = not fitnesses[selected_idx[0]] > fitnesses[selected_idx[1]]
        return_bin = better_bin ^ (np.random.rand() > prob_better_win)
        return population[selected_idx[return_bin]]


    def gen_alg(self, starting_population, max_gen=333, pop_size=15, prob_better_win=0.8, prob_cross=0.7, prob_mutation = 0.05):
        elites = []
        population = starting_population

        for igen in range(max_gen):
            new_population = []
            fitnesses = list(map(lambda x: x.fitness(), population))
            elite = population[np.argmax(fitnesses)]
            elites.append(elite)

            # Tournament selection
            for i in range(pop_size - 1):
                new_population.append(self.tour_sel(population, fitnesses, prob_better_win))

            # Mutation
            map(lambda x: x.mutate(prob_mutation), new_population)

            # Crossover
            for i in range(0, pop_size - 1, 2):
                new_population[i].crossover(new_population[i+1], prob_cross)

            new_population.append(elite) # The best individual is preserved
            population = new_population
        return elites

ea = EvolutionaryAlgorithm()
ea.run([Individual() for i in range(15)])
print([i.fitness() for i in ea.last_run_elites])

