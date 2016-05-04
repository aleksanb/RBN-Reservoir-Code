from tasks.temporal import create_datasets

from rbn.sklearn_rbn_node import RBNNode
from rbn.reservoir_system import ReservoirSystem
from rbn.attractors import find_attractors
from parseconf import setup_and_parse_conf

import numpy as np

import os
import json
import multiprocessing as mp
import time

reservoir_size=15

if __name__ == '__main__':
    conf = setup_and_parse_conf()

    reservoir_size = 15

    def get_rbn_meta(_):
        print "!!!", _
        rbn_reservoir = RBNNode(connectivity=conf.connectivity,
                                input_connectivity=reservoir_size/2,
                                n_nodes=reservoir_size)

        reservoir_system = ReservoirSystem(rbn_reservoir)
        reservoir_system.train_on(*conf.training_data)
        accuracy = reservoir_system.test_on(*conf.test_data)

        attractors_meta = find_attractors(rbn_reservoir)
        attractors_meta["accuracy"] = accuracy

        return attractors_meta

    pool = mp.Pool(conf.n_cores)
    result = pool.map(get_rbn_meta, range(conf.n_samples))

    output_file = "{}/attractor-results-{}.json".format(
        conf.output_dir,
        int(time.time()))

    with open(output_file, 'w') as f:
        json.dump(result, f, indent=4, sort_keys=True)
