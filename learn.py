if __name__ == '__main__':

    from evolutionary_algorithm import EvolutionaryAlgorithm
    from individual import Individual
    import pickle

    ea = EvolutionaryAlgorithm()
    starting_population = [Individual() for i in range(15)]
    ea.run(starting_population)

    with open("nn.txt", 'wb') as f:
        pickle.dump(ea.last_run_elites[-1], f)