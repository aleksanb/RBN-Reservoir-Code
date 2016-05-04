from tasks.temporal import create_datasets
from rbn.sklearn_rbn_node import RBNNode
from rbn.reservoir_system import ReservoirSystem

from utils import fst, snd

import multiprocessing as mp
import numpy as np
import json
import operator
import os
import time

from parseconf import setup_and_parse_conf


if __name__ == '__main__':
    conf = setup_and_parse_conf()

    def calculate_accuracy((n_nodes, input_connectivity, output_connectivity)):
        accuracies = []
        description = '-'.join(map(str,[n_nodes, input_connectivity, output_connectivity]))

        print "START-" + description

        for sample in range(conf.n_samples):
            rbn_reservoir = RBNNode(connectivity=conf.connectivity,
                                    input_connectivity=input_connectivity,
                                    n_nodes=n_nodes,
                                    output_connectivity=output_connectivity)

            reservoir_system = ReservoirSystem(rbn_reservoir)
            reservoir_system.train_on(*conf.training_data)
            accuracy = reservoir_system.test_on(*conf.test_data)

            accuracies.append(accuracy)

        print "END-" + description

        return {
            "accuracies": accuracies,
            "n_nodes": n_nodes,
            "n_samples": conf.n_samples,
            "input_connectivity": input_connectivity,
            "output_connectivity": output_connectivity
        }

    reservoir_distribution = {}
    pool = mp.Pool(conf.n_cores)

    for n_nodes in conf.n_nodes_range:
        reservoir_distribution[n_nodes] = []
        input_connectivity_range = conf.input_connectivity_fn(n_nodes)
        output_connectivity_range = conf.output_connectivity_fn(n_nodes)

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


    output_file = "{}/distribution-results-{}.json".format(
        conf.output_dir,
        int(time.time()))

    with open(output_file, 'w') as f:
        json.dump(reservoir_distribution, f, indent=4, sort_keys=True)

    print "Result written to", output_file
