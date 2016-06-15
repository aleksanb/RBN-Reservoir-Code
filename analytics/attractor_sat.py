from tasks.temporal import create_datasets

from rbn.sklearn_rbn_node import RBNNode
from rbn.reservoir_system import ReservoirSystem
from rbn.attractors import find_attractors
from parseconf import setup_and_parse_conf

import numpy as np

import re
import os
import json
import multiprocessing as mp
import time
import subprocess

if __name__ == '__main__':
    conf = setup_and_parse_conf()

    #TD3_train = create_datasets(
    #    1,
    #    task_size=4000,
    #    window_size=3,
    #    dataset_type='temporal_density')[0]

    #TD3_test = create_datasets(
    #    1,
    #    task_size=200,
    #    window_size=3,
    #    dataset_type='temporal_density')[0]

    #TD5_train = create_datasets(
    #    1,
    #    task_size=4000,
    #    window_size=5,
    #    dataset_type='temporal_density')[0]

    #TD5_test = create_datasets(
    #    1,
    #    task_size=200,
    #    window_size=5,
    #    dataset_type='temporal_density')[0]

    #reservoir_system.train_on(*TD3_train)
    #accuracy_TD3 = reservoir_system.test_on(*TD3_test)

    #reservoir_system.train_on(*TD5_train)
    #accuracy_TD5 = reservoir_system.test_on(*TD5_test)

    n_nodes = conf.n_nodes_range[0]
    print "NODES", n_nodes, "SAMPLES", conf.n_samples

    def get_rbn_meta(i):
        print "GOGO" + str(i)

        rbn_reservoir = RBNNode(connectivity=conf.connectivity,
                                n_nodes=n_nodes,
                                input_connectivity=n_nodes/2)

        reservoir_system = ReservoirSystem(rbn_reservoir)
        reservoir_system.train_on(*conf.training_data)
        accuracy = reservoir_system.test_on(*conf.test_data)

        bns_file = "{}/{}.bns".format(conf.output_dir, i)
        cnet_file = "{}/{}.cnet".format(conf.output_dir, i)
        acc_file = "{}/{}.acc".format(conf.output_dir, i)

        with open(cnet_file, 'w') as f:
            f.write(rbn_reservoir.into_cnet())

        with open(bns_file, 'w') as f:
            subprocess.call(['./analytics/SAT/bns', cnet_file], stdout=f)

        with open(bns_file, 'r') as bns:
            attractors = map(int, re.findall("Attractor \d+ is of length (\d+)", bns.read()))

            with open(acc_file, 'w') as acc:
                acc.write(json.dumps({
                    "accuracy": accuracy,
                    "attractors": attractors,
                    "mean_attractor_length": np.mean(attractors),
                    "n_attractors": len(attractors)
                }))

    pool = mp.Pool(conf.n_cores)
    result = pool.map(get_rbn_meta, range(conf.n_samples))
