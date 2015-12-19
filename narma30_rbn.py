import Oger
import mdp
import numpy as np

from utils import user_confirms, user_denies, default_input
from utils import dump, log_git_info, glob_load, get_working_dir
from rbn import rbn_node
from tasks import temporal

from rbn_reservoir_problem import RBNReservoirProblem
from ea.solve import solve

import log
import logging


def create_dataset():
    dataset_type = default_input(
        'Dataset [temporal_parity, temporal_density]', 'temporal_parity')
    n_datasets = default_input('Datasets', 10)
    task_size = default_input('Dataset length', 200)
    window_size = default_input('Window size', 3)

    datasets = temporal.create_datasets(
        n_datasets,
        task_size=task_size,
        window_size=window_size,
        dataset_type=dataset_type)

    dataset_description = '[{}-{}-{}-{}]'.format(
        dataset_type, n_datasets, task_size, window_size)

    return datasets, dataset_description


def create_reservoir():
    connectivity = default_input('connectivity', 2)
    n_nodes = default_input('n_nodes', 100)
    input_connectivity = default_input('input_connectivity', 50)
    rbn_reservoir = rbn_node.RBNNode(connectivity=connectivity,
                                     output_dim=n_nodes,
                                     input_connectivity=input_connectivity)

    return rbn_reservoir


if __name__ == '__main__':
    # Set pickle working dir
    working_dir = get_working_dir()

    log.setup(logging.DEBUG, path=working_dir)
    log_git_info()

    # Create datasets
    use_existing_dataset = user_confirms('Use existing dataset in folder?')
    if use_existing_dataset:
        test_dataset, _ = glob_load(working_dir + '*-dataset')[0]
        dataset_description = '[dataset_from_folder]'
    else:
        datasets, dataset_description = create_dataset()
        training_dataset, test_dataset = datasets[:-1], datasets[-1]

    if not use_existing_dataset and not user_denies('Pickle test dataset?'):
        dump(test_dataset, dataset_description + '-dataset',
             folder=working_dir)

    # Create or load reservoir and readout layer
    if user_confirms('Use readout layer from folder?'):
        readout, _ = glob_load(working_dir + '*readout')[0]
    else:
        rbn_reservoir = create_reservoir()
        readout = Oger.nodes.RidgeRegressionNode(
            input_dim=rbn_reservoir.output_dim,
            output_dim=1,
            verbose=True)

        # Train and execute newly created flow
        flow = mdp.Flow([rbn_reservoir, readout], verbose=1)
        flow.train([None, training_dataset])

        reservoir_input, expected_output = test_dataset
        actual_output = flow.execute(reservoir_input)
        for output in actual_output:
            output[0] = 1 if output[0] > 0.5 else 0

        errors = sum(actual_output != expected_output)
        accuracy = 1 - float(errors) / len(actual_output)

        logging.info("Accuracy: {} on {} items."
                     .format(accuracy, len(reservoir_input)))

        # Optionally dump newly created flow
        if not user_denies('Pickle reservoir and readout layer?'):
            flow_description = '{}-{}-[ACC:{}]'.format(
                dataset_description,
                rbn_reservoir.describe(),
                accuracy)
            dump(rbn_reservoir, flow_description + '-reservoir',
                 folder=working_dir)
            dump(readout, flow_description + '-readout',
                 folder=working_dir)

    # Evolve other reservoirs with similar dynamics
    if not user_denies('Use readout layer to evolve similar rbn_reservoirs?'):
        n_nodes = readout.input_dim
        connectivity = default_input('Connectivity', 2)
        n_runs = default_input('How many GA runs?', 1)

        for i in range(n_runs):
            reservoir_problem = RBNReservoirProblem(
                n_nodes, connectivity, readout, test_dataset)

            generation, adults = solve(reservoir_problem, path=working_dir)

            fitnesses = [x.fitness for x in adults]
            top3 = fitnesses[-3:]
            top3.reverse()
            mean = np.mean(fitnesses)
            std = np.std(fitnesses)

            description = (
                '{}-[N:{}-K:{}]-[TOP:{}-MEAN:{}-STD:{}-GEN:{}]-[{}of{}]-evolved'
                .format(dataset_description,
                        n_nodes,
                        connectivity,
                        top3,
                        mean,
                        std,
                        generation,
                        i,
                        n_runs))
            dump(adults, description, folder=working_dir)

            logging.info(
                'GA run {} of {} completed, adults pickled'.format(i, n_runs))
