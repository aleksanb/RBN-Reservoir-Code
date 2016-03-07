from tasks.temporal import create_datasets
from rbn.sklearn_rbn_node import RBNNode
from sklearn.linear_model import Ridge
from utils import fst, snd

import multiprocessing as mp
import numpy as np
from argparse import ArgumentParser
import json


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('config', help='path to configuration file')
    arguments = parser.parse_args()

    with open(arguments.config) as config_file:
        conf = config_file.read()
        print conf
        config = json.loads(conf)

    n_cores = config['system']['n_cores']

    training_input, training_output =\
            create_datasets(**config['datasets']['training'])[0]
    test_input, test_output =\
            create_datasets(**config['datasets']['test'])[0]

    reservoir_connectivity = config['reservoir']['connectivity']

    n_nodes_range = range(*config['distribution']['n_nodes_range'])
    n_samples = config['distribution']['n_samples']
    input_connectivity_step_size = config['distribution']['input_connectivity_step_size']

    def calculate_accuracy((n_nodes, input_connectivity)):
        print "START-{}-{}".format(n_nodes, input_connectivity)
        for sample in range(n_samples):
            rbn_reservoir = RBNNode(connectivity=reservoir_connectivity,
                                    input_connectivity=input_connectivity,
                                    n_nodes=n_nodes)
            readout_layer = Ridge()

            training_states = rbn_reservoir.execute(training_input)
            readout_layer.fit(training_states, training_output)

            test_states = rbn_reservoir.execute(test_input)
            predictions = readout_layer.predict(test_states)
            for prediction in predictions:
                prediction[0] = 1 if prediction[0] > 0.5 else 0

            errors = sum(predictions != test_output)
            accuracy = 1 - float(errors) / len(predictions)
            print("Accuracy: {} on {} items."
                         .format(accuracy, len(predictions)))
        print "END-{}-{}".format(n_nodes, input_connectivity)

    pool = mp.Pool(n_cores)
    for n_nodes in n_nodes_range:
        input_connectivity_range = range(n_nodes_range[0], n_nodes + 1, input_connectivity_step_size)
        result = pool.map_async(
            calculate_accuracy,
            ((n_nodes, input_connectivity) for input_connectivity in input_connectivity_range))

    result.wait()
