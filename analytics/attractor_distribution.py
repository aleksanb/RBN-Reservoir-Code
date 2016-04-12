from tasks.temporal import create_datasets

from rbn.sklearn_rbn_node import RBNNode
from rbn.reservoir_system import ReservoirSystem
from rbn.attractors import find_attractors

import numpy as np

import os
import json
import multiprocessing as mp
import time


tri, tro = create_datasets(
    1,
    task_size=4000,
    window_size=3,
    dataset_type='temporal_parity')[0]

tei, teo = create_datasets(
    1,
    task_size=200,
    window_size=3,
    dataset_type='temporal_parity')[0]

reservoir_size=15

n_cores = 6

n_samples = 300

def get_rbn_meta(_):
    print "!!!", _
    rbn_reservoir = RBNNode(connectivity=3,
                            input_connectivity=reservoir_size/2,
                            n_nodes=reservoir_size)

    reservoir_system = ReservoirSystem(rbn_reservoir)
    reservoir_system.train_on(tri, tro)
    accuracy = reservoir_system.test_on(tei, teo)

    attractors_meta = find_attractors(rbn_reservoir)
    attractors_meta["accuracy"] = accuracy

    return attractors_meta

pool = mp.Pool(n_cores)
result = pool.map(get_rbn_meta, range(n_samples))

filename = "{}/results-{}.json".format(os.getcwd(), int(time.time()))
with open(filename, 'w') as f:
    json.dump(result, f, indent=4)
