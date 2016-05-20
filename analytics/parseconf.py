from argparse import ArgumentParser
from tasks.temporal import create_datasets

import os.path as path
import os
import json
import pickle

def setup_and_parse_conf():
    parser = ArgumentParser()
    parser.add_argument('config', help='Path to configuration file')
    parser.add_argument('--output_dir', help='where to store output')
    arguments = parser.parse_args()

    with open(arguments.config) as f:
        config = json.loads(f.read())

    _output_dir = conf_dir =\
        path.dirname(path.join(os.getcwd(), arguments.config))
    if arguments.output_dir:
        _output_dir = path.join(os.getcwd(), arguments.output)

    training_file = path.join(_output_dir, 'training-dataset.pickle')
    test_file = path.join(_output_dir, 'test-dataset.pickle')

    if path.exists(training_file) and path.exists(test_file):
        _training_data = pickle.load(open(training_file, 'r'))
        _test_data = pickle.load(open(test_file, 'r'))

        print "Using pickled training and test data from files (%s, %s)" % (training_file, test_file)
    else:
        _training_data = create_datasets(**config['datasets']['training'])[0]
        _test_data = create_datasets(**config['datasets']['test'])[0]

        pickle.dump(_training_data, open(training_file, 'w'))
        pickle.dump(_test_data, open(test_file, 'w'))

        print "Created fresh training and test data, stored in (%s, %s)" % (training_file, test_file)

    class AnalyticsConfiguration():
	output_dir = _output_dir

        # System
        n_cores = config['system']['n_cores']

        # Datasets
        training_data = _training_data
        test_data = _test_data

        # Reservoir
        connectivity = config['reservoir']['connectivity']

        # Distribution
        n_nodes_range = range(*config['distribution']['n_nodes_range'])
        n_samples = config['distribution']['n_samples']

        def input_connectivity_fn(self, *args):
            return eval(config['distribution']['input_connectivity_fn'])(*args)

        def output_connectivity_fn(self, *args):
            return eval(config['distribution']['output_connectivity_fn'])(*args)


    return AnalyticsConfiguration()
