import datetime
import os
import pickle

import neat

import visualize
from individual import Individual


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        individual = Individual()
        individual.neat_network = net

        genome.fitness = individual.fitness()


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-16')

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    # Run for up to 30 generations.
    winner = p.run(eval_genomes, 1) ####

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    # output = winner_net.activate(sensors)
    with open("logs/neat/{}.txt".format(str(datetime.datetime.now()).replace(":", "-") + "-nn"), 'wb') as f:
        pickle.dump(winner_net, f)




if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat.config')
    run(config_path)