import Oger
import mdp
import numpy as np

from utils import user_confirms, user_denies, default_input
from utils import dump, load, log_git_info
from rbn import rbn_node
from tasks import temporal

from rbn_reservoir_problem import RBNReservoirProblem
from ea.solve import solve

import log
import logging
import os

if __name__ == '__main__':
    # Set pickle working dir
    folder = raw_input('Set working directory for experiment: ') or None

    prefixed_path = ''
    if folder:
        prefixed_path = 'pickle_dumps/{}/'.format(folder)
        if not os.path.exists(prefixed_path):
            os.makedirs(prefixed_path)

    log.setup(logging.DEBUG, path=prefixed_path)
    log_git_info()

    # Create datasets
    dataset_type = default_input('Dataset [temporal_parity, temporal_density]',
                                 'temporal_parity')
    n_datasets = default_input('Datasets', 10)
    task_size = default_input('Dataset length', 200)
    window_size = default_input('Window size', 3)

    datasets = temporal.create_datasets(
        n_datasets,
        task_size=task_size,
        window_size=window_size,
        dataset_type=dataset_type)
    training_dataset, test_dataset = datasets[:-1], datasets[-1]

    dataset_description = '[{}-{}-{}-{}]'.format(
        dataset_type, n_datasets, task_size, window_size)
    logging.info(dataset_description)

    if not user_denies('Pickle test dataset?'):
        dump(test_dataset, dataset_description + '-dataset', folder=folder)

    # Create or load reservoir and readout layer
    if user_confirms('Use existing readout layer?'):
        readout = load('Readout pickle:', folder=folder)
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

        # Train and execute newly created flow
        flow = mdp.Flow([rbn_reservoir, readout], verbose=1)
        flow.train([None, training_dataset])

        reservoir_input, expected_output = test_dataset
        actual_output = flow.execute(reservoir_input)
        for output in actual_output:
            output[0] = 1 if output[0] > 0.5 else 0

        errors = sum(actual_output != expected_output)
        accuracy = 1 - float(errors) / len(actual_output)
        logging.info("Accuracy: {} ({} error(s) out of {})"
                     .format(accuracy, errors[0], len(actual_output)))

        # Optionally dump newly created flow
        if not user_denies('Pickle reservoir and readout layer?'):
            flow_description = '{}-{}-[ACC:{}]'.format(
                dataset_description,
                rbn_reservoir.describe(),
                accuracy)
            dump(rbn_reservoir, flow_description + '-reservoir',
                 folder=folder)
            dump(readout, flow_description + '-readout',
                 folder=folder)

    # Evolve other reservoirs with similar dynamics
    if not user_denies('Use readout layer to evolve similar rbn_reservoirs?'):
        n_nodes = readout.input_dim
        connectivity = default_input('Connectivity', 2)
        n_runs = default_input('How many GA runs?', 1)

        for i in range(n_runs):
            reservoir_problem = RBNReservoirProblem(
                n_nodes, connectivity, readout, test_dataset)

            generation, adults = solve(reservoir_problem, path=prefixed_path)

            fitnesses = [x.fitness for x in adults]
            top3 = fitnesses[-3:]
            top3.reverse()
            mean = np.mean(fitnesses)
            std = np.std(fitnesses)

            description = (
                '{}-[N:{}-K:{}]-[TOP:{}-MEAN:{}-STD:{}-GEN:{}]'
                .format(dataset_description,
                        n_nodes,
                        connectivity,
                        top3,
                        mean,
                        std,
                        generation))
            dump(adults, description, folder=folder)

            logging.info('GA run % completed, adults pickled', i)

#plt.plot(actual_output, 'r')
#plt.plot(expected_output, 'b')
#plt.show()

#plt.matshow(input_connections, cmap=plt.cm.gray)
#plt.title('Input connections')
#plt.matshow(rbn_states, cmap=plt.cm.gray)
#plt.title('RBN states')
#plt.show()
