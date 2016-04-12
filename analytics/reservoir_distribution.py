from tasks.temporal import create_datasets
from rbn.sklearn_rbn_node import RBNNode
from rbn.reservoir_system import ReservoirSystem

from utils import fst, snd

import multiprocessing as mp
import numpy as np
from argparse import ArgumentParser
import json
import operator
import os


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('directory', help='directory containing configuration file')
    arguments = parser.parse_args()

    with open('/'.join([arguments.directory + 'config.json'])) as config_file:
        conf = config_file.read()
        print conf
        config = json.loads(conf)

    # System
    n_cores = config['system']['n_cores']

    # Datasets
    training_input, training_output =\
            create_datasets(**config['datasets']['training'])[0]
    test_input, test_output =\
            create_datasets(**config['datasets']['test'])[0]

    # Reservoir
    reservoir_connectivity = config['reservoir']['connectivity']

    # Distribution
    n_nodes_range = range(*config['distribution']['n_nodes_range'])
    n_samples = config['distribution']['n_samples']

    input_connectivity_fn = eval(config['distribution']['input_connectivity_fn'])
    output_connectivity_fn = eval(config['distribution']['output_connectivity_fn'])

    def calculate_accuracy((n_nodes, input_connectivity, output_connectivity)):
        accuracies = []
        description = '-'.join(map(str,[n_nodes, input_connectivity, output_connectivity]))

        print "START-" + description

        for sample in range(n_samples):
            rbn_reservoir = RBNNode(connectivity=reservoir_connectivity,
                                    input_connectivity=input_connectivity,
                                    n_nodes=n_nodes,
                                    output_connectivity=output_connectivity)

            reservoir_system = ReservoirSystem(rbn_reservoir)
            reservoir_system.train_on(training_input, training_output)
            accuracy = reservoir_system.test_on(test_input, test_output)

            accuracies.append(accuracy)

        print "END-" + description

        return {
            "accuracies": accuracies,
            "n_nodes": n_nodes,
            "n_samples": n_samples,
            "input_connectivity": input_connectivity,
            "output_connectivity": output_connectivity
        }

    reservoir_distribution = {}
    pool = mp.Pool(n_cores)

    for n_nodes in n_nodes_range:
        reservoir_distribution[n_nodes] = []

        input_connectivity_range = input_connectivity_fn(n_nodes)
        output_connectivity_range = output_connectivity_fn(n_nodes)

        for input_connectivity in input_connectivity_range:
            for output_connectivity in output_connectivity_range:
                if output_connectivity == 0:
                    continue

                result = pool.apply_async(
                    calculate_accuracy,
                    [(n_nodes, input_connectivity, output_connectivity)])

                reservoir_distribution[n_nodes].append(result)

    pool.close()
    pool.join()

    for n in reservoir_distribution:
        for i in range(len(reservoir_distribution[n])):
            reservoir_distribution[n][i] = reservoir_distribution[n][i].get()

    with open('/'.join([arguments.directory, 'result.json']), 'w') as f:
        json.dump(reservoir_distribution, f, indent=4, sort_keys=True)
