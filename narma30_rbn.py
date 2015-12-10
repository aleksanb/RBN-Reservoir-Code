import Oger
import mdp
#import matplotlib.pyplot as plt
import pickle
import math
from datetime import datetime
import numpy as np

from utils import confirm, default_input
from rbn import rbn_node, complexity_measures
from tasks import temporal

from rbn_reservoir_problem import RBNReservoirProblem
from ea.solve import solve

import log
import logging

log.setup(logging.DEBUG)


def rbn_genome_size(n_nodes, connectivity):
    bits_for_input_connection = 1
    bits_for_node_neighbors = connectivity * int(
        math.ceil(math.log(n_nodes, 2)))
    bits_for_transition_table = connectivity

    bits_per_node = (bits_for_input_connection +
                     bits_for_node_neighbors +
                     bits_for_transition_table)

    return bits_per_node * n_nodes


#plt.matshow(test_dataset[0][:10], cmap=plt.cm.gray)
#plt.title('Test input')
#plt.matshow(test_dataset[1][:10], cmap=plt.cm.gray)
#plt.title('Test output')



def execute_dataset(flow, (reservoir_input, expected_output)):
    reservoir = flow[0]
    readout = flow[1]

    actual_output = flow.execute(reservoir_input)
    for output in actual_output:
        output[0] = 1 if output[0] > 0.5 else 0

    complexity = complexity_measures.measure_computational_capability(
        reservoir, 100, 3)
    errors = sum(actual_output != expected_output)
    accuracy = 1 - float(errors) / len(actual_output)
    print "Accuracy: {} ({} errors out of {}, reservoir complexity: {})"\
        .format(accuracy, errors, len(actual_output), complexity)

    if raw_input('Pickle reservoir and readout layers? [y/N] ').strip() == 'y':
        date = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        pickle_dir = 'pickle_dumps'
        reservoir_path = '{}/{}-reservoir'.format(pickle_dir, date)
        readout_path = '{}/{}-readout'.format(pickle_dir, date)

        pickle.dump(reservoir, open(reservoir_path, 'w'))
        pickle.dump(readout, open(readout_path, 'w'))


if __name__ == '__main__':
    # Create datasets
    datasets = default_input('Datasets', 10)
    task_size = default_input('Dataset length', 200)
    window_size = default_input('Window size', 3)

    datasets = temporal.create_datasets(
        datasets,
        task_size=task_size,
        window_size=window_size,
        dataset_type="temporal_parity")
    training_dataset, test_dataset = datasets[:-1], datasets[-1]

    # Create or load reservoir and readout layer
    loaded_from_pickle = confirm('Load RBN+Readout from pickle?')
    if loaded_from_pickle:
        reservoir_path = 'pickle_dumps/' + raw_input('Reservoir pickle: ')
        readout_path = 'pickle_dumps/' + raw_input('Readout pickle: ')
        rbn_reservoir = pickle.load(open(reservoir_path, 'r'))
        readout = pickle.load(open(readout_path, 'r'))
    else:
        connectivity = default_input('connectivity', 2)
        n_nodes = default_input('n_nodes', 100)
        input_connectivity = default_input('input_connectivity', 50)
        rbn_reservoir = rbn_node.RBNNode(connectivity=connectivity,
                                         output_dim=n_nodes,
                                         input_connectivity=input_connectivity)

        readout = Oger.nodes.RidgeRegressionNode(input_dim=n_nodes,
                                                 output_dim=1,
                                                 verbose=True)

    # Train and execute reservoir system if freshly created
    flow = mdp.Flow([rbn_reservoir, readout], verbose=1)
    if not loaded_from_pickle:
        flow.train([None, training_dataset])
        execute_dataset(flow, test_dataset)

    # Evolve other reservoirs with similar dynamics
    if confirm('Use readout layer to evolve rbn_reservoir?'):
        reservoir_problem = RBNReservoirProblem(
            rbn_reservoir.n_nodes, rbn_reservoir.connectivity,
            readout, test_dataset)

        generation, adults = solve(reservoir_problem)

#plt.plot(actual_output, 'r')
#plt.plot(expected_output, 'b')
#plt.show()

#plt.matshow(input_connections, cmap=plt.cm.gray)
#plt.title('Input connections')
#plt.matshow(rbn_states, cmap=plt.cm.gray)
#plt.title('RBN states')
#plt.show()
