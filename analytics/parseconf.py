from argparse import ArgumentParser
from tasks.temporal import create_datasets

import os.path
import os
import json

def setup_and_parse_conf():
    parser = ArgumentParser()
    parser.add_argument('config', help='Path to configuration file')
    parser.add_argument('--output_dir', help='where to store output')
    arguments = parser.parse_args()

    with open(arguments.config) as f:
        config = json.loads(f.read())

    _output_dir = conf_dir =\
        os.path.dirname(os.path.join(os.getcwd(), arguments.config))
    if arguments.output_dir:
        _output_dir = os.path.join(os.getcwd(), arguments.output)

    class AnalyticsConfiguration():
	output_dir = _output_dir

        # System
        n_cores = config['system']['n_cores']

        # Datasets
        training_data = create_datasets(**config['datasets']['training'])[0]
        test_data = create_datasets(**config['datasets']['test'])[0]

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
