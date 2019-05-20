if __name__ == '__main__':

    from evolutionary_algorithm import EvolutionaryAlgorithm
    from individual import Individual
    import pickle

    ea = EvolutionaryAlgorithm()
    ea.MAX_GEN = 50
    starting_population = [Individual() for i in range(11)]
    ea.run(starting_population)

    with open("nn.txt", 'wb') as f:
        pickle.dump(ea.last_run_elites[-1], f)