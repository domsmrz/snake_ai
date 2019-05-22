if __name__ == '__main__':

    from evolutionary_algorithm import EvolutionaryAlgorithm
    from individual import Individual
    import pickle
    import datetime

    ea = EvolutionaryAlgorithm()
    ea.MAX_GEN = 25
    ea.CROSSOVER_PROB = 0.7
    starting_population = [Individual() for i in range(31)]
    ea.run(starting_population)

    with open("logs/{}.txt".format(str(datetime.datetime.now()).replace(":", "-")), 'wb') as f:
        pickle.dump(ea.last_run_elites[-1], f)
    with open("logs/population/{}.txt".format(str(datetime.datetime.now()).replace(":", "-") + "-population"), 'wb') as f:
        pickle.dump(ea.last_population, f)
    with open("logs/fitnesses/{}.txt".format(str(datetime.datetime.now()).replace(":", "-") + "-population"), 'wb') as f:
        pickle.dump(ea.saved_fitnesses, f)
